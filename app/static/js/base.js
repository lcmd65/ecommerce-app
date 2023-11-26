function changeHeightClose() {
    const box = document.querySelector(".chat-box-container");
    // Check the current height and toggle between 400px and 25px
    // Check the current height and toggle between 400px and 25px
    box.style.height = "25px";
}

function changeHeightOpen() {
    const box = document.querySelector(".chat-box-container");
    // Check the current height and toggle between 400px and 25px
    box.style.height = "400px";
}

const clickHeightOpen = document.querySelector("chat-button-openbutton")
const clickHeightClose = document.querySelector("chat-button-closebutton")

clickHeightClose.addEventListener("click", changeHeightClose);
clickHeightOpen.addEventListener("click", changeHeightOpen);