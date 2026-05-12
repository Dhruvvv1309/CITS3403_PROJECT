let currentUserId = window.currentUserId;
let loggedInUserId = window.loggedInUserId;

/* ---------- SWITCH CHAT ---------- */
function openChat(id, name) {
    currentUserId = id;
    document.getElementById("chatName").innerText = name;
    loadMessages();
}

/* ---------- LOAD MESSAGES ---------- */
function loadMessages() {
    fetch(`/get_messages/${currentUserId}`)
    .then(res => res.json())
    .then(data => {
        const box = document.getElementById("chatMessages");
        box.innerHTML = "";

        data.forEach(m => {
            const div = document.createElement("div");

            // ✅ FIXED LOGIC
            if (m.sender === loggedInUserId) {
                div.className = "message sent";
            } else {
                div.className = "message received";
            }

            div.innerText = m.content;
            box.appendChild(div);
        });

        box.scrollTop = box.scrollHeight;
    });
}

/* ---------- SEND MESSAGE ---------- */
function sendMessage() {
    const input = document.getElementById("messageInput");
    const text = input.value.trim();

    if (!text) return;

    fetch('/send_message', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: `receiver_id=${currentUserId}&content=${encodeURIComponent(text)}`
    })
    .then(() => {
        input.value = "";
        loadMessages();
    });
}

/* ---------- AUTO REFRESH ---------- */
setInterval(loadMessages, 2000);

/* ---------- INIT ---------- */
loadMessages();