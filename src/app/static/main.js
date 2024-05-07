async function fetchAndDisplayImages() {
    for (let x = 0; x < 20; x++) {
        const response = await fetch(`/history/images/${x}`);
        const image = await response.blob();
        const imageURL = URL.createObjectURL(image);
        const container = document.getElementById("graph" + (x + 1));
        console.log("graph" + (x + 1));
        if (container === null) {
            console.error(`Could not find container for image ${x}`);
        } else {
            container.src = imageURL;
        }
    }
}

window.onload = fetchAndDisplayImages;