const socket = io();
socket.on("connect", () => {
    console.log("Connected socket to the server"); 
})
socket.on("disconnect", () => {
    console.log("Disonnected from the server"); 
})

let recording = false
let file_name = "audio-1700563094.wav"

document.querySelector(".start-btn").addEventListener("click", () => {
    document.querySelector(".response-box").innerText = "Awaiting Response..."
    socket.emit("start-recording")
    setTimeout(function(){
        if(!recording)
            document.querySelector(".response-box").innerText = "Device doesn't seem to respond"
    }, 15000)
})

document.querySelectorAll(".audio-process").forEach(el => el.addEventListener("click", () => {
    document.querySelector(".audio-box").style.display = "block"
    file_name = el.id
    socket.emit("give-mel", {"file_name": file_name})
}));

document.querySelector(".noise-reduce .act-btn").addEventListener("click", () => {
    socket.emit("noise-reduce", {"file_name": file_name})
})

document.querySelector(".heart-beat .act-btn").addEventListener("click", () => {
    socket.emit("remove-hb", {"file_name": file_name})
})

document.querySelector(".classify .act-btn").addEventListener("click", () => {
    socket.emit("give-class", {"file_name": file_name})
})

socket.on("mel", (info) => {
    console.log(info.text)
    document.querySelector(".noise-reduce .before-img").src = info.image
})

socket.on("reduce-mel", (info) => {
    console.log(info.text)
    document.querySelector(".noise-reduce .after-img").src = info.image
})

socket.on("remove-hb-mel", (info) => {
    console.log(info.text)
    document.querySelector(".heart-beat .after-img").src = info.image
    document.querySelector(".audio-m").src = "{{ url_for('static', filename="+ file_name.slice(0,-4) + "_without_hb.wav" +") }}"
})

socket.on("take-class", (info) => {
    console.log(info.text)
    document.querySelector(".results").innerText = info.class
})

socket.on("message", (message) => {
    if(message.text == "Recording started..")
    recording = true
    document.querySelector(".response-box").innerText = message.text
})

socket.on("audio-file", (file) => {
    console.log(file.file_name)
    file_name = file.file_name
    socket.emit("add-file-to-user", {"file-name": file.file_name, "user": name})
})

function logout() {
    window.location.href = 'index.html';
}