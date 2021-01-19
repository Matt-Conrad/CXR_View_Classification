const realFileBtn = document.getElementById("real-file");
const fileChooseBtn = document.getElementById("file-choose-button");
const sendBtn = document.getElementById("send-button");
const customTxt = document.getElementById("custom-text");

fileChooseBtn.addEventListener("click", function() {
    realFileBtn.click();
});

realFileBtn.addEventListener("change", function() {
    if (realFileBtn.value) {
        customTxt.innerHTML = realFileBtn.value.match(/[\/\\]([\w\d\s\.\-\(\)]+)$/)[1]; // Regex inside parentheses extracts the filename from the full path
        alert(customTxt.innerHTML);
    } else {
        customTxt.innerHTML = "No file chosen, yet.";
    }
});

