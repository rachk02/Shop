document.addEventListener("DOMContentLoaded", function() {
    var retirerDuPanierBtns = document.querySelectorAll('.retirer-un-pinp-btn');

    retirerDuPanierBtns.forEach(function(btn) {
        btn.addEventListener('click', function() {
            var produitId = btn.getAttribute('data-produit-id');
            var retirerUnPinPForm = document.getElementById('retirerUnPinPForm-' + produitId);

            if (retirerUnPinPForm) {
                retirerUnPinPForm.submit();
            }
        });
    });
});