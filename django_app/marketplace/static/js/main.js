
function initializeFormValidation() {
    (function() {
        'use strict';
        window.addEventListener('load', function() {
            const forms = document.querySelectorAll('.needs-validation');
            Array.from(forms).forEach(function(form) {
                form.addEventListener('submit', function(event) {
                    if (!form.checkValidity()) {
                        event.preventDefault();
                        event.stopPropagation();
                    }
                    form.classList.add('was-validated');
                }, false);
            });
        }, false);
    })();
}


function initializeFieldValidation() {
    const fields = document.querySelectorAll('.form-control, .form-select');
    
    fields.forEach(field => {
        field.addEventListener('blur', function() {
            validateField(this);
        });
        
        field.addEventListener('input', function() {
            if (this.classList.contains('is-invalid')) {
                validateField(this);
            }
        });
    });
}


function validateField(field) {
    const validators = {
        email: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
        phone: /^\+?[\d\s\-()]{10,}$/,
        url: /^https?:\/\/.+/i,
        number: /^\d+(\.\d+)?$/
    };
    
    const type = field.type || field.dataset.validation;
    const value = field.value.trim();
    
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


function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}


function initializePopovers() {
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
}


function setButtonLoading(button, isLoading = true) {
    if (isLoading) {
        button.disabled = true;
        button.dataset.originalText = button.innerHTML;
        button.innerHTML = `
            <span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
            Loading...
        `;
        button.classList.add('btn-loading');
    } else {
        button.disabled = false;
        button.innerHTML = button.dataset.originalText;
        button.classList.remove('btn-loading');
    }
}


function showLoadingOverlay(show = true) {
    let overlay = document.getElementById('loadingOverlay');
    
    if (!overlay && show) {
        overlay = document.createElement('div');
        overlay.id = 'loadingOverlay';
        overlay.className = 'loading-overlay';
        overlay.innerHTML = `
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        `;
        document.body.appendChild(overlay);
    }
    
    if (overlay) {
        overlay.classList.toggle('hidden', !show);
    }
}


