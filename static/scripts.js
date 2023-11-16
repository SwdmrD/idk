document.addEventListener("DOMContentLoaded", function() {
    const table1Button = document.getElementById("table1-btn");
    const table1 = document.getElementById("table1");


    table1Button.addEventListener("click", function() {
        table1.style.display = "block";
    });
});
