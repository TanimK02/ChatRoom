// Define DOM Elements
const roomBtn = document.getElementById("room-btn");
const rxBtn = document.getElementById("RX-btn");
const roomDiv = document.getElementById("room-div");
const joinBtn = document.getElementById("JR-btn");
const sendBtn = document.getElementById("send-btn");
const messageInput = document.getElementById("message");
const msgList = document.getElementById("msg-list");
const myRoomList = document.getElementById("my-rooms-list");
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
const prev = document.getElementById("prev");
const next = document.getElementById("next");
const prevNext = document.getElementById("prev-next");
const mrBtn = document.getElementById("MR-button");
const myRms = document.getElementById("my-rooms");
const myRmsXbtn = document.getElementById("my-rooms-x-button");
const socket = io();
let server = "";

// Utility Functions
const clearMsg = () => {
    msgList.innerHTML = "";
};

const sendMessage = () => {
    if (messageInput.value !== "") {
        socket.emit("message_json", { "message": messageInput.value, "room": server });
        messageInput.value = "";
    }
};

const loadInRooms = (result) => {
    roomList.innerHTML = "";
    result.forEach((room) => {
        const li = document.createElement("li");
        const el = document.createElement("button");
        el.textContent = `${room.name} ${room.password ? `Users:` : 'Visits'} ${room.people}`;
        li.appendChild(el);
        roomList.appendChild(li);
        el.addEventListener("click", () => {
            joinerDiv.display = "none";
            joinerDiv.innerHTML = `
                <p><button id="join-x">X</button></p>
                <h2>${room.name}</h2>
                ${room.password ? `<input name="password" id="password" type="text" placeholder="password"/>` : ""}
                <input type="button" id="join-submit" value="join"/>`;
            joinerDiv.querySelector("#join-x").addEventListener("click", () => {
                joinerDiv.style.display = "none";
                joinerDiv.innerHTML = "";
            });
            joinerDiv.querySelector("#join-submit").addEventListener("click", () => {
                socket.emit('leave', { "room": server });
                clearMsg();
                socket.emit("join", {
                    "room": `${room.name}`,
                    "password": joinerDiv.querySelector("#password") ? (joinerDiv.querySelector("#password").value ? joinerDiv.querySelector("#password").value : "") : ""
                });
            });
            joinerDiv.style.display = "flex";
        });
    });
    return true;
};

const pageRooms = async (number) => {
    const response = await fetch(`/rooms/${number}`);
    console.log(`/rooms/${number}`);
    const result = await response.json();
    if (result.length == 0) {
        next.disabled = true;
        prev.click();
        next.disabled = false;
    }
    if (loadInRooms(result)) {
        loaded = true;
    }
};

const loadMyRooms = (result) => {
    myRoomList.innerHTML = "";
    result.forEach((room) => {
        const li = document.createElement("li");
        const el = document.createElement("button");
        el.textContent = `${room.name} ${room.password ? `Users:` : 'Visits'} ${room.people}`;
        li.appendChild(el);
        myRoomList.appendChild(li);
        el.addEventListener("click", () => {
            joinerDiv.display = "none";
            joinerDiv.innerHTML = `
                <p><button id="join-x">X</button></p>
                <h2>${room.name}</h2>
                <input type="button" id="join-submit" value="join"/>
                <input type="button" id="room-delete" value="delete" />`;
            joinerDiv.querySelector("#join-x").addEventListener("click", () => {
                joinerDiv.style.display = "none";
                joinerDiv.innerHTML = "";
            });
            joinerDiv.querySelector("#join-submit").addEventListener("click", () => {
                socket.emit('leave', { "room": server });
                clearMsg();
                socket.emit("join", {
                    "room": `${room.name}`,
                });
            });
            joinerDiv.querySelector("#room-delete").addEventListener("click", async() => {
                try{
                    const response = await fetch(`/delete_room/${room.id}`);
                    if (response.ok) {
                        console.log('Delete successful.');
                        joinerDiv.querySelector("#room-delete").disabled = true;
                        li.remove();
                        el.remove();
                        joinerDiv.style.display = "none";
                        if (roomName.textContent == room.name){
                            roomName.textContent = "Join A Room";
                            msgList.innerHTML = "";
                        }
                    } else {
                        console.error("Unsuccessful.")
                        alert("failed")
                    }}
                catch (error) {
                    console.error({"Error": error});
                }
            });

            joinerDiv.style.display = "flex";
        });
    });
};


