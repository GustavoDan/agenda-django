class ToastManager {
    constructor() {
        this.container = document.getElementById('toast-container');
        this.toasts = [];
        this.maxToasts = 5;
    }

    show(message, type = 'info', duration = 5000) {
        const toast = this.createToast(message, type);
        this.container.appendChild(toast);
        this.toasts.push(toast);

        setTimeout(() => {
            toast.classList.add('toast-show');
        }, 10);

        setTimeout(() => {
            this.remove(toast);
        }, duration);

        if (this.toasts.length > this.maxToasts) {
            this.remove(this.toasts[0]);
        }
    }

    createToast(message, type) {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        
        const icons = {
            'success': '✓',
            'error': '✕',
            'warning': '⚠',
            'info': 'ℹ'
        };

        toast.innerHTML = `
            <div class="toast-content">
                <span class="toast-icon">${icons[type] || icons.info}</span>
                <span class="toast-message">${message}</span>
            </div>
            <button class="toast-close" onclick="toastManager.remove(this.parentElement)">×</button>
        `;

        return toast;
    }

    remove(toast) {
        if (!toast || !toast.parentElement) return;
        
        toast.classList.add('toast-hide');
        
        setTimeout(() => {
            if (toast.parentElement) {
                toast.parentElement.removeChild(toast);
            }
            this.toasts = this.toasts.filter(t => t !== toast);
        }, 300);
    }

    clear() {
        this.toasts.forEach(toast => this.remove(toast));
    }
}

const toastManager = new ToastManager();

function initToasts() {
    if (typeof djangoMessages !== 'undefined' && djangoMessages.length > 0) {
        djangoMessages.forEach((msg, index) => {
            let type = msg.type || 'info';
            
            const typeMap = {
                'success': 'success',
                'error': 'error',
                'warning': 'warning',
                'info': 'info',
                'debug': 'info',
                '': 'info'
            };
            
            type = typeMap[type] || 'info';
            
            setTimeout(() => {
                toastManager.show(msg.text, type, 5000);
            }, index * 100);
        });
    }
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initToasts);
} else {
    setTimeout(initToasts, 100);
}
