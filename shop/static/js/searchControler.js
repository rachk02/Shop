document.addEventListener('DOMContentLoaded', function() {
    var submitButton = document.getElementById('search-btn');
    var searchForm = document.getElementById('searchForm');
    submitButton.addEventListener('click', function() {
        searchForm.submit();
    });
});
