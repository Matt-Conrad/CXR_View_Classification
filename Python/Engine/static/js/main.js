cornerstoneWADOImageLoader.external.cornerstone = cornerstone;

// this function gets called once the user drops the file onto the div
function handleFileSelect(evt) {
    evt.stopPropagation();
    evt.preventDefault();

    // Get the FileList object that contains the list of files that were dropped
    const files = evt.dataTransfer.files;

    // this UI is only built for a single file so just dump the first one
    file = files[0];
    const imageId = cornerstoneWADOImageLoader.wadouri.fileManager.add(file);
    loadAndViewImage(imageId);
}

function handleDragOver(evt) {
    evt.stopPropagation();
    evt.preventDefault();
    evt.dataTransfer.dropEffect = 'copy'; // Explicitly show this is a copy.
}

// Setup the dnd listeners.
const dropZone = document.getElementById('dicomImage');
dropZone.addEventListener('dragover', handleDragOver, false);
dropZone.addEventListener('drop', handleFileSelect, false);

let loaded = false;
let payload;

function loadAndViewImage(imageId) {
    const element = document.getElementById('dicomImage');
    const start = new Date().getTime();
    cornerstone.loadImage(imageId).then(function (image) {
        console.log(image);
        const viewport = cornerstone.getDefaultViewportForImage(element, image);
        cornerstone.displayImage(element, image, viewport);
        if (loaded === false) {
            cornerstoneTools.mouseInput.enable(element);
            loaded = true;
        }

        function getTransferSyntax() {
            const value = image.data.string('x00020010');
            return value;
        }

        function getSopClass() {
            const value = image.data.string('x00080016');
            return value;
        }

        document.getElementById('transferSyntax').textContent = getTransferSyntax();
        document.getElementById('sopClass').textContent = getSopClass();
    }, function (err) {
        alert(err);
    });
}

const element = document.getElementById('dicomImage');
cornerstone.enable(element);

const filenameDisplay = document.getElementById('fileSelected');
const resultDisplay = document.getElementById('result');

function sendImage(payload) {
    let xhttp = new XMLHttpRequest();
    
    xhttp.open("POST", `http://${window.location.hostname}:80/api/classify`, true);
    xhttp.setRequestHeader("Content-Type", "application/octet-stream");
    
    xhttp.onreadystatechange = function () {
        if (this.readyState == XMLHttpRequest.DONE) {
            let letter = JSON.parse(this.responseText)["result"]
            resultDisplay.innerHTML = letter;
        }
    }

    xhttp.send(payload)
}

document.getElementById('selectFile').addEventListener('change', function (e) {
    // Add the file to the cornerstoneFileImageLoader and get unique
    // number for that file
    const file = e.target.files[0];
    filenameDisplay.setAttribute("placeholder", file.name);
    resultDisplay.innerHTML = "";

    let reader = new FileReader();
    reader.onload = function () {
        payload = this.result;
    }
    reader.readAsArrayBuffer(file);

    const imageId = cornerstoneWADOImageLoader.wadouri.fileManager.add(file);
    loadAndViewImage(imageId);
});

document.getElementById('sendFile').addEventListener('click', function (e) {
    if (loaded === true) {
        sendImage(payload)
    }
});