const rowsPerPage = 20;
let currentPage = 1;
let totalRows = 0;
let totalPages = 0;


function getCollectionNameFromURL() {
    const pathSegments = window.location.pathname.split('/');
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
    const sortField = searchParams.get('sort');
    const sortOrder = searchParams.get('order');

    if (sortField) document.getElementById('sort-field').value = sortField;
    if (sortOrder) document.getElementById('sort-order').value = sortOrder;

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

    function loadMoreData() {
        const currentUrlParams = new URLSearchParams(window.location.search);
        const sort_field = currentUrlParams.get('sort') || null;
        const sort_order = currentUrlParams.get('order') || null;
        const filter_field = currentUrlParams.get('field') || null;
        const filter_op = currentUrlParams.get('op') || null;
        const filter_value = currentUrlParams.get('value') || null;
        const params = new URLSearchParams({
            collection: getCollectionNameFromURL(),
            limit: 1000,
            skip: totalRows, // Adjust this to the correct number based on your pagination
            sort_field: sort_field,
            sort_order: sort_order,
            filter_field: filter_field,
            filter_op: filter_op,
            filter_value: filter_value
        });
        fetch('/load-more-data?' + params.toString(), {
                method: 'GET', // Or 'POST' if required
                // Include any other necessary request details
            })
            .then(response => response.json())
            .then(data => {
                appendNewRows(data.newRows);
                totalPages = Math.ceil(totalRows / rowsPerPage);
                // currentPage = totalPages;
                displayRows(); // This will display the newly added rows
            })
            .catch(error => console.error('Error loading more data:', error));
    }

    function appendNewRows(newRows) {
        // Convert newRows to HTML and append to the table's tbody
        const tableBody = document.querySelector('table tbody');
        newRows.forEach(rowData => {
            const row = document.createElement('tr');
            // Assuming rowData is an object with keys corresponding to columns
            for (let key in rowData) {
                const cell = document.createElement('td');
                cell.textContent = rowData[key];
                row.appendChild(cell);
            }
            tableBody.appendChild(row);
        });

        // Update your documents variable if needed, or any other state tracking the total number of rows
        // For example: documents.push(...newRows);
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
        // if (currentPage === totalPages - 1) {
        //     loadMoreData();
        // } else
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
function openModal(element_id) {
    const modal = document.getElementById(element_id);
    modal.style.display = "block";
}

function openEditModal(data) {
    for (const key in data) {
        const input = document.getElementById(`${key}-edit`);
        if (input) {
            input.value = data[key];
            input.disabled = key === 'title';
        }

    }
    openModal("editModal");
}

function fetchAndFillItemData(item_id) {
    const collection_name = getCollectionNameFromURL()
    fetch(`/get-item-data/${collection_name}/${item_id}`) // Adjust the endpoint as necessary
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            openEditModal(data);
        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
        });
}

function closeModal(element_id) {
    const modal = document.getElementById(element_id);
    modal.style.display = "none";
}


