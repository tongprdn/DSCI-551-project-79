const rowsPerPage = 20;
let currentPage = 1;
let totalRows = 0;
let totalPages = 0;

function updateNavigationButtons() {
    document.getElementById('first-page').disabled = (currentPage === 1);
    document.getElementById('previous-page').disabled = (currentPage === 1);
    document.getElementById('next-page').disabled = (currentPage === totalPages);
    document.getElementById('last-page').disabled = (currentPage === totalPages);
}

document.addEventListener('DOMContentLoaded', (event) => {
    const rows = document.querySelectorAll('table tbody tr');
    totalRows = rows.length;
    totalPages = Math.ceil(totalRows / rowsPerPage);
    document.getElementById('total-pages').textContent = totalPages.toString();

    function displayRows() {
        const start = (currentPage - 1) * rowsPerPage;
        const end = start + rowsPerPage;
        rows.forEach((row, index) => {
            if (index >= start && index < end) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
        document.getElementById('current-page').textContent = currentPage.toString();
        updateNavigationButtons();
    }

    document.getElementById('first-page').addEventListener('click', () => {
        currentPage = 1;
        displayRows();
    });

    document.getElementById('previous-page').addEventListener('click', () => {
        if (currentPage > 1) {
            currentPage -= 1;
            displayRows();
        }
    });

    document.getElementById('next-page').addEventListener('click', () => {
        if (currentPage < totalPages) {
            currentPage += 1;
            displayRows();
        }
    });

    document.getElementById('last-page').addEventListener('click', () => {
        currentPage = totalPages;
        displayRows();
    });

    displayRows();

    document.getElementById('select-all').addEventListener('change', function(event) {
        let checkboxes = document.querySelectorAll('.select-item');
        checkboxes.forEach((checkbox) => {
            checkbox.checked = event.target.checked;
        });
    });
});
