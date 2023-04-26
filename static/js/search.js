$(document).ready(function() {
    var searchForm = $('#search-form');
    var searchInput = $('#search-input');
    var searchResults = $('#search-results');

    // Submit search form
    searchForm.submit(function(event) {
        event.preventDefault();
    });

    // Handle search input
    searchInput.keyup(function() {
        var query = $(this).val().trim();

        // Clear search results
        searchResults.html('');

        // Display loader
        searchResults.html('<div class="loader"></div>');

        // Make AJAX request
        $.ajax({
            type: 'GET',
            url: searchForm.attr('action'),
            data: {'q': query},
            success: function(data) {
                // Hide loader
                searchResults.html('');

                // Display search results
                searchResults.html(data);
            },
            error: function() {
                // Hide loader
                searchResults.html('');

                // Display error message
                searchResults.html('<p>Oops! Something went wrong.</p>');
            }
        });
    });
});