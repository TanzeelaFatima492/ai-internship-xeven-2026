<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Ervin Chatbot</title>
<script src="https://cdn.tailwindcss.com"></script>
<style>
  /* Subtle scrollbar */
  .chat-scroll::-webkit-scrollbar { width: 6px; }
  .chat-scroll::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 3px; }
  .chat-scroll::-webkit-scrollbar-thumb:hover { background: #94a3b8; }
 
  /* Typing dots */
  .typing span {
    display: inline-block;
    width: 6px; height: 6px;
    background: #94a3b8;
    border-radius: 50%;
    margin: 0 2px;
    animation: bounce 1.2s infinite ease-in-out;
  }
  .typing span:nth-child(2) { animation-delay: 0.15s; }
  .typing span:nth-child(3) { animation-delay: 0.3s; }
  @keyframes bounce {
    0%, 80%, 100% { transform: translateY(0); opacity: 0.4; }
    40% { transform: translateY(-4px); opacity: 1; }
  }
 
  /* Slide fade for view transitions */
  .view { animation: fadeIn 0.35s ease; }
  @keyframes fadeIn {
    from { opacity: 0; transform: translateY(8px); }
    to { opacity: 1; transform: translateY(0); }
  }
</style>
</head>
<body class="bg-gradient-to-br from-slate-50 via-indigo-50 to-purple-50 min-h-screen font-sans antialiased">
 
  <!-- ======================= SIGNUP VIEW ======================= -->
  <section id="view-signup" class="view min-h-screen flex items-center justify-center px-4">
    <div class="w-full max-w-md bg-white rounded-2xl shadow-xl p-8 border border-slate-100">
      <div class="text-center mb-6">
        <div class="inline-flex items-center justify-center w-14 h-14 rounded-2xl bg-gradient-to-br from-indigo-500 to-purple-600 text-white text-2xl font-bold mb-3">E</div>
        <h1 class="text-2xl font-bold text-slate-800">Create your account</h1>
        <p class="text-slate-500 text-sm mt-1">Sign up to start chatting with Ervin</p>
      </div>
 
      <form id="signupForm" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-slate-700 mb-1">Username</label>
          <input id="signupName" type="text" required minlength="2"
            class="w-full px-4 py-2.5 rounded-lg border border-slate-200 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100 outline-none transition"
            placeholder="arz" />
        </div>
        <div>
          <label class="block text-sm font-medium text-slate-700 mb-1">Email</label>
          <input id="signupEmail" type="email" required
            class="w-full px-4 py-2.5 rounded-lg border border-slate-200 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100 outline-none transition"
            placeholder="you@example.com" />
        </div>
        <div>
          <label class="block text-sm font-medium text-slate-700 mb-1">Password</label>
          <input id="signupPassword" type="password" required minlength="8"
            class="w-full px-4 py-2.5 rounded-lg border border-slate-200 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100 outline-none transition"
            placeholder="At least 8 characters" />
        </div>
 
        <div id="signupAlert" class="hidden text-sm rounded-lg px-3 py-2"></div>
 
        <button id="signupBtn" type="submit"
          class="w-full bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 text-white font-semibold py-2.5 rounded-lg transition shadow-md disabled:opacity-60 disabled:cursor-not-allowed">
          <span class="btn-label">Sign Up</span>
        </button>
      </form>
 
      <p class="text-center text-sm text-slate-500 mt-5">
        Already have an account?
        <button onclick="showView('login')" class="text-indigo-600 font-medium hover:underline">Log in</button>
      </p>
    </div>
  </section>
 
  <!-- ======================= LOGIN VIEW ======================= -->
  <section id="view-login" class="view hidden min-h-screen flex items-center justify-center px-4">
    <div class="w-full max-w-md bg-white rounded-2xl shadow-xl p-8 border border-slate-100">
      <div class="text-center mb-6">
        <div class="inline-flex items-center justify-center w-14 h-14 rounded-2xl bg-gradient-to-br from-indigo-500 to-purple-600 text-white text-2xl font-bold mb-3">E</div>
        <h1 class="text-2xl font-bold text-slate-800">Welcome back</h1>
        <p class="text-slate-500 text-sm mt-1">Log in to continue</p>
      </div>
 
      <form id="loginForm" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-slate-700 mb-1">Email</label>
          <input id="loginEmail" type="email" required
            class="w-full px-4 py-2.5 rounded-lg border border-slate-200 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100 outline-none transition"
            placeholder="you@example.com" />
        </div>
        <div>
          <label class="block text-sm font-medium text-slate-700 mb-1">Password</label>
          <input id="loginPassword" type="password" required
            class="w-full px-4 py-2.5 rounded-lg border border-slate-200 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100 outline-none transition"
            placeholder="••••••••" />
        </div>
 
        <div id="loginAlert" class="hidden text-sm rounded-lg px-3 py-2"></div>
 
        <button id="loginBtn" type="submit"
          class="w-full bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 text-white font-semibold py-2.5 rounded-lg transition shadow-md disabled:opacity-60 disabled:cursor-not-allowed">
          <span class="btn-label">Log In</span>
        </button>
      </form>
 
      <p class="text-center text-sm text-slate-500 mt-5">
        New here?
        <button onclick="showView('signup')" class="text-indigo-600 font-medium hover:underline">Create an account</button>
      </p>
    </div>
  </section>
 
  <!-- ======================= CHAT VIEW ======================= -->
  <section id="view-chat" class="view hidden min-h-screen flex flex-col">
    <!-- Header -->
    <header class="bg-white border-b border-slate-200 px-4 sm:px-6 py-3 flex items-center justify-between shadow-sm">
      <div class="flex items-center gap-3">
        <div class="w-9 h-9 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-600 text-white flex items-center justify-center font-bold">E</div>
        <div>
          <h2 class="font-semibold text-slate-800 leading-tight">Ervin Chatbot</h2>
          <p id="userBadge" class="text-xs text-slate-500">—</p>
        </div>
      </div>
      <div class="flex items-center gap-2">
        <button id="settingsBtn" title="Bot Settings"
          class="text-slate-500 hover:text-indigo-600 p-2 rounded-lg hover:bg-slate-100 transition">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
            <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
        </button>
        <button id="logoutBtn"
          class="text-sm text-slate-600 hover:text-red-600 px-3 py-1.5 rounded-lg hover:bg-red-50 transition font-medium">
          Log out
        </button>
      </div>
    </header>
 
    <!-- Settings panel -->
    <div id="settingsPanel" class="hidden bg-indigo-50/60 border-b border-indigo-100 px-4 sm:px-6 py-3">
      <div class="max-w-3xl mx-auto flex flex-col sm:flex-row gap-3 items-stretch sm:items-center">
        <div class="flex-1">
          <label class="block text-xs font-medium text-slate-600 mb-1">Bot ID</label>
          <input id="botIdInput" type="text" value="2392982"
            class="w-full px-3 py-2 rounded-lg border border-slate-200 text-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100 outline-none" />
        </div>
        <div class="flex-1">
          <label class="block text-xs font-medium text-slate-600 mb-1">Index Name</label>
          <input id="indexNameInput" type="text" value="arz"
            class="w-full px-3 py-2 rounded-lg border border-slate-200 text-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100 outline-none" />
        </div>
      </div>
    </div>
 
    <!-- Messages -->
    <main id="chatMessages" class="chat-scroll flex-1 overflow-y-auto px-4 sm:px-6 py-6 space-y-4">
      <div class="max-w-3xl mx-auto text-center text-slate-400 text-sm py-12">
        <div class="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-gradient-to-br from-indigo-100 to-purple-100 text-indigo-600 mb-3">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8">
            <path stroke-linecap="round" stroke-linejoin="round" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
          </svg>
        </div>
        <p class="font-medium text-slate-600">Start a conversation</p>
        <p class="text-xs mt-1">Ask anything to get going.</p>
      </div>
    </main>
 
    <!-- Composer -->
    <footer class="bg-white border-t border-slate-200 px-4 sm:px-6 py-3">
      <form id="chatForm" class="max-w-3xl mx-auto flex items-end gap-2">
        <textarea id="chatInput" rows="1" placeholder="Type your message..."
          class="flex-1 resize-none px-4 py-2.5 rounded-xl border border-slate-200 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100 outline-none transition max-h-32"></textarea>
        <button id="sendBtn" type="submit"
          class="bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 text-white font-semibold w-11 h-11 rounded-xl flex items-center justify-center shadow-md transition disabled:opacity-60 disabled:cursor-not-allowed shrink-0">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M5 12h14M13 6l6 6-6 6"/>
          </svg>
        </button>
      </form>
    </footer>
  </section>
 
<script>
/* ============================================================
   CONFIG
============================================================ */
const API_BASE = 'https://ervin.arzaiengineer.site/api';
const STORAGE_KEY = 'ervin_auth';
 
/* ============================================================
   VIEW SWITCHING
============================================================ */
function showView(name) {
  ['signup', 'login', 'chat'].forEach(v => {
    document.getElementById(`view-${v}`).classList.add('hidden');
  });
  const el = document.getElementById(`view-${name}`);
  el.classList.remove('hidden');
  // Re-trigger animation
  el.style.animation = 'none';
  void el.offsetWidth;
  el.style.animation = '';
}
 
/* ============================================================
   AUTH HELPERS
============================================================ */
function saveAuth(data) {
  // Note: localStorage isn't supported in artifact sandbox previews,
  // but works in real browsers. We fall back to in-memory state.
  try { localStorage.setItem(STORAGE_KEY, JSON.stringify(data)); } catch (e) {}
  window.__auth = data;
}
function loadAuth() {
  if (window.__auth) return window.__auth;
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw) { window.__auth = JSON.parse(raw); return window.__auth; }
  } catch (e) {}
  return null;
}
function clearAuth() {
  try { localStorage.removeItem(STORAGE_KEY); } catch (e) {}
  window.__auth = null;
}
 
