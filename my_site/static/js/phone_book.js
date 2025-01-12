// Відкриття діалогового вікна для вибору файлів
document.getElementById('uploadButton').addEventListener('click', function() {
    document.getElementById('file').click();  // Симулюємо клік на невидиме поле для файлів
});

// Автоматичне відправлення форми після вибору файлу
document.getElementById('file').addEventListener('change', function() {
    if (this.files.length > 0) {  // Перевіряємо, чи вибрано хоча б один файл
        document.getElementById('uploadForm').submit();  // Автоматична відправка форми
    }
});

// Сортування таблиці
document.getElementById("myTable").onclick = function (e) {
    if (e.target.tagName !== "TH") return

    let th = e.target;
    let colNum = th.cellIndex;
    let type = th.dataset.type;
    if (!type) return;

    let tbody = document.getElementById("myTable").querySelector("tbody");
    let rowsArray = Array.from(tbody.rows);

    let isAscending = th.dataset.order === "asc";
    th.dataset.order = isAscending ? "desc" : "asc";

    let getCellValue = (row, col) => row.cells[col]?.innerText || "";

    let compare =
        type === "number"
        ? (rowA, rowB) =>
            getCellValue(rowA, colNum) - getCellValue(rowB, colNum)
        : (rowA, rowB) =>
            getCellValue(rowA, colNum).toLowerCase()
            .localeCompare(getCellValue(rowB, colNum).toLowerCase());

    rowsArray.sort((rowA, rowB) => {
        let res = compare(rowA, rowB);
        return isAscending ? res : -res;
    });

    document.querySelectorAll("th").forEach(th => th.classList.remove("active"));
    th.classList.add("active");

    tbody.append(...rowsArray);
};

// Пошук у таблиці
function myFunction() {
    var filter = document.getElementById("myInput").value.toUpperCase();
    var rows = document.querySelectorAll("#myTable tbody tr");

    rows.forEach((row) => {
        var cellText = Array.from(row.cells)
            .map((cell) => cell.textContent || cell.innerText)
            .join(" ");
        row.style.display = cellText.toUpperCase().includes(filter) ? "" : "none";
    });
}

// Автоматичне закриття повідомлень
document.addEventListener("DOMContentLoaded", function () {
    setTimeout(function () {
        var alertList = document.querySelectorAll(".alert");
        alertList.forEach(function (alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000); // 5000 мілісекунд = 5 секунд
});
