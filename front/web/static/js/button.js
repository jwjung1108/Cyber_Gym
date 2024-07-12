document.addEventListener("DOMContentLoaded", function() {
    var showHintBtn = document.getElementById("show-hint-btn");
    var hint = document.getElementById("hint");

    showHintBtn.addEventListener("click", function() {
        if (hint.style.display === "none") {
            hint.style.display = "block";
            showHintBtn.textContent = "힌트 숨기기";
        } else {
            hint.style.display = "none";
            showHintBtn.textContent = "힌트 보기";
        }
    });
});