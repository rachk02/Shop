document.addEventListener("DOMContentLoaded", function() {
    var ajouterAuPanierBtns = document.querySelectorAll('.ajouter-au-panier-btn');

    ajouterAuPanierBtns.forEach(function(btn) {
        btn.addEventListener('click', function() {
            var produitId = btn.getAttribute('data-produit-id');
            var ajouterProduitForm = document.getElementById('ajouterProduitForm-' + produitId);

            if (ajouterProduitForm) {
                ajouterProduitForm.submit();
            }
        });
    });
});
