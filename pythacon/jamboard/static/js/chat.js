let messageBox = document.querySelector(".input input");
let sendButt = document.querySelector(".input button");

sendButt.addEventListener("click", sendMessage);
messageBox.addEventListener("keyup", (e) => {
  if (e.keyCode === 13) {
    sendMessage();
  }
});

function sendMessage() {
  let message = messageBox.value;
  let data = {
    type: "chat",
    message: message,
    time: new Date().getHours() + ":" + new Date().getMinutes(),
  };
  if (message.length > 0) {
    chatSocket.send(
      JSON.stringify(data)
    );
    messageBox.value = "";
    addMessage(data)
  }
}

function addMessage(data) {
  let message = document.createElement("div");
  message.classList.add("message");
  message.innerHTML = `<div class="user">
    <div class="name">
      <span>John Doe</span>
      <span>${data.time}</span>
    </div>
    <div class="content">
      <p class="fullmsg">${data.message}</p>
    </div>
  </div>`;
  document.querySelector(".messages").appendChild(message);
}
