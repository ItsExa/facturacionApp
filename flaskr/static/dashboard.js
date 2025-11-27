const menuItems = document.querySelectorAll('.menu-item');
const contentArea = document.getElementById('content-area');

// Cargar opción activa del localStorage
let activeSection = localStorage.getItem('activeSection') || 'inicio';

// Función para actualizar contenido
function loadSection(section) {
    activeSection = section;
    localStorage.setItem('activeSection', section);

    // Actualizar contenido de ejemplo
    contentArea.innerHTML = `<h2>${section.charAt(0).toUpperCase() + section.slice(1)}</h2>
                             <p>Contenido de la sección ${section}.</p>`;

    // Actualizar estilo activo
    menuItems.forEach(item => {
        if(item.dataset.section === section){
            item.classList.add('active');
        } else {
            item.classList.remove('active');
        }
    });
}

// Asignar click a cada item
menuItems.forEach(item => {
    item.addEventListener('click', () => loadSection(item.dataset.section));
});

// Inicializar sección activa al cargar la página
loadSection(activeSection);
