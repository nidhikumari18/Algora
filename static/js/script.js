// Toggle mobile menu
function toggleMenu() {
  const navMenu = document.querySelector('.nav-menu');
  navMenu.classList.toggle('active');
}

// Close alerts automatically
function closeAlert(element) {
  element.style.display = 'none';
}

// Auto-close alerts after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
  const alerts = document.querySelectorAll('.alert');
  alerts.forEach(alert => {
    setTimeout(() => {
      alert.style.animation = 'slideUp 0.3s ease';
      setTimeout(() => {
        alert.style.display = 'none';
      }, 300);
    }, 5000);
  });
});

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      target.scrollIntoView({
        behavior: 'smooth',
        block: 'start'
      });
    }
  });
});

// Add animation on scroll
const observerOptions = {
  threshold: 0.1,
  rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver(function(entries) {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.style.animation = 'slideUp 0.6s ease';
      observer.unobserve(entry.target);
    }
  });
}, observerOptions);

document.querySelectorAll('.subject-card, .feature-card, .chapter-card, .resource-card').forEach(el => {
  el.style.opacity = '0';
  observer.observe(el);
});

// Form validation
function validateForm(formId) {
  const form = document.getElementById(formId);
  if (!form) return true;

  const inputs = form.querySelectorAll('input[required], textarea[required], select[required]');
  let isValid = true;

  inputs.forEach(input => {
    if (!input.value.trim()) {
      input.style.borderColor = '#e53935';
      isValid = false;
    } else {
      input.style.borderColor = '';
    }
  });

  return isValid;
}

// Confirm before delete
function confirmDelete(message = 'Are you sure you want to delete this?') {
  return confirm(message);
}

// Copy to clipboard
function copyToClipboard(text, message = 'Copied!') {
  navigator.clipboard.writeText(text).then(() => {
    const originalText = event.target.textContent;
    event.target.textContent = message;
    setTimeout(() => {
      event.target.textContent = originalText;
    }, 2000);
  });
}

// Debounce function for search
function debounce(func, delay) {
  let timeoutId;
  return function(...args) {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => func(...args), delay);
  };
}

// Add CSS animation keyframes dynamically
const style = document.createElement('style');
style.textContent = `
  @keyframes slideUp {
    from {
      opacity: 0;
      transform: translateY(20px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
`;
document.head.appendChild(style);
