window.addEventListener("load", function() {
    const buttonclick = document.querySelector('.button-link-app');
    buttonclick.addEventListener('click', async function() {
        await fetch('/intro', {
                method: 'GET',
            })
            .then(response => response.text())
            .then(data => {
                // Assuming the response is HTML, you can replace the current page content
                document.documentElement.innerHTML = data;
            })
            .catch(error => console.error('Error:', error));
    });
});