const detailButtons = document.querySelectorAll('.details-toggle');

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
