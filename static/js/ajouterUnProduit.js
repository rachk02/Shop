document.addEventListener("DOMContentLoaded", function() {
    var ajouterUnAuPanierBtns = document.querySelectorAll('.ajouter-un-au-panier-btn');

    ajouterUnAuPanierBtns.forEach(function(btn) {
        btn.addEventListener('click', function() {
            var produitId = btn.getAttribute('data-produit-id');
            var ajouterUnAuPanierForm = document.getElementById('ajouterUnAuPanierForm-' + produitId);

            if (ajouterUnAuPanierForm) {
                ajouterUnAuPanierForm.submit();
            }
        });
    });
});