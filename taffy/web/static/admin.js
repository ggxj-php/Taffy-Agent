'use strict';

/* 后台管理前端：登录 -> 改模型 / 改聊天和图片各自的接口与 Key。
   口令是按天算的，所以这里不存任何东西，cookie 交给浏览器自己管。 */

const statusEl = document.getElementById('status');
const loginView = document.getElementById('login-view');
const panelView = document.getElementById('panel-view');
const logoutEl = document.getElementById('logout');
const loginForm = document.getElementById('login-form');
const passwordEl = document.getElementById('password');
const modelEl = document.getElementById('model');
const visionEl = document.getElementById('vision-model');
const datalistEl = document.getElementById('model-list');
const historyHintEl = document.getElementById('history-hint');
const historyEl = document.getElementById('history-chips');
const saveModelsEl = document.getElementById('save-models');
const chatBaseEl = document.getElementById('chat-base');
const chatKeyEl = document.getElementById('chat-key');
const chatStateEl = document.getElementById('chat-state');
const visionBaseEl = document.getElementById('vision-base');
const visionKeyEl = document.getElementById('vision-key');
const visionStateEl = document.getElementById('vision-state');
const saveKeysEl = document.getElementById('save-keys');

let lastState = null;

function flash(text, ok) {
  statusEl.textContent = text;
  statusEl.classList.toggle('bad', ok === false);
}

/* 统一发请求：非 2xx 就把后端给的 detail 抛出来 */
async function api(path, body) {
  const post = body !== undefined;
  const resp = await fetch(path, {
    method: post ? 'POST' : 'GET',
    headers: post ? { 'Content-Type': 'application/json' } : {},
    body: post ? JSON.stringify(body) : undefined,
  });
  let data = null;
  try {
    data = await resp.json();
  } catch (err) {
    data = null;
  }
  if (!resp.ok) {
    const error = new Error(data && data.detail ? data.detail : `服务返回 ${resp.status}`);
    error.status = resp.status;
    throw error;
  }
  return data;
}

function showLogin(message) {
  loginView.hidden = false;
  panelView.hidden = true;
  logoutEl.hidden = true;
  flash(message || '先输口令喵', false);
  passwordEl.focus();
}

function render(state) {
  lastState = state;
  loginView.hidden = true;
  panelView.hidden = false;
  logoutEl.hidden = false;

  modelEl.value = state.model;
  visionEl.value = state.vision_model;

  // 接口地址不是秘密，直接填进去给主人看着改；提交时没动过就不写盘
  chatBaseEl.value = state.chat_base_url;
  visionBaseEl.value = state.vision_base_url;
  chatStateEl.textContent = state.chat_key_source === 'admin'
    ? '当前 key 是后台设过的。'
    : '当前 key 用的是 .env 里的。';
  visionStateEl.textContent = state.vision_key_source === 'admin'
    ? '当前 key 是后台单独给图片这套设过的。'
    : '当前 key 用的是 .env 里给图片这套的默认值，跟聊天那套无关。';

  const history = state.model_history || [];
  datalistEl.innerHTML = '';
  historyEl.innerHTML = '';
  history.forEach((name) => {
    const option = document.createElement('option');
    option.value = name;
    datalistEl.appendChild(option);

    const chip = document.createElement('button');
    chip.type = 'button';
    chip.textContent = name;
    chip.addEventListener('click', () => {
      modelEl.value = name;
      flash(`已经填进「聊天模型」了喵：${name}`);
    });
    historyEl.appendChild(chip);
  });
  historyHintEl.textContent = history.length
    ? '用过的模型（点一下填进聊天模型）：'
    : '还没用过别的模型喵。';

  if (!history.length) historyEl.hidden = true;
  else historyEl.hidden = false;
}

async function load(message) {
  try {
    render(await api('/api/admin/state'));
    flash(message || '已登录喵', true);
  } catch (err) {
    showLogin(err && err.status === 401 ? '先输口令喵' : err.message);
  }
}

/* 输入框里的值和当前生效的一样，就当没改过，不写盘 */
function changed(el, current) {
  const value = el.value.trim();
  return value === current ? '' : value;
}

loginForm.addEventListener('submit', async (event) => {
  event.preventDefault();
  try {
    await api('/api/admin/login', { password: passwordEl.value });
    passwordEl.value = '';
    await load('登录成功喵～');
  } catch (err) {
    flash(err.message, false);
    passwordEl.value = '';
  }
});

logoutEl.addEventListener('click', async () => {
  try {
    await api('/api/admin/logout', {});
  } catch (err) {
    /* 退不了也要把界面切回登录页 */
  }
  showLogin('已经退出喵');
});

saveModelsEl.addEventListener('click', async () => {
  const model = modelEl.value.trim();
  const vision = visionEl.value.trim();
  if (!model || !vision) {
    flash('两个模型名都得填喵', false);
    return;
  }
  saveModelsEl.disabled = true;
  try {
    render(await api('/api/admin/models', { model, vision_model: vision }));
    flash('模型存好了喵，下一条消息就生效', true);
  } catch (err) {
    if (err.status === 401) showLogin(err.message);
    else flash(err.message, false);
  } finally {
    saveModelsEl.disabled = false;
  }
});

saveKeysEl.addEventListener('click', async () => {
  const body = {
    chat_key: chatKeyEl.value.trim(),
    vision_key: visionKeyEl.value.trim(),
    chat_base_url: changed(chatBaseEl, lastState.chat_base_url),
    vision_base_url: changed(visionBaseEl, lastState.vision_base_url),
  };
  if (!body.chat_key && !body.vision_key && !body.chat_base_url && !body.vision_base_url) {
    flash('什么都没改喵', false);
    return;
  }
  saveKeysEl.disabled = true;
  try {
    render(await api('/api/admin/keys', body));
    chatKeyEl.value = '';
    visionKeyEl.value = '';
    flash('接口设置存好了喵，下一条消息就生效', true);
  } catch (err) {
    if (err.status === 401) showLogin(err.message);
    else flash(err.message, false);
  } finally {
    saveKeysEl.disabled = false;
  }
});

load();
