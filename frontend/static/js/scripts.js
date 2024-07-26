// frontend/static/js/scripts.js

document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("file-upload").addEventListener("change", function(event) {
        document.getElementById("file-upload-label").innerHTML = event.target.files[0].name;
    });
});
