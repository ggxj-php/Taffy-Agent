'use strict';

/* 网页前端：把后端的 SSE 事件流画成聊天记录。
   会话 id 存在 sessionStorage，点「新会话」换一个 id，历史就重开一份。
   用 sessionStorage 而不是 localStorage：它按标签页隔离，开两个标签页就是
   两个独立会话；同一标签页刷新仍保留，关掉标签页才丢。 */

const STORAGE_KEY = 'taffy_session_id';
const AVATAR = '/static/avatar.jpg';

/* 每种心情对应几张真·塔菲表情包，发的时候随机挑一张 */
const STICKERS = {
  happy: ['happy1', 'happy2', 'happy3'],
  think: ['think1', 'think2', 'think3'],
  confused: ['confused1', 'confused2', 'confused3'],
  proud: ['proud1', 'proud2', 'proud3'],
  cry: ['cry1', 'cry2'],
  angry: ['angry1', 'angry2', 'angry3'],
  sleepy: ['sleepy1', 'sleepy2'],
  love: ['love1', 'love2', 'love3'],
};

const messagesEl = document.getElementById('messages');
const formEl = document.getElementById('composer');
const inputEl = document.getElementById('input');
const sendEl = document.getElementById('send');
const statusEl = document.getElementById('status');
const newChatEl = document.getElementById('new-chat');
const toBottomEl = document.getElementById('to-bottom');
const pickImageEl = document.getElementById('pick-image');
const imageInputEl = document.getElementById('image-input');
const attachBarEl = document.getElementById('attach-bar');
const attachPreviewEl = document.getElementById('attach-preview');
const attachRemoveEl = document.getElementById('attach-remove');

let sessionId = sessionStorage.getItem(STORAGE_KEY);
let busy = false;
let pendingImage = null; // 已经选好、还没发出去的图片（data URL）

marked.setOptions({ gfm: true, breaks: true });

const el = (tag, cls) => {
  const node = document.createElement(tag);
  if (cls) node.className = cls;
  return node;
};

/* ---------------- 数学式子 ---------------- */

/* 模型偶尔还是漏出 LaTeX，雏草姬看不懂，这里把它翻成人能读的写法。
   代码块和行内代码里的内容一律原样保留，绝不改动。 */
const MATH_WORDS = {
  times: '×', cdot: '·', div: '÷', pm: '±', mp: '∓',
  le: '≤', leq: '≤', ge: '≥', geq: '≥', ne: '≠', neq: '≠',
  approx: '≈', equiv: '≡', sim: '∼', propto: '∝',
  infty: '∞', sum: '∑', prod: '∏', int: '∫', oint: '∮',
  partial: '∂', nabla: '∇', forall: '∀', exists: '∃',
  in: '∈', notin: '∉', subset: '⊂', subseteq: '⊆', supset: '⊃', supseteq: '⊇',
  cup: '∪', cap: '∩', emptyset: '∅', therefore: '∴', because: '∵',
  rightarrow: '→', to: '→', Rightarrow: '⇒', leftarrow: '←', Leftarrow: '⇐',
  leftrightarrow: '↔', Leftrightarrow: '⇔', mapsto: '↦',
  ldots: '…', cdots: '…', dots: '…', vdots: '⋮', ddots: '⋱',
  angle: '∠', perp: '⊥', parallel: '∥', triangle: '△', circ: '∘',
  degree: '°', log: 'log', ln: 'ln', lg: 'lg', lim: 'lim', gcd: 'gcd', mod: 'mod',
  alpha: 'α', beta: 'β', gamma: 'γ', delta: 'δ', epsilon: 'ε', varepsilon: 'ε',
  zeta: 'ζ', eta: 'η', theta: 'θ', iota: 'ι', kappa: 'κ', lambda: 'λ', mu: 'μ',
  nu: 'ν', xi: 'ξ', pi: 'π', rho: 'ρ', sigma: 'σ', tau: 'τ', upsilon: 'υ',
  phi: 'φ', varphi: 'φ', chi: 'χ', psi: 'ψ', omega: 'ω',
  Gamma: 'Γ', Delta: 'Δ', Theta: 'Θ', Lambda: 'Λ', Xi: 'Ξ', Pi: 'Π',
  Sigma: 'Σ', Upsilon: 'Υ', Phi: 'Φ', Psi: 'Ψ', Omega: 'Ω',
};

