// Smart Agriculture Advisory System - Core JavaScript

// Bilingual translation dictionary (English & Kannada)
const translations = {
    'en': {
        'brand': 'Smart Agri',
        'home': 'Home',
        'about': 'About',
        'services': 'Services',
        'features': 'Features',
        'faq': 'FAQ',
        'contact': 'Contact',
        'login': 'Login',
        'register': 'Register',
        'dashboard': 'Dashboard',
        'profile': 'My Profile',
        'crop_recommendation': 'Crop Recommendation',
        'weather_advisory': 'Weather Advisory',
        'fertilizer_recommendation': 'Fertilizer Advisor',
        'pest_disease': 'Pests & Diseases',
        'irrigation_advisory': 'Irrigation Schedule',
        'market_prices': 'Market Prices',
        'agricultural_news': 'Agricultural News',
        'government_schemes': 'Government Schemes',
        'feedback': 'Submit Feedback',
        'settings': 'Settings',
        'logout': 'Logout',
        'welcome': 'Welcome, Farmer!',
        'quick_access': 'Quick Access',
        'notifications': 'Recent Notifications',
        'recent_recommendations': 'Recent recommendations',
        'today_temp': 'Today\'s Temperature',
        'humidity': 'Humidity',
        'market_update': 'Market Price Updates',
        'latest_news': 'Latest News',
        'gov_schemes': 'Government Schemes',
        'total_crops': 'Total Crops'
    },
    'kn': {
        'brand': 'ಸ್ಮಾರ್ಟ್ ಕೃಷಿ',
        'home': 'ಮುಖಪುಟ',
        'about': 'ನಮ್ಮ ಬಗ್ಗೆ',
        'services': 'ಸೇವೆಗಳು',
        'features': 'ವೈಶಿಷ್ಟ್ಯಗಳು',
        'faq': 'ಪ್ರಶ್ನೋತ್ತರಗಳು',
        'contact': 'ಸಂಪರ್ಕಿಸಿ',
        'login': 'ಲಾಗಿನ್',
        'register': 'ನೋಂದಣಿ',
        'dashboard': 'ಡ್ಯಾಶ್‌ಬೋರ್ಡ್',
        'profile': 'ನನ್ನ ವಿವರಗಳು',
        'crop_recommendation': 'ಬೆಳೆ ಶಿಫಾರಸು',
        'weather_advisory': 'ಹವಾಮಾನ ಸಲಹೆ',
        'fertilizer_recommendation': 'ಗೊಬ್ಬರ ಸಲಹೆಗಾರ',
        'pest_disease': 'ಕೀಟಗಳು ಮತ್ತು ರೋಗಗಳು',
        'irrigation_advisory': 'ನೀರಾವರಿ ವೇಳಾಪಟ್ಟಿ',
        'market_prices': 'ಮಾರುಕಟ್ಟೆ ಬೆಲೆಗಳು',
        'agricultural_news': 'ಕೃಷಿ ಸುದ್ದಿ',
        'government_schemes': 'ಸರ್ಕಾರಿ ಯೋಜನೆಗಳು',
        'feedback': 'ಅಭಿಪ್ರಾಯ ಸಲ್ಲಿಸಿ',
        'settings': 'ಸಂಯೋಜನೆಗಳು',
        'logout': 'ಲಾಗ್ ಔಟ್',
        'welcome': 'ಕೃಷಿಕರೇ, ನಿಮಗೆ ಸುಸ್ವಾಗತ!',
        'quick_access': 'ತ್ವರಿತ ಪ್ರವೇಶ',
        'notifications': 'ಇತ್ತೀಚಿನ ಅಧಿಸೂಚನೆಗಳು',
        'recent_recommendations': 'ಇತ್ತೀಚಿನ ಬೆಳೆ ಶಿಫಾರಸುಗಳು',
        'today_temp': 'ಇಂದಿನ ತಾಪಮಾನ',
        'humidity': 'ಆರ್ದ್ರತೆ',
        'market_update': 'ಮಾರುಕಟ್ಟೆ ಬೆಲೆ ಅಪ್ಡೇಟ್',
        'latest_news': 'ಇತ್ತೀಚಿನ ಸುದ್ದಿಗಳು',
        'gov_schemes': 'ಸರ್ಕಾರಿ ಯೋಜನೆಗಳು',
        'total_crops': 'ಒಟ್ಟು ಬೆಳೆಗಳು'
    }
};

