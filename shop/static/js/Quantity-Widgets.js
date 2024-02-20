document.addEventListener("DOMContentLoaded", function () {
    // Ajouter des gestionnaires d'événements pour les boutons
    document.getElementById('decreaseButton').addEventListener('click', decreaseQuantity);
    document.getElementById('increaseButton').addEventListener('click', increaseQuantity);
});

function decreaseQuantity() {
    // Logique pour diminuer la quantité
    let quantityField = document.getElementById('id_quantite');
    if (quantityField.value > 1) {
        quantityField.value = parseInt(quantityField.value, 10) - 1;
    }
}

function increaseQuantity() {
    // Logique pour augmenter la quantité
    let quantityField = document.getElementById('id_quantite');
    quantityField.value = parseInt(quantityField.value, 10) + 1;
}