function showAlert(message, type = 'info', duration = 5000) {
    const alertHTML = `
        <div class="alert alert-${type} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    const container = document.querySelector('main') || document.body;
    const alertElement = document.createElement('div');
    alertElement.innerHTML = alertHTML;
    container.insertBefore(alertElement.firstElementChild, container.firstChild);
    
    if (duration > 0) {
        setTimeout(() => {
            const alert = container.querySelector('.alert');
            if (alert) {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }
        }, duration);
    }
}


function copyToClipboard(text, showMessage = true) {
    navigator.clipboard.writeText(text).then(() => {
        if (showMessage) {
            showAlert('Copied to clipboard!', 'success', 3000);
        }
        return true;
    }).catch(err => {
        console.error('Failed to copy:', err);
        return false;
    });
}

function initializeStarRating() {
    const ratingContainers = document.querySelectorAll('[data-rating-input]');
    
    ratingContainers.forEach(container => {
        const input = document.getElementById(container.dataset.ratingInput);
        if (!input) return;
        
        const stars = container.querySelectorAll('.star');
        
        stars.forEach((star, index) => {
            star.addEventListener('click', () => {
                const rating = index + 1;
                input.value = rating;
                updateStars(container, rating);
                input.dispatchEvent(new Event('change', { bubbles: true }));
            });
            
            star.addEventListener('mouseover', () => {
                updateStars(container, index + 1);
            });
        });
        
        container.addEventListener('mouseleave', () => {
            const currentRating = input.value || 0;
            updateStars(container, currentRating);
        });
    });
}


function updateStars(container, rating) {
    const stars = container.querySelectorAll('.star');
    stars.forEach((star, index) => {
        if (index < rating) {
            star.classList.remove('star-empty');
            star.classList.add('star-filled');
        } else {
            star.classList.remove('star-filled');
            star.classList.add('star-empty');
        }
    });
}


function resetForm(formSelector) {
    const form = document.querySelector(formSelector);
    if (form) {
        form.reset();
        form.classList.remove('was-validated');
        const fields = form.querySelectorAll('.form-control, .form-select');
        fields.forEach(field => {
            field.classList.remove('is-valid', 'is-invalid');
        });
    }
}


function clearFormErrors(formSelector) {
    const form = document.querySelector(formSelector);
    if (form) {
        const fields = form.querySelectorAll('.is-invalid');
        fields.forEach(field => {
            field.classList.remove('is-invalid');
            const feedback = field.nextElementSibling;
            if (feedback && feedback.classList.contains('invalid-feedback')) {
                feedback.remove();
            }
        });
    }
}


function populateForm(formSelector, data) {
    const form = document.querySelector(formSelector);
    if (!form) return;
    
    Object.keys(data).forEach(key => {
        const field = form.querySelector(`[name="${key}"]`);
        if (field) {
            if (field.type === 'checkbox' || field.type === 'radio') {
                field.checked = data[key];
            } else {
                field.value = data[key];
            }
        }
    });
}


function serializeForm(formSelector) {
    const form = document.querySelector(formSelector);
    if (!form) return {};
    
    const formData = new FormData(form);
    const data = {};
    
    for (let [key, value] of formData.entries()) {
        if (data[key]) {
            if (Array.isArray(data[key])) {
                data[key].push(value);
            } else {
                data[key] = [data[key], value];
            }
        } else {
            data[key] = value;
        }
    }
    
    return data;
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


function initializeLiveSearch(inputSelector, onSearch) {
    const input = document.querySelector(inputSelector);
    if (!input) return;
    
    input.addEventListener('input', debounce((e) => {
        const query = e.target.value.trim();
        onSearch(query);
    }, 300));
}


function filterItems(containerSelector, itemSelector, searchQuery, searchFields = ['textContent']) {
    const container = document.querySelector(containerSelector);
    if (!container) return;
    
    const items = container.querySelectorAll(itemSelector);
    let visibleCount = 0;
    
    items.forEach(item => {
        const matches = searchFields.some(field => {
            const text = field === 'textContent' ? 
                item.textContent.toLowerCase() : 
                (item.dataset[field] || '').toLowerCase();
            return text.includes(searchQuery.toLowerCase());
        });
        
        item.style.display = matches ? '' : 'none';
        if (matches) visibleCount++;
    });
    
    const noResultsMsg = container.querySelector('.no-results');
    if (noResultsMsg) {
        noResultsMsg.style.display = visibleCount === 0 ? 'block' : 'none';
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


function addAnimatedClass(selector, className, duration = 500) {
    const element = document.querySelector(selector);
    if (element) {
        element.classList.add(className);
        setTimeout(() => {
            element.classList.remove(className);
        }, duration);
    }
}


function smoothScrollTo(selector) {
    const element = document.querySelector(selector);
    if (element) {
        element.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}



async function ajaxRequest(url, method = 'GET', data = null, headers = {}) {
    try {
        const options = {
            method: method,
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
                ...headers
            }
        };
        
        if (data && (method === 'POST' || method === 'PUT' || method === 'PATCH')) {
            options.body = JSON.stringify(data);
        }
        
        const response = await fetch(url, options);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const contentType = response.headers.get('content-type');
        if (contentType && contentType.includes('application/json')) {
            return await response.json();
        } else {
            return await response.text();
        }
    } catch (error) {
        console.error('AJAX request failed:', error);
        throw error;
    }
}


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.addEventListener('DOMContentLoaded', function() {
    initializeFormValidation();
    initializeFieldValidation();
    initializeTooltips();
    initializePopovers();
    initializeStarRating();
    
    console.log('✓ Marketplace scripts initialized');
});

window.MarketplaceUtils = {
    showAlert,
    showLoadingOverlay,
    setButtonLoading,
    copyToClipboard,
    resetForm,
    clearFormErrors,
    populateForm,
    serializeForm,
    filterItems,
    toggleElement,
    addAnimatedClass,
    smoothScrollTo,
    ajaxRequest,
    debounce
};