document.addEventListener('DOMContentLoaded', () => {
    // Initialize Theme (Dark Mode)
    initTheme();
    
    // Initialize Language
    initLanguage();

    // Attach form validations
    setupValidations();
});

// Theme Management (Dark Mode)
function initTheme() {
    const themeToggle = document.getElementById('themeToggle');
    if (!themeToggle) return;

    // Check saved preference
    const isDarkMode = localStorage.getItem('darkMode') === 'enabled';
    if (isDarkMode) {
        document.body.classList.add('dark-mode');
        themeToggle.checked = true;
        updateToggleIcon(true);
    }

    themeToggle.addEventListener('change', () => {
        if (themeToggle.checked) {
            document.body.classList.add('dark-mode');
            localStorage.setItem('darkMode', 'enabled');
            updateToggleIcon(true);
        } else {
            document.body.classList.remove('dark-mode');
            localStorage.setItem('darkMode', 'disabled');
            updateToggleIcon(false);
        }
    });
}

function updateToggleIcon(isDark) {
    const icon = document.getElementById('themeIcon');
    if (!icon) return;
    if (isDark) {
        icon.className = 'fas fa-moon text-light';
    } else {
        icon.className = 'fas fa-sun text-warning';
    }
}

// Language Management (Bilingual Switcher)
function initLanguage() {
    const langSelect = document.getElementById('langSelect');
    if (!langSelect) return;

    // Load saved lang preference
    const savedLang = localStorage.getItem('appLang') || 'en';
    langSelect.value = savedLang;
    applyLanguage(savedLang);

    langSelect.addEventListener('change', () => {
        const selectedLang = langSelect.value;
        localStorage.setItem('appLang', selectedLang);
        applyLanguage(selectedLang);
        
        // Also send request to server to store language in session if needed
        fetch(`/farmer/settings`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `language=${selectedLang}`
        }).catch(err => console.log('Lang session update failed:', err));
    });
}

function applyLanguage(lang) {
    document.querySelectorAll('[data-translate]').forEach(elem => {
        const key = elem.getAttribute('data-translate');
        if (translations[lang] && translations[lang][key]) {
            // Check if element is a button, placeholder, or standard text
            if (elem.placeholder) {
                elem.placeholder = translations[lang][key];
            } else {
                elem.innerText = translations[lang][key];
            }
        }
    });
}

// Client-Side Form Validations
function setupValidations() {
    // 1. Validation for Registration Form
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', (e) => {
            const password = document.getElementById('password').value;
            const confirmPassword = document.getElementById('confirm_password').value;
            const email = document.getElementById('email').value;
            const phone = document.getElementById('phone').value;

            // Password matching validation
            if (password !== confirmPassword) {
                alert('Passwords do not match.');
                e.preventDefault();
                return;
            }

            // Password strength validation (min 6 characters)
            if (password.length < 6) {
                alert('Password must be at least 6 characters long.');
                e.preventDefault();
                return;
            }

            // Email format validation
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(email)) {
                alert('Please enter a valid email address.');
                e.preventDefault();
                return;
            }

            // Phone number validation (10 digits)
            const phoneRegex = /^[0-9]{10}$/;
            if (phone && !phoneRegex.test(phone)) {
                alert('Please enter a valid 10-digit phone number.');
                e.preventDefault();
                return;
            }
        });
    }

    // 2. Validation for Contact Form
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', (e) => {
            const email = document.getElementById('email').value;
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(email)) {
                alert('Please enter a valid email address.');
                e.preventDefault();
                return;
            }
        });
    }

    // 3. Validation for Profile Edit Form
    const profileForm = document.getElementById('profileForm');
    if (profileForm) {
        profileForm.addEventListener('submit', (e) => {
            const phone = document.getElementById('phone').value;
            const farmSize = document.getElementById('farm_size').value;

            const phoneRegex = /^[0-9]{10}$/;
            if (phone && !phoneRegex.test(phone)) {
                alert('Please enter a valid 10-digit phone number.');
                e.preventDefault();
                return;
            }

            if (farmSize && isNaN(parseFloat(farmSize))) {
                alert('Farm size must be a number.');
                e.preventDefault();
                return;
            }
        });
    }
}
