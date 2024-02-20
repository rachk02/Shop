document.addEventListener("DOMContentLoaded", function () {
    var descriptionSwitch = document.querySelector('#descriptionSwitch');
    var descriptionContent = document.querySelector('#descriptionContent');

    if (descriptionSwitch && descriptionContent) {
        descriptionSwitch.addEventListener('change', function () {
            descriptionContent.style.display = this.checked ? 'block' : 'none';
        });
    }
});