// index.js

document.addEventListener('DOMContentLoaded', function () {
    const isCurrentCheckbox = document.getElementById('is_current');
    const endDateField = document.querySelector('[name="end_date"]');

    if (!isCurrentCheckbox || !endDateField) {
        console.error('Required elements not found in the DOM');
        return;
    }

    function toggleEndDate() {
        if (isCurrentCheckbox.checked) {
            endDateField.disabled = true;
            endDateField.value = '';  // Clear the value if it's disabled
        } else {
            endDateField.disabled = false;
        }
    }

    // Initialize the state on page load
    toggleEndDate();

    // Add event listener to checkbox
    isCurrentCheckbox.addEventListener('change', toggleEndDate);
});