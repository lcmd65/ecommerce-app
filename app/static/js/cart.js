async function eventClickedCard() {
    const message = await fetch("/card", method = ["GET"]);
    const respone = await message.json()

    const cart = document.createElement("div")
    cart.classList.add("card-container")


}

const cartIcon = document.querySelector("#card-icon");
cartIcon.addEventListener("click", eventClickedCard);