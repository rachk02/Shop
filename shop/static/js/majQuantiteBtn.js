document.addEventListener("DOMContentLoaded", function () {
    var majQteBtns = document.querySelectorAll('.maj-qte-btn');

    majQteBtns.forEach(function (btn) {
        btn.addEventListener('click', function () {
            var produitId = btn.dataset.produitId;
            submitForm(produitId);
        });
    });

    function submitForm(produitId) {
        var form = document.querySelector('.maj-quantite-form[data-produit-id="' + produitId + '"]');
        form.submit();
    }
});
