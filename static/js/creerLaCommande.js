document.addEventListener('DOMContentLoaded', function() {
    var submitButton = document.getElementById('creer_commande_btn');
    var commandeForm = document.getElementById('creerCommandeForm');
    submitButton.addEventListener('click', function() {
        commandeForm.submit();
    });
});
