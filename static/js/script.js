const roomBtn = document.getElementById("room-btn")
const rxBtn = document.getElementById("RX-btn")
const roomDiv = document.getElementById("room-div")


const connect_to_server = () => {
    const socket = io();

    socket.on('connect', () => {
        
    });
}

rxBtn.addEventListener("click", () => {
    roomDiv.style.display = "none";
})

roomBtn.addEventListener("click", () => {
    roomDiv.style.display = "grid";
})