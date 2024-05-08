async function fetchAndDisplayGraphs() {
    for (let x = 0; x < 20; x++) {
        // get data from server
        const txtResponse = await fetch(`/history/${x}`);
        // check if we got a 404
        if (txtResponse.status === 404) {
            // if we did, we can stop here because that means we reached the end of the history
            break;
        }
        const txtResponseJson = await txtResponse.json();
        const imgResponse = await fetch(`/history/images/${x}`);
        if (imgResponse.status === 404) {
            // This should never happen, because the image should always be there if the text is there
            console.error(`An error occured when letting the server generate the image for graph ${x}`);
        }
        const image = await imgResponse.blob();
        const imageURL = URL.createObjectURL(image);

        // display data
        // get the cell
        const cell = document.getElementById("graph" + (x + 1));
        if (cell === null) {
            console.error(`Could not find cell for image ${x}`);
            continue;
        }
        // update text
        if (txtResponseJson.success) {
            const txtContainer = cell.querySelector("p");
            if (txtContainer === null) {
                console.error(`Could not find container for text ${x}`);
                continue;
            } else {
                txtContainer.innerHTML = txtResponseJson.graphString;
            }
        }
        // update image
        const imgContainer = cell.querySelector("img");
        if (imgContainer === null) {
            console.error(`Could not find container for image ${x}`);
            continue;
        } else {
            imgContainer.src = imageURL;
        }
    }
}

function ChangeStatus(status) {
    var statusElement = document.getElementById("status");
    statusElement.innerHTML = status;
}

window.onload = fetchAndDisplayGraphs;

document.addEventListener("DOMContentLoaded", function() {
    // handle form submit
    document.getElementById('graphForm').addEventListener('submit', function(event) {
        event.preventDefault();

        var input1 = document.getElementById('orderInput').value;
        var input2 = document.getElementById('filterInput').value;
        var input3 = document.getElementById('minDegreeInput').value;

        ChangeStatus("Handling request...");

        fetch('/filter', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ "order": input1, "filter": input2, "minDegree": input3 }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                ChangeStatus("Success");
                // fetch and display new graphs
                fetchAndDisplayGraphs();
            } else {
                console.error('Error processing request');
                ChangeStatus("Error processing request");
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    });
});