function demathExpr(expr) {
  let s = expr;
  s = s.replace(/\\[,;!]/g, ' ');
  s = s.replace(/\\(?:d|t)?frac\s*\{([^{}]*)\}\s*\{([^{}]*)\}/g, '($1)/($2)');
  s = s.replace(/\\sqrt\s*\[([^\]]*)\]\s*\{([^{}]*)\}/g, '$1√($2)');
  s = s.replace(/\\sqrt\s*\{([^{}]*)\}/g, '√($1)');
  s = s.replace(/\^\s*\{([^{}]*)\}/g, '^($1)');
  s = s.replace(/_\s*\{([^{}]*)\}/g, '_($1)');
  s = s.replace(/\\(?:text|mathrm|mathbf|mathit|operatorname)\s*\{([^{}]*)\}/g, '$1');
  s = s.replace(/\\(?:left|right)\s*/g, '');
  s = s.replace(/\\([A-Za-z]+)/g, (m, name) => (name in MATH_WORDS ? MATH_WORDS[name] : m));
  return s;
}

function demathText(seg) {
  let out = seg
    .replace(/\$\$([\s\S]+?)\$\$/g, (m, e) => demathExpr(e))
    .replace(/\\\[([\s\S]+?)\\\]/g, (m, e) => demathExpr(e))
    .replace(/\$([^$\n]+?)\$/g, (m, e) => demathExpr(e))
    .replace(/\\\(([\s\S]+?)\\\)/g, (m, e) => demathExpr(e));
  // 兜底：散落在正文里的 \le、\times 之类也翻掉，认不出来的保留原样
  return out.replace(/\\([A-Za-z]+)/g, (m, name) => (name in MATH_WORDS ? MATH_WORDS[name] : m));
}

function demath(text) {
  // 按围栏代码块 / 行内代码切分，只处理纯文本片段
  return text
    .split(/(```[\s\S]*?```|~~~[\s\S]*?~~~|`[^`\n]*`)/g)
    .map((part) => {
      const isCode = part.startsWith('```') || part.startsWith('~~~') ||
        (part.startsWith('`') && part.endsWith('`') && part.length > 1);
      return isCode ? part : demathText(part);
    })
    .join('');
}

/* ---------------- Markdown / 代码高亮 ---------------- */

function renderMarkdown(text) {
  return DOMPurify.sanitize(marked.parse(demath(text)));
}