/* ============================================================
   UI HELPERS
============================================================ */
function showAlert(id, message, type = 'error') {
  const el = document.getElementById(id);
  el.textContent = message;
  el.className = 'text-sm rounded-lg px-3 py-2 ' + (
    type === 'error'
      ? 'bg-red-50 text-red-700 border border-red-100'
      : 'bg-green-50 text-green-700 border border-green-100'
  );
  el.classList.remove('hidden');
}
function hideAlert(id) {
  document.getElementById(id).classList.add('hidden');
}
function setLoading(btn, loading, idleText) {
  btn.disabled = loading;
  const label = btn.querySelector('.btn-label');
  if (label) label.textContent = loading ? 'Please wait...' : idleText;
}
 
/* ============================================================
   SIGNUP
============================================================ */
document.getElementById('signupForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  hideAlert('signupAlert');
 
  const btn = document.getElementById('signupBtn');
  const payload = {
    user_name: document.getElementById('signupName').value.trim(),
    email: document.getElementById('signupEmail').value.trim(),
    password: document.getElementById('signupPassword').value
  };
 
  setLoading(btn, true, 'Sign Up');
  try {
    const res = await fetch(`${API_BASE}/signup`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'accept': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await res.json().catch(() => ({}));
 
    if (res.ok && data.succeeded) {
      showAlert('signupAlert', 'Account created! Redirecting to login...', 'success');
      // Pre-fill login form
      document.getElementById('loginEmail').value = payload.email;
      document.getElementById('loginPassword').value = payload.password;
      setTimeout(() => showView('login'), 1000);
    } else {
      showAlert('signupAlert', data.message || `Signup failed (${res.status})`);
    }
  } catch (err) {
    showAlert('signupAlert', 'Network error: ' + err.message);
  } finally {
    setLoading(btn, false, 'Sign Up');
  }
});
 
