/* messages.js */

let activeUserId   = null;
let activeUserName = null;
let pollInterval   = null;
let lastMsgCount   = 0;

/* ═══════════════════════════════════════
   OPEN A CONVERSATION
═══════════════════════════════════════ */
function openConv(uid, uname) {
  activeUserId   = uid;
  activeUserName = uname;

  // Highlight sidebar item
  document.querySelectorAll('.conv-item').forEach(el => {
    el.classList.toggle('active', parseInt(el.dataset.uid) === uid);
  });

  // Update header
  document.getElementById('chatAvatar').textContent = uname[0].toUpperCase();
  document.getElementById('chatName').textContent   = uname;

  // Toggle panels
  document.getElementById('chatEmpty').classList.add('hidden');
  document.getElementById('chatActive').classList.remove('hidden');

  // Reset
  document.getElementById('chatMessages').innerHTML =
    '<div class="msgs-loading">Loading…</div>';
  document.getElementById('msgInput').value = '';

  // Load messages
  fetchMessages(uid);

  // Start polling every 3 s
  clearInterval(pollInterval);
  pollInterval = setInterval(() => fetchMessages(uid, true), 3000);
}

/* ═══════════════════════════════════════
   FETCH MESSAGES FROM API
═══════════════════════════════════════ */
function fetchMessages(uid, silent = false) {
  fetch(`/api/messages/${uid}`)
    .then(r => r.json())
    .then(data => {
      if (data.messages.length === lastMsgCount && silent) return;
      lastMsgCount = data.messages.length;
      renderMessages(data.messages);
    })
    .catch(() => {
      if (!silent) showToast('Could not load messages.');
    });
}

/* ═══════════════════════════════════════
   RENDER MESSAGES
═══════════════════════════════════════ */
function renderMessages(msgs) {
  const container = document.getElementById('chatMessages');
  if (!msgs.length) {
    container.innerHTML = '<div class="msgs-loading">No messages yet — say hello! ☕</div>';
    return;
  }

  let html      = '';
  let lastDate  = null;

  msgs.forEach(m => {
    // Date divider
    if (m.date !== lastDate) {
      html += `<div class="date-divider"><span>${m.date}</span></div>`;
      lastDate = m.date;
    }

    const side = m.sender_id === CURRENT_USER_ID ? 'sent' : 'received';
    html += `
      <div class="msg-row ${side}">
        <div class="bubble">
          ${escHtml(m.body)}
          <div class="bubble-time">${m.timestamp}</div>
        </div>
      </div>
    `;
  });

  container.innerHTML = html;
  container.scrollTop = container.scrollHeight;
}

/* ═══════════════════════════════════════
   SEND A MESSAGE
═══════════════════════════════════════ */
function sendMessage() {
  const input = document.getElementById('msgInput');
  const body  = input.value.trim();
  if (!body || !activeUserId) return;

  input.value    = '';
  input.disabled = true;

  fetch(`/api/messages/${activeUserId}/send`, {
    method:  'POST',
    headers: { 'Content-Type': 'application/json' },
    body:    JSON.stringify({ body }),
  })
    .then(r => r.json())
    .then(data => {
      input.disabled = false;
      input.focus();
      if (data.success) {
        fetchMessages(activeUserId);
        updateSidebarPreview(activeUserId, body);
      } else {
        showToast(data.error || 'Could not send message.');
      }
    })
    .catch(() => {
      input.disabled = false;
      showToast('Could not send message.');
    });
}

/* ═══════════════════════════════════════
   SIDEBAR PREVIEW UPDATE (optimistic)
═══════════════════════════════════════ */
function updateSidebarPreview(uid, body) {
  const item = document.querySelector(`.conv-item[data-uid="${uid}"]`);
  if (!item) return;
  const preview = item.querySelector('.conv-preview');
  const time    = item.querySelector('.conv-time');
  if (preview) { preview.textContent = body.substring(0, 60); preview.classList.remove('muted-italic'); }
  if (time)    { time.textContent = new Date().toTimeString().substring(0, 5); }
  // Remove fresh class so styling updates
  item.classList.remove('fresh');
}

/* ═══════════════════════════════════════
   SEARCH / FILTER
═══════════════════════════════════════ */
function filterConvs(q) {
  const lower = q.toLowerCase();
  document.querySelectorAll('.conv-item').forEach(el => {
    const name = (el.dataset.name || '').toLowerCase();
    el.style.display = name.includes(lower) ? '' : 'none';
  });
}

function filterModal(q) {
  const lower = q.toLowerCase();
  document.querySelectorAll('.picker-item').forEach(el => {
    const name = el.querySelector('.picker-name').textContent.toLowerCase();
    el.style.display = name.includes(lower) ? '' : 'none';
  });
}

/* ═══════════════════════════════════════
   NEW CONVERSATION MODAL
═══════════════════════════════════════ */
function openNewConvModal() {
  document.getElementById('newConvModal').classList.remove('hidden');
  document.getElementById('modalSearch').value = '';
  filterModal('');
  document.getElementById('modalSearch').focus();
}

function closeNewConvModal() {
  document.getElementById('newConvModal').classList.add('hidden');
}

function pickUser(uid, uname) {
  closeNewConvModal();
  openConv(uid, uname);
}

// Close modal on overlay click
document.getElementById('newConvModal').addEventListener('click', function(e) {
  if (e.target === this) closeNewConvModal();
});

/* ═══════════════════════════════════════
   TOAST
═══════════════════════════════════════ */
let toastTimer = null;
function showToast(msg) {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.classList.add('show');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => t.classList.remove('show'), 2600);
}

/* ═══════════════════════════════════════
   HELPERS
═══════════════════════════════════════ */
function escHtml(str) {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

/* Stop polling when tab is hidden */
document.addEventListener('visibilitychange', () => {
  if (document.hidden) {
    clearInterval(pollInterval);
  } else if (activeUserId) {
    pollInterval = setInterval(() => fetchMessages(activeUserId, true), 3000);
  }
});