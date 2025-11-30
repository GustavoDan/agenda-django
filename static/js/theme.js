class ThemeManager {
    constructor() {
        this.theme = this.getStoredTheme() || this.getSystemTheme();
        this.init();
    }

    getSystemTheme() {
        return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    }

    getStoredTheme() {
        return localStorage.getItem('theme');
    }

    setTheme(theme) {
        this.theme = theme;
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);
        this.updateToggleIcon();
    }

    toggle() {
        const newTheme = this.theme === 'dark' ? 'light' : 'dark';
        this.setTheme(newTheme);
    }

    updateToggleIcon() {
        const toggle = document.getElementById('theme-toggle');
        if (!toggle) return;

        const sunIcon = toggle.querySelector('.sun-icon');
        const moonIcon = toggle.querySelector('.moon-icon');

        if (this.theme === 'dark') {
            sunIcon.style.display = 'block';
            moonIcon.style.display = 'none';
        } else {
            sunIcon.style.display = 'none';
            moonIcon.style.display = 'block';
        }
    }

    init() {
        document.documentElement.setAttribute('data-theme', this.theme);
        
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.setupToggle());
        } else {
            this.setupToggle();
        }

        setTimeout(() => {
            document.body.classList.remove('prevent-transition-on-load');
        }, 100);

        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
            if (!this.getStoredTheme()) {
                this.setTheme(e.matches ? 'dark' : 'light');
            }
        });
    }

    setupToggle() {
        const toggle = document.getElementById('theme-toggle');
        if (toggle) {
            this.updateToggleIcon();
            toggle.addEventListener('click', () => this.toggle());
        }
    }
}

const themeManager = new ThemeManager();

