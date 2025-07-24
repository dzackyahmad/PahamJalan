const chatContainer = document.getElementById("chat-container");

function addMessage(text, isBot = false) {
  const msgWrapper = document.createElement("div");
  msgWrapper.className = `chat-message ${isBot ? "chatbot" : "user"}`;

  const avatar = document.createElement("img");
  avatar.src = isBot ? "bot.png" : "user.png";
  avatar.alt = isBot ? "Bot" : "User";
  avatar.className = "avatar";

  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.innerText = text;

  msgWrapper.appendChild(avatar);
  msgWrapper.appendChild(bubble);
  chatContainer.appendChild(msgWrapper);
  chatContainer.scrollTop = chatContainer.scrollHeight;
}

async function send() {
  const input = document.getElementById("question");
  const question = input.value.trim();
  if (!question) return;

  addMessage(question, false);
  input.value = "";

  addMessage("⏳ Sedang berpikir...", true);
  const allBubbles = document.querySelectorAll(".chatbot .bubble");
  const loadingBubble = allBubbles[allBubbles.length - 1];

  try {
    const res = await fetch("http://localhost:8000/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
    });
    const data = await res.json();
    loadingBubble.innerText = data.answer;
  } catch (err) {
    loadingBubble.innerText = "❌ Gagal mendapatkan jawaban.";
  }
}

function newChat() {
  chatContainer.innerHTML = "";
  addMessage("Selamat datang di PahamJalan! 👋\n\nSaya adalah chatbot hukum lalu lintas berbasis UU No. 22 Tahun 2009 dan peraturan terkait. Silakan tanyakan hal-hal seputar hukum lalu lintas Indonesia.", true);
}

function showAbout() {
  document.getElementById("about-modal").style.display = "block";
}

function closeAbout() {
  document.getElementById("about-modal").style.display = "none";
}

// Enter key triggers send
document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("question").addEventListener("keydown", function (e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      send();
    }
  });

  newChat();
});
