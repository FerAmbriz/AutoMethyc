// Obtén todos los elementos 'li' dentro de '.vertical'
let items = document.querySelectorAll('.vertical li a');
let activeItem;

function setActiveItem(item) {
    // Remueve la clase 'active' de todos los elementos
    items.forEach((item) => {
        item.parentElement.classList.remove('active');
        if (item.parentElement.parentElement.parentElement.tagName === 'LI') {
            item.parentElement.parentElement.parentElement.classList.remove('active');
        }
    });

    // Añade la clase 'active' al elemento seleccionado
    item.parentElement.classList.add('active');
    if (item.parentElement.parentElement.parentElement.tagName === 'LI') {
        item.parentElement.parentElement.parentElement.classList.add('active');
    }
    activeItem = item;
}

// Añade un evento de escucha a cada elemento 'li'
items.forEach((item) => {
    item.addEventListener('click', function(event) {
        event.stopPropagation();
        setActiveItem(this);
    });
});

window.addEventListener('scroll', function() {
    items.forEach(function(item) {
        var section = document.querySelector(item.getAttribute('href'));
        var sectionTop = section.offsetTop;
        var sectionBottom = sectionTop + section.offsetHeight;
        if (window.scrollY >= sectionTop && window.scrollY < sectionBottom) {
            setActiveItem(item);
        }
    });
});

window.addEventListener('hashchange', function() {
    items.forEach(function(item) {
        if (item.getAttribute('href') === location.hash) {
            setActiveItem(item);
        }
    });
});
