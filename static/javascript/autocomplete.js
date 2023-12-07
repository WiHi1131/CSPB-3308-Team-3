document.addEventListener('DOMContentLoaded', function() {
    var searchInput = document.getElementById('searchInput');

    searchInput.addEventListener('input', function() {
        var searchTerm = searchInput.value;

        if (searchTerm.length > 0) {
            fetch('/get_food_suggestions?term=' + encodeURIComponent(searchTerm))
                .then(response => response.json())
                .then(data => {
                    // Clear any existing suggestions
                    removeAllChildNodes(searchInput.nextElementSibling);

                    // Create a new list of suggestions
                    var suggestionList = document.createElement('ul');
                    data.forEach(function(item) {
                        var listItem = document.createElement('li');
                        listItem.textContent = item;
                        suggestionList.appendChild(listItem);
                    });

                    searchInput.parentNode.appendChild(suggestionList);
                })
                .catch(error => console.error('Error:', error));
        }
    });

    function removeAllChildNodes(parent) {
        while (parent.firstChild) {
            parent.removeChild(parent.firstChild);
        }
    }
});
