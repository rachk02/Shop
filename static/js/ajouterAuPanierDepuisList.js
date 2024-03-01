$(document).ready(function() {
    $(".ajouter-au-panier-depuis-list-btn").click(function() {
        var produitId = $(this).data("produit-id");

        $.post(
            "/panier/ajouter_produit_direct/" + produitId + "/",
        );
    });
});
