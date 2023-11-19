    document.addEventListener("DOMContentLoaded", function() {
        let table1 = document.getElementById("table1");
        let table2 = document.getElementById("table2");
        let table3 = document.getElementById("table3");

        window.show1 = function() {
            table1.style.display = "block";
            table2.style.display = "none";
            table3.style.display = "none";
            alert("Таблица 1");
        }

        window.show2 = function() {
            table1.style.display = "none";
            table2.style.display = "block";
            table3.style.display = "none";
            alert("Таблица 2");
        }

        window.show3 = function() {
            table1.style.display = "none";
            table2.style.display = "none";
            table3.style.display = "block";
            alert("Таблица 3");
        }
    });
