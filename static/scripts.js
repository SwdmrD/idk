document.addEventListener("DOMContentLoaded", function() {
    const table1Button = document.getElementById("table1-btn");
    const table2Button = document.getElementById("table2-btn");
    const table3Button = document.getElementById("table3-btn");
    const table1 = document.getElementById("table1");
    const table2 = document.getElementById("table2");
    const table3 = document.getElementById("table3");

    table1Button.addEventListener("click", function() {
        table1.style.display = "block";
        table2.style.display = "none";
        table3.style.display = "none";
    });

    table2Button.addEventListener("click", function() {
        table1.style.display = "none";
        table2.style.display = "block";
        table3.style.display = "none";
    });
     table3Button.addEventListener("click", function() {
        table1.style.display = "none";
        table2.style.display = "none";
        table3.style.display = "block";
    });
});
