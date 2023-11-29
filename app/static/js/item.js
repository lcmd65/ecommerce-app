async function eventClickedItem(item_click) {
    const item = document.createElement("div");
    const workspace_container = document.querySelector(".main-workspace-container-header");

    item.classList.add("item-view-container");

    const item_id = document.createElement("p");
    item_id.classList.add("item-view-container-line")
    item_id.innerHTML = item_click.name;

    const item_description = document.createElement("p")
    const request = await fetch('/description_get', {
        method: ["POST"],
        header: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(item_click.description)
    });

    const respone = request.json()
    item_description.innerHTML = JSON.parse(respone)






    while (workspace_container.firstChild) {
        workspace_container.removeChild(workspace_container.firstChild);
    }

}