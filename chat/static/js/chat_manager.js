

function getCurrentTime() {
    const now = new Date();
    return now;
}
//not working :(
function getChatTime(ChatDate) {
    now = getCurrentTime();
    const instant = new Temporal.Instant(ChatDate);
    const zonedDateTime = instant.toZonedDateTime("America/New_York");

    dt = ZonedDateTime.toPlainDateTime().toJSDate();
    aux = now - dt;
    return aux.getMinutes();
}

//this will refresh the Chats on the sidebar
async function refreshChat(chats) {
    request = await fetch("get_chats/");
    chats = await request.json()
    if (chats.succeded == "yes") {

        chatContainer.innerHTML = "";
        Array.from(chats.chats).reverse().forEach(chat => {
            chatB = document.createElement("div");
            chatB.classList = "sidebar-chats chat-button "
            chatB.innerHTML = `
                    <div class="chat-item notactive">
                    <div class="d-flex justify-content-between">
                        <strong>${chat.title}</strong>
                        <span class="time">${chat.created_humanized}</span>
                    </div>
                    <p class="mb-0 text-truncate">${chat.subtitle}</p>
                    </div>
                `
            chatB.id = `chat:${chat.id}`

            chatContainer.appendChild(chatB);


        })
        chts = chatContainer.children
        Array.from(chts).forEach(chatB => {
            chatB.addEventListener("click", async () => {
                id = chatB.id.split(":")[1];

                idChat = document.getElementById("chatID");
                idChat.value = `${id}`;

                response = await fetch(`./load_chat/${id}`);
                loadedChat = await response.json();
                Array.from(chts).forEach(x => {
                    x.children[0].classList.replace("active", "notactive")
                });
                chatB.children[0].classList.replace("notactive", "active")
                refreshMessages(loadedChat);
            });
            chts[0].click()

        });
    }
}

function refreshMessages(messages) {
    messagesDiv.innerHTML = " ";
    if (messages.succeded == "yes") {
        messages.messages.forEach(message => {
            messagesDiv.innerHTML += `<h3 class="message message-user">${message.message}</h3>`
            messagesDiv.innerHTML += `<h3 class="message message-bot ">${message.response}</h3>`


        });
    } else {
        messagesDiv.innerHTML += `<h1 id="noMessagesMessage">No messages yet</h1>`;
    }
};



const sendMessage = async (evt) => {

    rompt = document.getElementById("prompt");

    if (rompt.value != "") {
        const input = document.getElementById('messageInput');
        const formDt = new FormData(input)
        if (formDt) {
            const userMessage = document.createElement('h3');
            userMessage.className = 'message message-user';
            userMessage.innerHTML = `${formDt.get("prompt")}`;
            if (document.getElementById('messagesDiv').children[0].isSameNode(document.getElementById("noMessagesMessage"))) {
                document.getElementById('messagesDiv').children[0].remove()
            }
            document.getElementById('messagesDiv').appendChild(userMessage);


            const botMessage = document.createElement('h3');
            botMessage.className = 'message message-bot';
            botMessage.innerHTML = `...`;
            document.getElementById('messagesDiv').appendChild(botMessage);

            document.getElementById('messagesDiv').lastChild.scrollIntoView({ behavior: "smooth" });

            rompt.value = '';
            console.log(formDt.get("Chat_ID"))
            if(formDt.Chat_ID!="-1"){
            resp = await fetch("send/", {
                method: "POST",
                body: formDt
            })}
            else{
                alert("You must first create a chat")
            }

            jsonresp = await resp.json()
            botMessage.innerHTML = `${jsonresp.response}`

        }


    } else {
        alert("Write a message first")
    }
}
const chat_loader = async () => {


    refreshChat()



    var chats = document.querySelectorAll(".chat-button");

    if (chats.length > 0) {
        chats[0].click();
    } else {
        chatContainer.innerHTML = `<h3>Start a new chat</h3>`;
        messagesDiv.innerHTML += `<h1 id="noMessagesMessage">Create a chat first</h1>`;
    }

    createChat.addEventListener("click", async () => {

        x = await fetch("new_chat/");
        x = x.json()

        console.log(x)
        refreshChat()

    })

    const sidebar = document.getElementById('sidebar');
    const sidebarToggle = document.getElementById('sidebarToggle');
    const overlay = document.getElementById('overlay');

    sidebarToggle.addEventListener('click', function () {
        sidebar.classList.toggle('active');
        overlay.classList.toggle('active');
    });

    overlay.addEventListener('click', function () {
        sidebar.classList.remove('active');
        overlay.classList.remove('active');
    });

}
messageInput.addEventListener('submit', (evt) => {
    evt.preventDefault();
    sendMessage()
})


window.addEventListener("load", async () => {

    await chat_loader();

})
