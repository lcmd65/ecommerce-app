function changeHeightClose() {
    const box = document.querySelector(".chat-box-container");
    // Check the current height and toggle between 400px and 25px
    // Check the current height and toggle between 400px and 25px
    if (box.clientHeight === 400) {
        box.style.height = "25px";
    }
}

function changeHeightOpen() {
    const box = document.querySelector(".chat-box-container");
    // Check the current height and toggle between 400px and 25px
    if (box.clientHeight === 25) {
        box.style.height = "400px";
    }
}