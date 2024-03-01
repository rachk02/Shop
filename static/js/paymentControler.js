document.addEventListener('DOMContentLoaded', function() {
    var submitButton = document.getElementById('payment-btn');
    var paymentForm = document.getElementById('paymentForm');
    submitButton.addEventListener('click', function() {
        paymentForm.submit();
    });
});