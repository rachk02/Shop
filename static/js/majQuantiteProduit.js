document.addEventListener("DOMContentLoaded", function() {
    var decreaseButtons = document.querySelectorAll('.cart-decrease');
    var increaseButtons = document.querySelectorAll('.cart-increase');

    decreaseButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            decreasePinPQuantite(button);
        });
    });

    increaseButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            increasePinPQuantite(button);
        });
    });
});

function decreasePinPQuantite(button) {
    var produitId = button.closest('.maj-quantite-form').dataset.produitId;
    var inputField = button.closest('.maj-quantite-form').querySelector('input[name="quantite"]');
    var currentQuantite = parseInt(inputField.value, 10);
    if (currentQuantite > 1) {
        inputField.value = currentQuantite - 1;
    }
}

function increasePinPQuantite(button) {
    var produitId = button.closest('.maj-quantite-form').dataset.produitId;
    var inputField = button.closest('.maj-quantite-form').querySelector('input[name="quantite"]');
    var currentQuantite = parseInt(inputField.value, 10);
    inputField.value = currentQuantite + 1;
}
