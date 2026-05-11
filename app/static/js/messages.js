let currentUser = "Dhruv";

const chats = {
    "Dhruv": [],
    "Winston": [],
    "Hadia": [],
    "Aarav": []
};

function openChat(name) {
    currentUser = name;
    document.getElementById("chatName").innerText = name;
    renderMessages();
}

function sendMessage() {
    const input = document.getElementById("messageInput");
    const text = input.value.trim();

    if (!text) return;

    chats[currentUser].push({ text, type: "sent" });

    // fake reply (for demo)
    setTimeout(() => {
        chats[currentUser].push({
            text: "Nice coffee choice ☕",
            type: "received"
        });
        renderMessages();
    }, 800);

    input.value = "";
    renderMessages();
}

function renderMessages() {
    const container = document.getElementById("chatMessages");
    container.innerHTML = "";

    chats[currentUser].forEach(msg => {
        const div = document.createElement("div");
        div.className = "message " + msg.type;
        div.innerText = msg.text;
        container.appendChild(div);
    });

    container.scrollTop = container.scrollHeight;
}