// Get all star elements
const stars = document.querySelectorAll('.star');
const ratingInput = document.getElementById('ratingValue');
const ratingLabel = document.getElementById('ratingLabel');

// Labels for each star rating
const labels = ['', 'Poor', 'Fair', 'Good', 'Great', 'Amazing'];

// Highlight stars up to the selected number
function highlightStars(count) {
    stars.forEach(star => {
        if (star.dataset.value <= count) {
            star.classList.add('filled');
        } else {
            star.classList.remove('filled');
        }
    });
}

// Add hover and click events to each star
stars.forEach(star => {
    star.addEventListener('mouseover', function() {
    highlightStars(this.dataset.value);
    ratingLabel.textContent = labels[this.dataset.value];
    });

    star.addEventListener('mouseout', function() {
    highlightStars(ratingInput.value);
    ratingLabel.textContent = ratingInput.value === '0' ? 'Tap to rate' : labels[ratingInput.value];
    });

    star.addEventListener('click', function() {
        ratingInput.value = this.dataset.value;
        ratingLabel.textContent = labels[this.dataset.value];
        highlightStars(this.dataset.value);
    });
});