const getMyRooms = async () => {
    const response = await fetch(`/my_rooms`);
    const result = await response.json();
    loadMyRooms(result);
}

// Socket Event Handlers
socket.on('connect', () => {
    console.log("connected");
});

socket.on("message_json", (data) => {
    console.log("received");
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

socket.on('join', (data) => {
    if (data["room"]) {
        roomName.textContent = data["room"];
        joinerDiv.style.display = 'none';
        server = data["channel"];
        console.log(data);
    } else {
        roomName.textContent = "Join A Room";
        joinerDiv.querySelectorAll(".errors").forEach(el => el.remove());
        const error = document.createElement("p");
        error.textContent = "Failed to join room";
        error.classList.add("errors");
        joinerDiv.querySelector("h2").insertAdjacentElement("afterend", error);
    }
});

// DOM Event Listeners
rxBtn.addEventListener("click", () => {
    roomDiv.style.display = "none";
});

roomBtn.addEventListener("click", () => {
    roomDiv.style.display = roomDiv.style.display == "flex" ? "none" : "flex";
});

prev.addEventListener("click", () => {
    const p = prevNext.querySelector("p");
    if (p.textContent == 1) {
        pageRooms(1);
        return;
    } else {
        p.textContent = parseInt(p.textContent) - 1;
        pageRooms(parseInt(p.textContent));
        return;
    }
});

next.addEventListener("click", () => {
    if (roomList.querySelectorAll("li").length < 10) {
        return;
    }
    const p = prevNext.querySelector("p");
    p.textContent = parseInt(p.textContent) + 1;
    pageRooms(parseInt(p.textContent));
    return;
});

joinBtn.addEventListener("click", () => {
    rooms.style.display = rooms.style.display == "block" ? "none" : "block";
    pageRooms(1);
});

sendBtn.addEventListener("click", sendMessage);

messageInput.addEventListener("keydown", (event) => {
    if (event.key == "Enter") {
        sendMessage();
    }
});

roomsContainerXBtn.addEventListener("click", () => {
    rooms.style.display = "none";
});

createBtn.addEventListener("click", () => {
    roomCreatorDiv.style.display = roomCreatorDiv.style.display == "block" ? "none" : "block";
});

preventForm.addEventListener("click", (event) => {
    event.preventDefault();
    roomCreatorDiv.style.display = "none";
});

roomForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const response = await fetch('/room/create', {
        method: "POST",
        body: new FormData(roomForm)
    });
    const result = await response.json();
    if (result.room) {
        socket.emit('leave', { "room": server });
        clearMsg();
        socket.emit("join", { "room": `${roomForm.name.value}`, "password": roomForm.password.value ? roomForm.password.value : "" });
        roomName.textContent = roomForm.name.value;
        roomCreatorDiv.style.display = "none";
        getMyRooms();
    } else {
        document.querySelectorAll(".errors").forEach((el) => {
            el.remove();
        });
        const error = document.createElement("p");
        error.textContent = result["error"];
        error.classList.add("errors");
        createh2.insertAdjacentElement('afterend', error);
    }
});

mrBtn.addEventListener("click", () => {
    myRms.style.display = myRms.style.display == "block" ? "none" : "block";
    getMyRooms();
});

myRmsXbtn.addEventListener("click", () => {
    myRms.style.display = myRms.style.display == "block" ? "none" : "block";
});
