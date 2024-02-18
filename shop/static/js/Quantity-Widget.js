// quantityWidget.js

document.addEventListener('DOMContentLoaded', function() {
    var quantityInput = document.querySelector('.ref-quantity-widget input');
    var decreaseButton = document.querySelector('.ref-decrease');
    var increaseButton = document.querySelector('.ref-increase');

    decreaseButton.addEventListener('click', function() {
        var currentValue = parseInt(quantityInput.value);
        if (currentValue > 1) {
            quantityInput.value = currentValue - 1;
        }
    });

    increaseButton.addEventListener('click', function() {
        var currentValue = parseInt(quantityInput.value);
        quantityInput.value = currentValue + 1;
    });
});
