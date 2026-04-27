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

// Save coffee entry to localStorage
function logCoffee() {
    const cafeName = document.getElementById('cafeName').value.trim();
    const coffeeType = document.getElementById('coffeeType').value;
    const rating = ratingInput.value;
    const notes = document.getElementById('notes').value.trim();

    // Validation - make sure required fields are filled
    if (!cafeName || !coffeeType || rating === '0') {
        alert('Please fill in the cafe name, coffee type, and rating!');
        return;
    }

    // Create the entry object
    const entry = {
        id: Date.now(),
        cafeName,
        coffeeType,
        rating: parseInt(rating),
        notes,
        date: new Date().toLocaleDateString('en-AU', { day: 'numeric', month: 'long', year: 'numeric' })
    };

    // Save to localStorage
    const existing = JSON.parse(localStorage.getItem('coffeeLog') || '[]');
    existing.push(entry);
    localStorage.setItem('coffeeLog', JSON.stringify(existing));

    // Show success message
    document.getElementById('successMsg').classList.add('show');
    setTimeout(() => document.getElementById('successMsg').classList.remove('show'), 3000);

    // Reset the form
    document.getElementById('cafeName').value = '';
    document.getElementById('coffeeType').value = '';
    document.getElementById('notes').value = '';
    ratingInput.value = '0';
    ratingLabel.textContent = 'Tap to rate';
    highlightStars(0);
}

// Link button to logCoffee function
document.getElementById('submitBtn').addEventListener('click', logCoffee);

// Show text input when 'Other' is selected
document.getElementById('coffeeType').addEventListener('change', function() {
    const otherInput = document.getElementById('otherType');
    if (this.value === 'Other') {
        otherInput.style.display = 'block';
    } else {
        otherInput.style.display = 'none';
    }
});