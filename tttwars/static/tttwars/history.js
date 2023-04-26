document.addEventListener('DOMContentLoaded', function() {  
    document.querySelectorAll('.gamelisting').forEach(function(listing) {
        listing.onclick = function () {
            const id = listing.dataset.id;
            console.log(id)
            window.location.replace('/history/' + id);
        }
    })
})
