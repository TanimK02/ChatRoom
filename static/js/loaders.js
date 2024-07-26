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
