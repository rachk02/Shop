document.addEventListener("DOMContentLoaded", function () {
    var removeButton = document.querySelector('.ref-product-remove');
    if (removeButton) {
        removeButton.addEventListener('click', function () {
            document.getElementById('removeForm').submit();
        });
    }
});