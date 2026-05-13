const detailButtons = document.querySelectorAll('.details-toggle');
const journalCount = document.getElementById('journalCount');
const journalSection = document.querySelector('.journal-section');
const activityBadge = document.getElementById('activityBadge');

detailButtons.forEach(button => {
    button.addEventListener('click', () => {
        const detailsId = button.getAttribute('aria-controls');
        const detailsPanel = document.getElementById(detailsId);
        const isExpanded = button.getAttribute('aria-expanded') === 'true';

        button.setAttribute('aria-expanded', String(!isExpanded));
        button.textContent = isExpanded ? 'View details' : 'Hide details';
        detailsPanel.hidden = isExpanded;
    });
});

function updateCoffeeCount(count) {
    if (!journalCount) {
        return;
    }

    journalCount.textContent = `${count} ${count === 1 ? 'coffee' : 'coffees'}`;
}

function updateActivityBadge(label) {
    if (!activityBadge || !label) {
        return;
    }

    activityBadge.textContent = label;
}

function showEntryError(card, message) {
    const error = card.querySelector('.entry-error');
    if (!error) {
        return;
    }

    error.textContent = message;
    error.hidden = false;
}

function hideEntryError(card) {
    const error = card.querySelector('.entry-error');
    if (!error) {
        return;
    }

    error.textContent = '';
    error.hidden = true;
}

function setText(card, field, value) {
    const element = card.querySelector(`[data-entry-field="${field}"]`);
    if (element) {
        element.textContent = value;
    }
}

function updateEntryCard(card, entry) {
    setText(card, 'title', entry.title);
    setText(card, 'coffee_type', entry.coffee_type);
    setText(card, 'cafe_name', entry.cafe_name);
    setText(card, 'stars', entry.stars);
    setText(card, 'notes', entry.notes);
    setText(card, 'detail_cafe_name', entry.cafe_name);
    setText(card, 'detail_coffee_type', entry.coffee_type);
    setText(card, 'rating', entry.rating);
    setText(card, 'detail_notes', entry.notes);
}

function showEmptyJournal() {
    if (!journalSection || document.getElementById('emptyJournal')) {
        return;
    }

    const emptyMessage = document.createElement('div');
    emptyMessage.className = 'empty-journal';
    emptyMessage.id = 'emptyJournal';
    emptyMessage.textContent = 'No coffee logs yet.';
    journalSection.appendChild(emptyMessage);
}

document.querySelectorAll('.edit-entry').forEach(button => {
    button.addEventListener('click', () => {
        const card = button.closest('.entry-card');
        const form = card.querySelector('.entry-edit-form');

        hideEntryError(card);
        form.hidden = false;
    });
});

document.querySelectorAll('.cancel-edit').forEach(button => {
    button.addEventListener('click', () => {
        const card = button.closest('.entry-card');
        const form = card.querySelector('.entry-edit-form');

        hideEntryError(card);
        form.hidden = true;
    });
});

document.querySelectorAll('.entry-edit-form').forEach(form => {
    form.addEventListener('submit', async event => {
        event.preventDefault();

        const card = form.closest('.entry-card');
        const entryId = card.dataset.entryId;
        const formData = new FormData(form);
        const payload = {
            cafe_name: formData.get('cafe_name'),
            coffee_type: formData.get('coffee_type'),
            rating: formData.get('rating'),
            notes: formData.get('notes'),
        };

        hideEntryError(card);

        try {
            const response = await fetch(`/my_journal/${entryId}/edit`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload),
            });
            const data = await response.json();

            if (!response.ok || !data.success) {
                throw new Error(data.error || 'Unable to update this entry.');
            }

            updateEntryCard(card, data.entry);
            form.hidden = true;
        } catch (error) {
            showEntryError(card, error.message);
        }
    });
});

document.querySelectorAll('.delete-entry').forEach(button => {
    button.addEventListener('click', async () => {
        const card = button.closest('.entry-card');
        const entryId = card.dataset.entryId;
        const confirmed = confirm('Are you sure you want to delete this entry?');

        if (!confirmed) {
            return;
        }

        hideEntryError(card);

        try {
            const response = await fetch(`/my_journal/${entryId}/delete`, {
                method: 'POST',
            });
            const data = await response.json();

            if (!response.ok || !data.success) {
                throw new Error(data.error || 'Unable to delete this entry.');
            }

            card.remove();
            updateCoffeeCount(data.entry_count);
            updateActivityBadge(data.activity_badge);

            if (data.entry_count === 0) {
                showEmptyJournal();
            }
        } catch (error) {
            showEntryError(card, error.message);
        }
    });
});
