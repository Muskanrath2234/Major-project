// Select all dropdown elements
const allDropdown = document.querySelectorAll('#sidebar .side-dropdown');

// Function to handle dropdown click events
allDropdown.forEach(item => {
    const a = item.parentElement.querySelector('a:first-child');
    a.addEventListener('click', function (e) {
        e.preventDefault();

        if (!this.classList.contains('active')) {
            allDropdown.forEach(i => {
                const aLink = i.parentElement.querySelector('a:first-child');
                aLink.classList.remove('active');
                i.classList.remove('show');
            });
        }

        this.classList.toggle('active');
        item.classList.toggle('show');
    });
});

// PROFILE DROPDOWN
const profile = document.querySelector('nav .profile');
const imgProfile = profile.querySelector('img');
const dropdownProfile = profile.querySelector('.profile-link');

imgProfile.addEventListener('click', function () {
    dropdownProfile.classList.toggle('show');
});

// Close profile dropdown if clicking outside
window.addEventListener('click', function (e) {
    if (!profile.contains(e.target)) {
        if (dropdownProfile.classList.contains('show')) {
            dropdownProfile.classList.remove('show');
        }
    }
});

// SIDEBAR COLLAPSE
const sidebar = document.querySelector('#sidebar');
const toggleSidebar = document.querySelector('nav .toggle-sidebar');
const allSideDivider = document.querySelectorAll('#sidebar .divider');

// Update state on initial load
if (sidebar.classList.contains('hide')) {
    updateSidebarState('-');
} else {
    updateSidebarState();
}

toggleSidebar.addEventListener('click', function () {
    sidebar.classList.toggle('hide');
    updateSidebarState(sidebar.classList.contains('hide') ? '-' : null);
});

sidebar.addEventListener('mouseleave', function () {
    if (sidebar.classList.contains('hide')) {
        updateSidebarState('-');
    }
});

sidebar.addEventListener('mouseenter', function () {
    if (sidebar.classList.contains('hide')) {
        updateSidebarState();
    }
});

// Function to update sidebar state
function updateSidebarState(overrideText = null) {
    allSideDivider.forEach(item => {
        item.textContent = overrideText || item.dataset.text;
    });
    allDropdown.forEach(item => {
        const a = item.parentElement.querySelector('a:first-child');
        a.classList.remove('active');
        item.classList.remove('show');
    });
}
