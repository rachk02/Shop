document.addEventListener("DOMContentLoaded", function () {
    var decreaseButtons = document.querySelectorAll('.cart-decrease');
    var increaseButtons = document.querySelectorAll('.cart-increase');
    var majQteBtns = document.querySelectorAll('.maj-qte-btn');

    decreaseButtons.forEach(function (button) {
        button.addEventListener('click', function () {
            updateQuantite(button, -1);
        });
    });

    increaseButtons.forEach(function (button) {
        button.addEventListener('click', function () {
            updateQuantite(button, 1);
        });
    });

    majQteBtns.forEach(function (btn) {
        btn.addEventListener('click', function () {
            var produitId = btn.dataset.produitId;
            var inputField = document.querySelector('.maj-quantite-form[data-produit-id="' + produitId + '"] input[name="quantite"]');
            var currentQuantite = parseInt(inputField.value, 10);
            submitForm(produitId, currentQuantite);
        });
    });

    function updateQuantite(button, change) {
        var produitId = button.closest('.maj-quantite-form').dataset.produitId;
        var inputField = button.closest('.maj-quantite-form').querySelector('input[name="quantite"]');
        var currentQuantite = parseInt(inputField.value, 10);
        var newQuantite = currentQuantite + change;

        if (newQuantite > 0) {
            inputField.value = newQuantite;
            submitForm(produitId, newQuantite);
        }
    }

    function submitForm(produitId, produitQte) {
        var form = document.querySelector('.maj-quantite-form[data-produit-id="' + produitId + '"]');
        form.querySelector('input[name="quantite"]').value = produitQte;
        form.submit();
    }
});
