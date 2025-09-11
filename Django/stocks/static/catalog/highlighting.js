const path = window.location.pathname;

let currentPage = '';
if (path === '/' || path.endsWith('/company/')) {
currentPage = 'home';
} else if (path.includes('about') || path.endsWith('/about_me/')) {
currentPage = 'aboutme';
} else if (path.includes('contact') || path.endsWith('/contact/')) {
currentPage = 'contact';
}

// Highlight matching nav link
document.querySelectorAll('.nav-link').forEach(link => {
if (link.dataset.page === currentPage) {
link.classList.add('active');
}
});
