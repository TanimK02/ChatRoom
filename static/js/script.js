
const roomBtn = document.getElementById("room-btn");
const rxBtn = document.getElementById("RX-btn");
const roomDiv = document.getElementById("room-div");
const joinBtn = document.getElementById("JR-btn");
const sendBtn = document.getElementById("send-btn");
const messageInput = document.getElementById("message");
const msgList = document.getElementById("msg-list");
const rooms = document.getElementById("rooms-container");
const roomsContainerXBtn = document.getElementById("rooms-container-x-button");
const roomCreatorDiv = document.getElementById("room-creator-div");
const createBtn = document.getElementById("CM-btn");
const preventForm = document.getElementById("rooms-creator-x-button");
const roomName = document.getElementById("room-name");
const roomForm = document.getElementById("room-creator-form");
const createh2 = document.getElementById("create-h2");
const roomList = document.getElementById("room-list");
const joinerDiv = document.getElementById("joiner-div");
const socket = io();
let server = "";


const clearMsg = () => {
    msgList.innerHTML = "";
}

const sendMessage = () => {
    if (messageInput.value !== ""){
        socket.emit("message_json", {"message": messageInput.value, "room": server})
        messageInput.value = "";}
};

socket.on('connect', () => {
    console.log("connected");
});

socket.on("message_json", (data) => {
    console.log("recieved");
    const msg = document.createElement("li");
    if (data.img) {
        const img = document.createElement("img");
        img.src = data.img;
        msg.appendChild(img);
    }
    msg.textContent = data["message"];
    msgList.appendChild(msg);
    msg.scrollIntoView({ behavior: 'smooth', block: 'end' });
});

socket.on('join', (data)=> {
    if (data) {
        roomName.textContent = data;
        joinerDiv.style.display = 'none';
        server = data;
        console.log(data);
    } else {
        const error = document.createElement("p");
        error.textContent = "Failed to join room";
        error.classList.add("errors");
        joinerDiv.querySelector("h2").insertAdjacentElement("afterend", error);
    }
});

rxBtn.addEventListener("click", () => {
roomDiv.style.display = "none";
});

roomBtn.addEventListener("click", () => {
roomDiv.style.display = "flex";
});


let roomPg = 1;
let loaded = false;
joinBtn.addEventListener("click", async () => {
rooms.style.display = "block";
if (loaded) {
    return
}
const response = await fetch (`/rooms/${roomPg}`);
const result = await response.json();
result.forEach((room) => {
    const li = document.createElement("li");
    const el = document.createElement("button");
    el.textContent = `${room.name} Visits: ${room.people}`;
    li.appendChild(el);
    roomList.appendChild(li);
    loaded = true;
    el.addEventListener("click", () => {
        joinerDiv.display = "none";
        joinerDiv.innerHTML = `
                    <p><button id="join-x">X</button></p>
                    <h2>${room.name}</h2>
                    ${room.password? `<input name="password" id="password" type="text" placeholder="password"/>`: ""}
                    <input type="button" id="join-submit" value="join"/>`
        joinerDiv.querySelector("#join-x").addEventListener("click", ()=> {
            joinerDiv.style.display = "none";
            joinerDiv.innerHTML = "";
        })
        joinerDiv.querySelector("#join-submit").addEventListener("click", () => {
            socket.emit('leave', {"room" : server});
            clearMsg();
            socket.emit("join", {"room": `${room.name}`, "password": 
                joinerDiv.querySelector("#password")? ((joinerDiv.querySelector("#password").value? joinerDiv.querySelector("#password").value : "")) : "" });
        })
        joinerDiv.style.display = "flex";
        
    })
})
});



sendBtn.addEventListener("click", sendMessage);

messageInput.addEventListener("keydown", (event) => {
    if (event.key == "Enter") {
        sendMessage();
    }
} )

roomsContainerXBtn.addEventListener("click", ()=> {
    rooms.style.display = "none"
})

createBtn.addEventListener("click", () => {
    roomCreatorDiv.style.display = "block";
})

preventForm.addEventListener("click", (event) => {
    event.preventDefault();
    roomCreatorDiv.style.display = "none";
})

roomForm.addEventListener("submit", async (event)=> {
    event.preventDefault();
    const response = await fetch('/room/create', {
        method: "Post",
        body: new FormData(roomForm)
    })
    const result = await response.json()
    if (result.room) {
        socket.emit('leave', {"room" : server});
        clearMsg();
        socket.emit("join", {"room": `${roomForm.name.value}`, "password": roomForm.password.value? roomForm.password.value : "" });
        roomName.textContent = roomForm.name.value;
        roomCreatorDiv.style.display = "none";
    }
    else {
        const error = document.createElement("p");
        error.textContent = result["error"];
        error.classList.add("errors");
        createh2.insertAdjacentElement('afterend', error);
    }
})

