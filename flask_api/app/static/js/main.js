
function initializeFormValidation() {
    'use strict';
    const forms = document.querySelectorAll('.needs-validation');
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
}


function initializeFieldValidation() {
    const fields = document.querySelectorAll('.form-control, .form-select');
    
    fields.forEach(field => {
        field.addEventListener('blur', function() {
            validateField(this);
        });
    });
}


function validateField(field) {
    const validators = {
        email: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
        password: /.{6,}/,
        phone: /^\+?[\d\s\-()]{10,}$/,
    };
    
    const type = field.type || field.dataset.validation;
    const value = field.value.trim();
    
    if (!value && field.hasAttribute('required')) {
        updateFieldValidation(field, false);
        return false;
    }
    
    if (!value) return true;
    
    if (type && validators[type]) {
        const isValid = validators[type].test(value);
        updateFieldValidation(field, isValid);
        return isValid;
    }
    
    return true;
}


function updateFieldValidation(field, isValid) {
    if (isValid) {
        field.classList.remove('is-invalid');
        field.classList.add('is-valid');
    } else {
        field.classList.remove('is-valid');
        field.classList.add('is-invalid');
    }
}


function showAlert(message, type = 'info', duration = 5000) {
    const alertHTML = `
        <div class="alert alert-${type} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    const container = document.querySelector('main') || document.querySelector('.container');
    if (!container) return;
    
    const alertElement = document.createElement('div');
    alertElement.innerHTML = alertHTML;
    container.insertBefore(alertElement.firstElementChild, container.firstChild);
    
    if (duration > 0) {
        setTimeout(() => {
            const alert = container.querySelector('.alert');
            if (alert) {
                alert.remove();
            }
        }, duration);
    }
}


function setButtonLoading(button, isLoading = true) {
    if (isLoading) {
        button.disabled = true;
        button.dataset.originalText = button.innerHTML;
        button.innerHTML = `
            <span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
            Loading...
        `;
    } else {
        button.disabled = false;
        button.innerHTML = button.dataset.originalText;
    }
}


function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}


function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}


function getValue(selector) {
    const element = document.querySelector(selector);
    return element ? element.value : null;
}


function setValue(selector, value) {
    const element = document.querySelector(selector);
    if (element) {
        element.value = value;
    }
}


function toggleElement(selector, forceShow = null) {
    const element = document.querySelector(selector);
    if (element) {
        if (forceShow !== null) {
            element.style.display = forceShow ? '' : 'none';
        } else {
            element.style.display = element.style.display === 'none' ? '' : 'none';
        }
    }
}


document.addEventListener('DOMContentLoaded', function() {
    initializeFormValidation();
    initializeFieldValidation();
    initializeTooltips();
    
    console.log(' Flask Marketplace scripts initialized');
});


window.FlaskUtils = {
    showAlert,
    setButtonLoading,
    debounce,
    getValue,
    setValue,
    toggleElement,
    validateField
};
