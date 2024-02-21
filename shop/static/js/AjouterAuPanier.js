document.addEventListener("DOMContentLoaded", function() {
    var ajouterAuPanierBtns = document.querySelectorAll('.ajouter-au-panier-btn');

    ajouterAuPanierBtns.forEach(function(btn) {
        btn.addEventListener('click', function(event) {
            event.preventDefault(); // Empêche le comportement par défaut du lien

            var produitId = btn.getAttribute('data-produit-id');
            var ajouterProduitForm = document.getElementById('ajouterProduitForm-' + produitId);

            if (ajouterProduitForm) {
                ajouterProduitForm.submit();
            }
        });
    });
});
