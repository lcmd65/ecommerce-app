async function filterProducts() {
    // Get the form element
    var form = document.getElementById('filterForm');

    // Create an object to store selected values
    var selectedValues = {};

    // Iterate through checkboxes and store selected values
    var checkboxes = form.querySelectorAll('input[type="checkbox"]:checked');
    checkboxes.forEach(function(checkbox) {
        var categoryName = checkbox.getAttribute('name');
        var checkboxValue = checkbox.value;
        if (!selectedValues[categoryName]) {
            selectedValues[categoryName] = [];
        }
        selectedValues[categoryName].push(checkboxValue);
    });

    // Convert the object to a JSON string and store it in a hidden input field
    var selectedValuesInput = document.createElement('input');
    selectedValuesInput.type = 'hidden';
    selectedValuesInput.name = 'selectedValues';
    selectedValuesInput.value = JSON.stringify(selectedValues);
    form.appendChild(selectedValuesInput);

    // Submit the form
    form.submit();
}