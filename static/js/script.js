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
const channelList = document.getElementById("channels-list");
const channelAdd = document.getElementById("add-channel");
const createChBtn = document.getElementById("create-ch");
const edChBtn = document.getElementById("edit-ch");
const edChDiv = document.getElementById("ed-channel");
const mobileCh = document.getElementById("mobile-ch");
const socket = io();
let server = "";
let roomId = "";
let admin = false;
let chatPage = 1;
let canScroll = true;

// Utility Functions

const getCSRFToken = () => {
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
};

const clearMsg = () => {
    msgList.innerHTML = "";
    chatPage = 1;
    canScroll = true;
};

const leaveRC = () => {
    socket.emit('leave', { "room": server });
    socket.emit('leave', { "room": roomId });
};

const leaveNcLear = () => {
    leaveRC();
    clearMsg();
    clearChs();
    createChBtn.disabled = true;
    edChBtn.disabled = true;
};

const clearChs = () => {
    channelList.querySelectorAll("li").forEach(element => {
        if (!element.classList.contains(".necessary")) {
            element.remove();
        };
            
    })
};

const sendMessage = () => {
    if (messageInput.value !== "") {
        socket.emit("message", { "message": messageInput.value, "channel": server });
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
                <h2></h2>
                ${room.password ? `<input name="password" id="password" type="text" placeholder="password"/>` : ""}
                <input type="button" id="join-submit" value="join"/>`;
            joinerDiv.querySelector("h2").textContent = room.name;
            joinerDiv.querySelector("#join-x").addEventListener("click", () => {
                joinerDiv.style.display = "none";
                joinerDiv.innerHTML = "";
            });
            joinerDiv.querySelector("#join-submit").addEventListener("click", () => {
                leaveNcLear()
                socket.emit("join", {
                    "room": `${room.id}`,
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
                <h2></h2>
                <input type="button" id="join-submit" value="join"/>
                <input type="button" id="room-delete" value="delete" />`;
            joinerDiv.querySelector("h2").textContent = room.name;
            joinerDiv.querySelector("#join-x").addEventListener("click", () => {
                joinerDiv.style.display = "none";
                joinerDiv.innerHTML = "";
            });
            joinerDiv.querySelector("#join-submit").addEventListener("click", () => {
                leaveNcLear()
                socket.emit("join", {
                    "room": `${room.id}`,
                });
            });
            joinerDiv.querySelector("#room-delete").addEventListener("click", async() => {
                leaveNcLear()
                try{
                    const csrfToken = getCSRFToken();
                    const response = await fetch(`/delete_room/${room.id}`,
                        {headers: {'X-CSRFToken': csrfToken}}
                    );
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
};

const loadChannels = (result) => {
    clearChs();
    result.forEach((channel) => {
        const li = document.createElement("li");
        const el = document.createElement("button");
        el.textContent = `${channel.name.toUpperCase()}`;
        li.appendChild(el);
        channelList.appendChild(li);
        el.addEventListener("click", () => {
            socket.emit('leave', { "room": server });
            clearMsg();
            socket.emit("join", {
                "room": `${channel.room_id ? channel.room_id : roomId}`,
                "channel_id": `${channel.id}`
            });
            edChDiv.querySelector("h1").textContent = channel.name.toUpperCase();
        })
    } )
};

const getChannels = async () => {
    const response = await fetch(`/load_channels/${roomId}`);
    const result = await response.json();
    loadChannels(result);
};

const addChannel = async() => {
    const name = channelAdd.querySelector("input").value;
try {
    const csrfToken = getCSRFToken();
    const response = await fetch('/create_channel', {
        method: "POST",
        headers: {
            "X-CSRFToken": csrfToken,
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ "room": roomId, "name": name })
    });

    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();

} catch (error) {
    console.error('Fetch error:', error);
    createChBtn.disabled = true;
    channelAdd.style.display = "none";
}

}

const openMChannels = () => {
    if (channelList.querySelectorAll(".close").length == 0){
    const close = document.createElement("button");
    close.textContent = "Close Window";
    close.style.backgroundColor = "red";
    close.style.color = "white";
    close.classList.add("close", "necessary");
    close.addEventListener("click", () => {
        channelList.style.display = "none";
    });
    channelList.prepend(close);
    close.style.height = "50px";
    close.style.width = "100%";};
    channelList.style.display = "flex";
    channelList.style.flexDirection = "column";
    channelList.style.alignItems = "center";
    channelList.style.position = "absolute";
    channelList.style.top = "0";
    channelList.style.left = "0";
    channelList.style.zIndex = "999";
    channelList.style.width = "100%";
    channelList.style.height = "100%";

};

// Socket Event Handlers
socket.on('connect', () => {
    console.log("connected");
});

socket.on("load_prev", (data) => {
    if (data.length == 0) {
        canScroll = false;
        return;
    };
    let first;
    data.forEach(messageData => {
        try{
            messageData = JSON.parse(messageData)}
        catch {
        }
        const msg = document.createElement("li");
        if (!first) {
            first = msg;
        };
        if (messageData.img) {
            const img = document.createElement("img");
            img.src = messageData.img;
            msg.appendChildChild(img);
        }
        msg.textContent = messageData["username"] + ": " + messageData["text"];
        msgList.prepend(msg);
        });
        first.scrollIntoView({ behavior: 'smooth', block: 'end'})
    }
    
    );

socket.on("message", (data) => {
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
        server = data["channel_id"];
        roomId = data["room_id"];
        admin = data["admin"];
        createChBtn.disabled = admin? false : true;
        edChBtn.disabled = admin? false : true;
        getChannels();
        if (channelList.querySelector(".close")) {
            channelList.style.display = "none";
        }
    } else {
        roomName.textContent = "Join A Room";
        joinerDiv.querySelectorAll(".errors").forEach(el => el.remove());
        const error = document.createElement("p");
        error.textContent = "Failed to join room";
        error.classList.add("errors");
        joinerDiv.querySelector("h2").insertAdjacentElement("afterend", error);
        clearChs();
    }
});

socket.on('channels_update', (result) => loadChannels(result));

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
    if (result.room_name) {
        leaveNcLear()
        socket.emit("join", { "room": `${result.room_id}`, "password": roomForm.password.value ? roomForm.password.value : "" });
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

channelAdd.querySelector("#channel-add-btn").addEventListener("click", addChannel);

createChBtn.addEventListener("click", () => {
    channelAdd.style.display = channelAdd.style.display == "flex" ? "none" : "flex";
})

channelAdd.querySelector(".add-channel-h").querySelector("button").addEventListener("click",() => {channelAdd.style.display = "none"});

edChBtn.addEventListener("click", () => {
    edChDiv.style.display = edChDiv.style.display == "flex" ? "none" : "flex";
})

edChDiv.querySelector(".ed-x").addEventListener("click", ()=> edChDiv.style.display="none");

edChDiv.querySelector("#ch-name-btn").addEventListener("click", async() => {
    const new_name = edChDiv.querySelector("#new-name").value;
    if (new_name !== ""){
        const csrfToken = getCSRFToken();
        try {
            const response = await fetch("/edit_channel", {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken,
            },
            body: JSON.stringify({ "room": roomId, "channel_id": server, "new_name": new_name})
            
        });
        if (response.ok) {
            edChDiv.querySelector("h1").textContent = new_name.toUpperCase();
        };
    }
    catch (error) {
        console.error("400 Channel name change didn't work.");
    };
       
    };
});

edChDiv.querySelector("#ch-delete-btn").addEventListener("click", async() => {
    try {
        const csrfToken = getCSRFToken();
        const response = await fetch("/delete_channel", {
        method: "Delete",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,
        },
        body: JSON.stringify({ "room": roomId, "channel_id": server})
    });
    if (response.ok) {
        edChDiv.style.display = "none";
    } else {
        alert("Can't delete if only channel.")
    };
}
    catch (error) {
        console.error("error", error);
    };
})

msgList.addEventListener("scroll", () => {
    if (msgList.scrollTop <= 0 && canScroll) {
        socket.emit("load_prev", {"page": chatPage, "channel_id": server});
        chatPage += 1;
    };;
});

mobileCh.addEventListener("click", ( () => {
    if (roomId) {
        openMChannels()
    };
}
));