// Event listeners
document.addEventListener('DOMContentLoaded', (event) => {
    const fileInput = document.getElementById('jsonFile');
    const insertForm = document.getElementById('insertForm');
    const editForm = document.getElementById('editForm');
    window.addEventListener('click', function(event) {
        if (event.target.id === 'insertModal' || event.target.id === 'editModal') {
            closeModal(event.target.id);
        }
    });
    insertForm.addEventListener("submit", (event) => {
        // Prevent the default form submission
        event.preventDefault();
        const urlParams = new URLSearchParams(window.location.search);

        // Create a new FormData object to build the data payload
        const formData = new FormData();
        formData.append('collection_name', getCollectionNameFromURL());

        // Check if a JSON file is uploaded
        if (fileInput.files.length > 0 && fileInput.files[0].type === 'application/json') {
            formData.append('jsonFile', fileInput.files[0]);
        } else {
            // If no file is chosen, iterate over each input and append its value to formData
            const inputs = document.querySelectorAll('#insertForm .input-group input[type="text"]');
            inputs.forEach(input => {
                if (input.value) { // Only add input values that are not empty
                    formData.append(input.name, input.value);
                }
            });
        }

        fetch('/insert_document', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                console.log(data); // Handle success
                if (data.status === 'success') {
                    // Clear all inputs if file upload was successfully
                    document.getElementById('jsonFile').value = ''; // Clear file input
                    document.querySelectorAll('#insertForm .input-group input[type="text"]').forEach(input => {
                        input.value = '';
                        input.disabled = false;
                    });
                    alert(data.message);
                } else {
                    alert("Error: " + data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error); // Handle errors here
            });
    });

    fileInput.addEventListener('change', function(event) {
        const file = event.target.files[0];
        const value = event.target.value;
        if (file && value !== '') {
            console.log("File uploaded")
            if (file.type === 'application/json') {
                // Disable all input fields when a JSON file is selected
                disableInputFields();
            } else {
                document.getElementById('jsonFile').value = ''; // Clear file input
                alert("Please input only .json file");
            }
        }
    });

    editForm.addEventListener("submit", (event) => {
        // Prevent the default form submission
        event.preventDefault();
        const formData = new FormData();
        const collection_name = getCollectionNameFromURL();
        const inputs = document.querySelectorAll('#editForm .input-group input[type="text"]');
        inputs.forEach(input => {
            if (input.value) { // Only add input values that are not empty
                formData.append(input.name, input.value);
            }
        });
        const selectedCheckbox = document.querySelector('.select-item:checked');
        let item_id = null;
        if (selectedCheckbox) {
            item_id = selectedCheckbox.value;
        } else {
            alert("Please select an item to edit.");
        }


        fetch(`/edit_document/${collection_name}/${item_id}`, {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                console.log(data); // Handle success
                if (data.status === 'success') {
                    document.querySelectorAll('#insertForm .input-group input[type="text"]').forEach(input => {
                        input.value = '';
                    });
                    closeModal("editModal")
                    window.location.reload();
                    alert(data.message);
                } else {
                    alert("Error: " + data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error); // Handle errors here
            });
    });

    function disableInputFields() {
        // Find all input groups in the form and disable them
        const inputFields = insertForm.querySelectorAll('#insertForm .input-group input');
        inputFields.forEach(function(input) {
            input.value = '';
            input.disabled = true;
        });
    }

});



document.getElementById('edit').addEventListener('click', () => {
    const selectedCheckbox = document.querySelector('.select-item:checked');
    if (selectedCheckbox) {
        const itemId = selectedCheckbox.value;
        fetchAndFillItemData(itemId);

    } else {
        alert("Please select an item to edit.");
    }
});

document.addEventListener('DOMContentLoaded', function() {

    const selectAllCheckbox = document.getElementById('select-all');
    const checkboxes = Array.from(document.querySelectorAll('.select-item'));
    const deleteButton = document.getElementById('delete');
    const editButton = document.getElementById('edit');
    // Function to update the delete button's disabled state
    function updateButtonState() {
        const checkedCheckboxes = checkboxes.filter(checkbox => checkbox.checked);
        const anyChecked = checkedCheckboxes.length > 0;
        const oneChecked = checkedCheckboxes.length === 1;
        // Toggle delete button disabled state based on if any checkbox is checked
        deleteButton.disabled = !anyChecked;
        // Toggle edit button disabled state based on if exactly one checkbox is checked
        editButton.disabled = !oneChecked;
        selectAllCheckbox.checked = checkboxes.length === checkedCheckboxes.length;
    }

    // Event listener for 'select all' checkbox
    selectAllCheckbox.addEventListener('change', function() {
        checkboxes.forEach(checkbox => {
            checkbox.checked = this.checked;
        });
        updateButtonState();
    });

    // Event listeners for each checkbox in the table
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', updateButtonState);
    });

    // Event listener for the delete button
    deleteButton.addEventListener('click', function() {
        if (confirm('Are you sure you want to delete the selected items?')) {
            const selectedIds = Array.from(checkboxes)
                .filter(checkbox => checkbox.checked)
                .map(checkbox => checkbox.value);
            const selectAll_status = document.getElementById('select-all').checked;

            // Create a FormData object to send the selected IDs
            let formData = new FormData();
            formData.append('collection_name', getCollectionNameFromURL());
            if (selectAll_status) {
                formData.append('select-all', true)
                let url = new URL(document.location.toString());
                formData.append('params', url.toString())
            } else {
                formData.append('ids', JSON.stringify(selectedIds));
            }

            // Send the DELETE request
            fetch('/delete_document', {
                    method: 'POST', // If your server supports DELETE, change this to 'DELETE'
                    body: formData
                })
                .then(response => response.json())
                .then(data => {
                    console.log(data); // Handle the response data
                    if (data.status === 'success') {
                        alert(data.message);
                        window.location.reload();
                    } else {
                        alert(data.message);
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    console.error('Error:', error); // Handle errors here
                });
        }
    });

    // Initialize delete button state on page load
    updateButtonState();
});