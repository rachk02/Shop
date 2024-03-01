document.addEventListener('DOMContentLoaded', function() {
    var ajouterAuPanierBtn = document.querySelector('.ajouter-au-panier-btn-produit');

    if (ajouterAuPanierBtn) {
        ajouterAuPanierBtn.addEventListener('click', function() {
            // Soumettez le formulaire associé
            var formulaire = document.getElementById('ajouterProduitPanierForm');
            if (formulaire) {
                formulaire.submit();
            }
        });
    }
});