function enhance(root) {
  root.querySelectorAll('a[href]').forEach((a) => {
    a.target = '_blank';
    a.rel = 'noopener noreferrer';
  });

  root.querySelectorAll('pre > code').forEach((code) => {
    const pre = code.parentElement;
    const langMatch = /language-([\w+#-]+)/.exec(code.className);
    hljs.highlightElement(code);
    if (pre.querySelector('.code-bar')) return;

    const bar = el('div', 'code-bar');
    const lang = el('span', 'code-lang');
    lang.textContent = langMatch ? langMatch[1] : 'text';

    const copy = el('button', 'code-copy');
    copy.type = 'button';
    copy.textContent = '复制';
    copy.addEventListener('click', async () => {
      try {
        await navigator.clipboard.writeText(code.textContent);
        copy.textContent = '已复制';
      } catch (err) {
        copy.textContent = '复制失败';
      }
      setTimeout(() => { copy.textContent = '复制'; }, 1400);
    });

    bar.append(lang, copy);
    pre.appendChild(bar);
  });
}

/* 流式下每个增量都重渲染整块，用 rAF 压一下频率，别把帧率拖垮 */
function scheduleRender(block) {
  if (block.pending) return;
  block.pending = true;
  requestAnimationFrame(() => {
    block.pending = false;
    block.el.innerHTML = renderMarkdown(block.raw);
    enhance(block.el);
    updateToBottom();
  });
}

/* ---------------- 滚动 ---------------- */

/* 不再自动吸底跟随。内容流式增长时视图一动不动，雏草姬想翻到哪就翻到哪，
   不会被新来的内容顶回去。只有发消息这一下才把最新一条带进视野。 */
function scrollToBottom() {
  messagesEl.scrollTop = messagesEl.scrollHeight;
  updateToBottom();
}

/* 只要没贴着底，右下角就冒一个「回到底部」的按钮；翻到底了它就自己藏起来。 */
const NEAR_BOTTOM = 80;

function updateToBottom() {
  const gap = messagesEl.scrollHeight - messagesEl.scrollTop - messagesEl.clientHeight;
  toBottomEl.classList.toggle('show', gap > NEAR_BOTTOM);
}

messagesEl.addEventListener('scroll', updateToBottom, { passive: true });
window.addEventListener('resize', updateToBottom);

toBottomEl.addEventListener('click', () => {
  messagesEl.scrollTo({ top: messagesEl.scrollHeight, behavior: 'smooth' });
});

/* ---------------- 消息渲染 ---------------- */

function addUser(text, image) {
  const row = el('div', 'msg user');
  const bubble = el('div', 'bubble');
  if (image) {
    const img = el('img', 'sent-image');
    img.src = image;
    img.alt = '发送的图片';
    bubble.appendChild(img);
  }
  if (text) {
    const box = el('div', 'text');
    box.textContent = text;
    bubble.appendChild(box);
  }
  row.appendChild(bubble);
  messagesEl.appendChild(row);
  scrollToBottom();
}

function addAgent() {
  const row = el('div', 'msg agent');
  const avatar = el('img', 'avatar');
  avatar.src = AVATAR;
  avatar.alt = '塔菲';
  const bubble = el('div', 'bubble');
  row.append(avatar, bubble);
  messagesEl.appendChild(row);
  scrollToBottom();
  return { row, bubble, thinking: null, content: null, tools: {} };
}

function thinkingChunk(turn, text) {
  if (!turn.thinking) {
    const box = el('details', 'thinking');
    box.open = false;
    const summary = el('summary');
    const spin = el('span', 'spin');
    const label = el('span', 'tsum');
    label.textContent = '思考中…';
    summary.append(spin, label);
    const body = el('div', 'thinking-body');
    box.append(summary, body);
    turn.bubble.appendChild(box);
    turn.thinking = { box, body };
  }
  turn.thinking.body.textContent += text;
  updateToBottom();
}

/* 正文/工具/表情包一来，就说明这段思考结束了，把标题标一下。
   盒子开不开交给雏草姬自己决定，这里不强行收起。 */
function settleThinking(turn) {
  if (!turn.thinking) return;
  turn.thinking.box.querySelector('.tsum').textContent = '已深度思考';
  turn.thinking = null;
}

function contentChunk(turn, text) {
  settleThinking(turn);
  if (!turn.content) {
    const box = el('div', 'content');
    turn.bubble.appendChild(box);
    turn.content = { el: box, raw: '', pending: false };
  }
  turn.content.raw += text;
  scheduleRender(turn.content);
}

function toolStart(turn, name, args) {
  settleThinking(turn);
  turn.content = null; // 工具跑完后的正文另起一块，保持先后顺序

  const card = el('details', 'tool');
  card.open = false;
  const summary = el('summary');
  const label = el('span', 'tname');
  label.textContent = name;
  const state = el('span', 'tstate');
  state.textContent = '运行中…';
  summary.append(label, state);

  const body = el('div', 'tool-body');
  const argsLabel = el('div', 'tool-label');
  argsLabel.textContent = '参数';
  const argsPre = el('pre', 'tool-args');
  argsPre.textContent = prettyArgs(args);
  const resultLabel = el('div', 'tool-label');
  resultLabel.textContent = '结果';
  const resultPre = el('pre', 'tool-result');
  resultPre.textContent = '等待中…';
  body.append(argsLabel, argsPre, resultLabel, resultPre);

  card.append(summary, body);
  turn.bubble.appendChild(card);
  turn.tools[name] = card;
  updateToBottom();
}

function toolEnd(turn, name, result) {
  const card = turn.tools[name];
  if (!card) return;
  card.querySelector('.tool-result').textContent = result;
  const state = card.querySelector('.tstate');
  state.textContent = '完成';
  state.classList.add('ok');
  updateToBottom();
}

function addSticker(turn, mood) {
  settleThinking(turn);
  turn.content = null;
  const safe = String(mood).replace(/[^a-z]/gi, '');
  const pool = STICKERS[safe];
  if (!pool || !pool.length) return;
  const img = el('img', 'sticker');
  img.src = `/static/stickers/${pool[Math.floor(Math.random() * pool.length)]}.png`;
  img.alt = mood;
  img.loading = 'lazy';
  img.addEventListener('error', () => img.remove());
  turn.bubble.appendChild(img);
  updateToBottom();
}

function errorBubble(turn, message) {
  settleThinking(turn);
  turn.content = null;
  const box = el('div', 'error');
  box.textContent = '喵呜…出错了：' + message;
  turn.bubble.appendChild(box);
}

function prettyArgs(raw) {
  try {
    return JSON.stringify(JSON.parse(raw), null, 2);
  } catch (err) {
    return raw || '{}';
  }
}

/* ---------------- 会话 ---------------- */

async function ensureSession(force) {
  if (!force && sessionId) return sessionId;
  const resp = await fetch('/api/session', { method: 'POST' });
  if (!resp.ok) throw new Error('开新会话失败');
  const data = await resp.json();
  sessionId = data.session_id;
  sessionStorage.setItem(STORAGE_KEY, sessionId);
  return sessionId;
}

/* ---------------- SSE ---------------- */

async function streamChat(id, message, onEvent, image) {
  const body = { session_id: id, message };
  if (image) body.image = image;
  const resp = await fetch('/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  if (!resp.ok || !resp.body) throw new Error(`服务返回 ${resp.status}`);

  const reader = resp.body.getReader();
  const decoder = new TextDecoder();
  let buffer = '';
  let done_events = false; // 收到 [DONE] 后就只把剩余字节读完，不再解析

  for (;;) {
    const { done, value } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });

    let cut;
    while ((cut = buffer.indexOf('\n\n')) >= 0) {
      const chunk = buffer.slice(0, cut);
      buffer = buffer.slice(cut + 2);
      if (done_events) continue;
      const line = chunk.split('\n').find((l) => l.startsWith('data:'));
      if (!line) continue;
      const payload = line.slice(5).trim();
      if (payload === '[DONE]') {
        done_events = true;
        continue;
      }
      try {
        onEvent(JSON.parse(payload));
      } catch (err) {
        /* 半截 JSON，忽略 */
      }
    }
  }
}

function handleEvent(turn, event) {
  switch (event.type) {
    case 'thinking':
      thinkingChunk(turn, event.text);
      break;
    case 'content':
      contentChunk(turn, event.text);
      break;
    case 'tool_start':
      // send_sticker 不用画工具卡片，紧接着的 sticker 事件就是它的样子
      if (event.name !== 'send_sticker') toolStart(turn, event.name, event.arguments);
      break;
    case 'tool_end':
      toolEnd(turn, event.name, event.result);
      break;
    case 'sticker':
      addSticker(turn, event.mood);
      break;
    case 'error':
      errorBubble(turn, event.message);
      break;
    default:
      break;
  }
}

/* ---------------- 发送 ---------------- */

async function send(text, image) {
  if (busy) return;
  busy = true;
  sendEl.disabled = true;
  pickImageEl.disabled = true;
  inputEl.value = '';
  autosize();
  statusEl.textContent = '正在思考喵…';
  addUser(text, image);
  clearImage();

  const turn = addAgent();
  try {
    const id = await ensureSession();
    await streamChat(id, text, (event) => handleEvent(turn, event), image);
  } catch (err) {
    errorBubble(turn, err && err.message ? err.message : String(err));
  } finally {
    settleThinking(turn);
    if (turn.content) scheduleRender(turn.content);
    busy = false;
    sendEl.disabled = false;
    pickImageEl.disabled = false;
    statusEl.textContent = '在线喵';
    inputEl.focus();
  }
}

/* ---------------- 输入框 ---------------- */

function autosize() {
  inputEl.style.height = 'auto';
  // scrollHeight 不含边框，而全局是 border-box，所以要把上下边框加回去，
  // 否则撑高之后输入框会比两边按钮矮 2px，又错位了。
  const cs = getComputedStyle(inputEl);
  const border = parseFloat(cs.borderTopWidth) + parseFloat(cs.borderBottomWidth);
  inputEl.style.height = Math.min(inputEl.scrollHeight + border, 140) + 'px';
}

inputEl.addEventListener('input', autosize);

/* ---------------- 发图片 ----------------
   图片只在浏览器里读成 data URL，随请求发上去；服务端不落盘，塔菲看完整轮
   就把图片数据从对话历史里抹掉，所以不会在服务器上留下任何图片文件。 */

const IMAGE_MAX_BYTES = 4 * 1024 * 1024; // 原图上限，超了直接拦掉，别让 base64 撑爆请求

function clearImage() {
  pendingImage = null;
  imageInputEl.value = '';
  attachPreviewEl.removeAttribute('src');
  attachBarEl.hidden = true;
}

pickImageEl.addEventListener('click', () => imageInputEl.click());

imageInputEl.addEventListener('change', () => {
  const file = imageInputEl.files && imageInputEl.files[0];
  if (!file) return;
  if (!file.type.startsWith('image/')) {
    statusEl.textContent = '只能发图片喵';
    clearImage();
    return;
  }
  if (file.size > IMAGE_MAX_BYTES) {
    statusEl.textContent = '图片太大了喵，限 4MB';
    clearImage();
    return;
  }
  const reader = new FileReader();
  reader.onload = () => {
    pendingImage = reader.result;
    attachPreviewEl.src = pendingImage;
    attachBarEl.hidden = false;
    statusEl.textContent = '在线喵';
    inputEl.focus();
  };
  reader.onerror = () => {
    statusEl.textContent = '读图片失败喵';
    clearImage();
  };
  reader.readAsDataURL(file);
});

attachRemoveEl.addEventListener('click', () => {
  clearImage();
  inputEl.focus();
});

/* 回车不发送，老老实实在输入框里换行；要发就点「发送」按钮。
   手机端也一样，软键盘的回车键只负责换行，不会手滑把半句话发出去。 */
formEl.addEventListener('submit', (e) => {
  e.preventDefault();
  const text = inputEl.value.trim();
  if ((!text && !pendingImage) || busy) return;
  send(text, pendingImage);
});

newChatEl.addEventListener('click', async () => {
  if (busy) return;
  clearImage();
  messagesEl.innerHTML = '';
  sessionId = null;
  sessionStorage.removeItem(STORAGE_KEY);
  updateToBottom();
  try {
    await ensureSession(true);
    welcome();
  } catch (err) {
    statusEl.textContent = '开新会话失败';
  }
  inputEl.focus();
});

/* ---------------- 开场 ---------------- */

function welcome() {
  const turn = addAgent();
  contentChunk(
    turn,
    '雏草姬来啦喵～我是永雏塔菲，有什么想聊的直接说就好喵。\n\n' +
    '算法题、代码、知识库里的资料都可以问我；嵌入式、单片机（STM32 那种）、物联网、' +
    '计算机组成原理这些塔菲也懂喵。左下角可以发图片给塔菲看（看完就删，不会留着）；' +
    '想换个话题就点右上角「新会话」，塔菲会把之前的事忘干净从头开始喵～'
  );
}

(async function init() {
  try {
    await ensureSession();
    welcome();
  } catch (err) {
    statusEl.textContent = '连不上服务喵';
  }
  inputEl.focus();
})();
