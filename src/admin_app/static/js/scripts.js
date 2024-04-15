const rowsPerPage = 20;
let currentPage = 1;
let totalRows = 0;
let totalPages = 0;


function getCollectionNameFromURL() {
    const pathSegments = window.location.pathname.split('/');
    // Assuming the collection name is the last part of the URL e.g. /dashboard/movies
    return pathSegments[pathSegments.length - 1];
}

function getUpdatedSearchParams(newParams) {
  const searchParams = new URLSearchParams(window.location.search);
  Object.keys(newParams).forEach(key => {
    searchParams.set(key, newParams[key]);
  });

  return searchParams;
}

function applySort() {
      const sort = document.getElementById('sort-field').value;
      const order = document.getElementById('sort-order').value;
      const collectionName = getCollectionNameFromURL();
      const newSearchParams = getUpdatedSearchParams({
          'sort': sort,
          'order': order
        });

      window.location.href = `/dashboard/${collectionName}?${newSearchParams.toString()}`;
}

function applyFilter() {
      const field = document.getElementById('filter-field').value;
      const operation = document.getElementById('filter-operation').value;
      const value = document.getElementById('filter-value').value;
      const collectionName = getCollectionNameFromURL();
      const newSearchParams = getUpdatedSearchParams({
          'field': field,
          'op': operation,
          'value': value
      });

      window.location.href = `/dashboard/${collectionName}?${newSearchParams.toString()}`;
}

document.addEventListener('DOMContentLoaded', (event) => {
  const searchParams = new URLSearchParams(window.location.search);

  // Set the sort field and order
  const sortField = searchParams.get('sort');
  const sortOrder = searchParams.get('order');
  if (sortField) document.getElementById('sort-field').value = sortField;
  if (sortOrder) document.getElementById('sort-order').value = sortOrder;

  // Set the filter field and operation
  const filterField = searchParams.get('field');
  const filterOperation = searchParams.get('op');
  const filterValue = searchParams.get('value');
  if (filterField) document.getElementById('filter-field').value = filterField;
  if (filterOperation) document.getElementById('filter-operation').value = filterOperation;
  if (filterValue) document.getElementById('filter-value').value = filterValue;
});


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
        const bodyRows = document.querySelectorAll('table tbody tr');
        totalRows = bodyRows.length;
        totalPages = Math.ceil(totalRows / rowsPerPage);

        bodyRows.forEach((row, index) => {
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

function loadCollection(collectionName) {
    window.location.href = '/dashboard/' + collectionName;
}

// Function to open the modal
function openModal() {
  const modal = document.getElementById("insertModal");
  modal.style.display = "block";
}

// Function to close the modal
function closeModal() {
  const modal = document.getElementById("insertModal");
  modal.style.display = "none";
}

// Function to submit the form
function submitForm() {
  const form = document.getElementById("insertForm");
  form.submit();
}

// Event listeners
document.addEventListener('DOMContentLoaded', (event) => {
    // When the insert button is clicked, open the modal
    document.getElementById("insert").addEventListener("click", openModal);

    // When the close button (x) is clicked, close the modal
    document.getElementById("form-close-btn").addEventListener("click", closeModal);

    // When the user clicks anywhere in the window
    window.addEventListener('click', function(event) {
        if (event.target.id === 'insertModal') {
            closeModal();
        }
    });

    document.getElementById("insertForm").addEventListener("submit", (event) => {
        event.preventDefault(); // Prevent the default form submit action
        submitForm(); // Call the function to submit the form
    });
});