/* ============================================================
   LOGIN
============================================================ */
document.getElementById('loginForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  hideAlert('loginAlert');
 
  const btn = document.getElementById('loginBtn');
  const payload = {
    email: document.getElementById('loginEmail').value.trim(),
    password: document.getElementById('loginPassword').value
  };
 
  setLoading(btn, true, 'Log In');
  try {
    const res = await fetch(`${API_BASE}/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'accept': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await res.json().catch(() => ({}));
 
    if (res.ok && data.succeeded && data.data?.token) {
      saveAuth(data.data);
      enterChat();
    } else {
      showAlert('loginAlert', data.message || `Login failed (${res.status})`);
    }
  } catch (err) {
    showAlert('loginAlert', 'Network error: ' + err.message);
  } finally {
    setLoading(btn, false, 'Log In');
  }
});
 
/* ============================================================
   CHAT
============================================================ */
function enterChat() {
  const auth = loadAuth();
  if (!auth) { showView('login'); return; }
 
  document.getElementById('userBadge').textContent = `${auth.user_name || 'User'} · ${auth.email || ''}`;
  showView('chat');
  document.getElementById('chatInput').focus();
}
 
document.getElementById('logoutBtn').addEventListener('click', () => {
  clearAuth();
  // Reset chat UI
  document.getElementById('chatMessages').innerHTML = `
    <div class="max-w-3xl mx-auto text-center text-slate-400 text-sm py-12">
      <div class="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-gradient-to-br from-indigo-100 to-purple-100 text-indigo-600 mb-3">
        <svg xmlns="http://www.w3.org/2000/svg" class="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8">
          <path stroke-linecap="round" stroke-linejoin="round" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
        </svg>
      </div>
      <p class="font-medium text-slate-600">Start a conversation</p>
      <p class="text-xs mt-1">Ask anything to get going.</p>
    </div>`;
  document.getElementById('loginForm').reset();
  document.getElementById('signupForm').reset();
  showView('login');
});
 
document.getElementById('settingsBtn').addEventListener('click', () => {
  document.getElementById('settingsPanel').classList.toggle('hidden');
});
 
/* Auto-resize textarea */
const chatInput = document.getElementById('chatInput');
chatInput.addEventListener('input', () => {
  chatInput.style.height = 'auto';
  chatInput.style.height = Math.min(chatInput.scrollHeight, 128) + 'px';
});
/* Submit on Enter (Shift+Enter for newline) */
chatInput.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    document.getElementById('chatForm').requestSubmit();
  }
});
 
function clearEmptyState() {
  const messages = document.getElementById('chatMessages');
  const placeholder = messages.querySelector('.text-slate-400');
  if (placeholder) placeholder.parentElement.remove ? placeholder.remove() : null;
  // safer:
  const emptyContainer = messages.querySelector('.max-w-3xl.mx-auto.text-center');
  if (emptyContainer) emptyContainer.remove();
}
 
function escapeHtml(str) {
  return String(str)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;').replace(/'/g, '&#039;');
}
 
function appendMessage(role, content) {
  clearEmptyState();
  const messages = document.getElementById('chatMessages');
  const wrapper = document.createElement('div');
  wrapper.className = 'max-w-3xl mx-auto flex ' + (role === 'user' ? 'justify-end' : 'justify-start');
 
  const bubble = document.createElement('div');
  if (role === 'user') {
    bubble.className = 'bg-gradient-to-br from-indigo-600 to-purple-600 text-white px-4 py-2.5 rounded-2xl rounded-br-sm max-w-[80%] shadow-sm whitespace-pre-wrap break-words';
  } else if (role === 'error') {
    bubble.className = 'bg-red-50 text-red-700 border border-red-100 px-4 py-2.5 rounded-2xl rounded-bl-sm max-w-[80%] whitespace-pre-wrap break-words text-sm';
  } else {
    bubble.className = 'bg-white text-slate-800 border border-slate-200 px-4 py-2.5 rounded-2xl rounded-bl-sm max-w-[80%] shadow-sm whitespace-pre-wrap break-words';
  }
  bubble.innerHTML = escapeHtml(content);
  wrapper.appendChild(bubble);
  messages.appendChild(wrapper);
  messages.scrollTop = messages.scrollHeight;
  return wrapper;
}
 
function appendTyping() {
  clearEmptyState();
  const messages = document.getElementById('chatMessages');
  const wrapper = document.createElement('div');
  wrapper.className = 'max-w-3xl mx-auto flex justify-start';
  wrapper.id = 'typingIndicator';
  wrapper.innerHTML = `
    <div class="bg-white border border-slate-200 px-4 py-3 rounded-2xl rounded-bl-sm shadow-sm">
      <div class="typing"><span></span><span></span><span></span></div>
    </div>`;
  messages.appendChild(wrapper);
  messages.scrollTop = messages.scrollHeight;
}
function removeTyping() {
  const t = document.getElementById('typingIndicator');
  if (t) t.remove();
}
 
document.getElementById('chatForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const auth = loadAuth();
  if (!auth) { showView('login'); return; }
 
  const text = chatInput.value.trim();
  if (!text) return;
 
  const botId = document.getElementById('botIdInput').value.trim() || '2392982';
  const indexName = document.getElementById('indexNameInput').value.trim() || 'arz';
 
  appendMessage('user', text);
  chatInput.value = '';
  chatInput.style.height = 'auto';
 
  const sendBtn = document.getElementById('sendBtn');
  sendBtn.disabled = true;
  appendTyping();
 
  try {
    const res = await fetch(`${API_BASE}/chatbot-agent`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'accept': 'application/json',
        'Authorization': `Bearer ${auth.token}`
      },
      body: JSON.stringify({ query: text, bot_id: botId, index_name: indexName })
    });
    const data = await res.json().catch(() => ({}));
    removeTyping();
 
    if (res.status === 401) {
      appendMessage('error', 'Session expired. Please log in again.');
      setTimeout(() => { clearAuth(); showView('login'); }, 1200);
      return;
    }
 
    if (data.succeeded) {
      // The API spec didn't show a success payload shape — try common fields.
      const reply = data.data?.response || data.data?.answer || data.data?.message || data.response || data.message || JSON.stringify(data.data || data);
      appendMessage('bot', reply);
    } else {
      appendMessage('error', data.message || `Request failed (${res.status})`);
    }
  } catch (err) {
    removeTyping();
    appendMessage('error', 'Network error: ' + err.message);
  } finally {
    sendBtn.disabled = false;
    chatInput.focus();
  }
});
 
/* ============================================================
   INIT
============================================================ */
(function init() {
  const auth = loadAuth();
  if (auth?.token) enterChat();
  else showView('signup');
})();
</script>
</body>
</html>