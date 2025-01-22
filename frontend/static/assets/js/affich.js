document.addEventListener('DOMContentLoaded', (event) => {
    const menuItems = document.querySelectorAll('#meenu-decouvr .meenu-item');
    const sections = document.querySelectorAll('.content-affich-section');

    menuItems.forEach(item => {
        item.addEventListener('click', () => {
            // Hide all sections
            sections.forEach(section => {
                section.classList.remove('active');
            });

            // Show the corresponding section
            const sectionId = item.getAttribute('data-content');
            document.getElementById(sectionId).classList.add('active');
        });
    });
});
