document.addEventListener("DOMContentLoaded", function() {
    var ajouterAuPanierBtns = document.querySelectorAll('.ajouter-au-panier-btn');

    ajouterAuPanierBtns.forEach(function(btn) {
        btn.addEventListener('click', function() {
            var produitId = btn.getAttribute('data-produit-id');
            var ajouterProduitForm = document.getElementById('ajouterProduitForm');

            if (ajouterProduitForm) {
                ajouterProduitForm.submit();
            }
        });
    });

    var retirerDuPanierBtns = document.querySelectorAll('.retirer-du-panier-btn');

    retirerDuPanierBtns.forEach(function(btn) {
        btn.addEventListener('click', function() {
            var produitId = btn.getAttribute('data-produit-id');
            var retirerProduitForm = document.getElementById('retirerProduitForm');

            if (retirerProduitForm) {
                retirerProduitForm.submit();
            }
        });
    });
});
