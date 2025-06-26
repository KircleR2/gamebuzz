// GameBuzz JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initSearch();
    initSmoothScrolling();
    initNewsletterForm();
    initMobileMenu();
    initLazyLoading();
    initAnimations();
    initEventCardEffects();
    initStatsAnimation();
    loadHeroEvents(); // Load hero events from API and initialize slider
});

// Search functionality
function initSearch() {
    const searchForm = document.querySelector('.hero-search');
    const searchInput = document.querySelector('.hero-search-input');
    
    if (searchForm && searchInput) {
        searchForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const query = searchInput.value.trim();
            if (query) {
                // Redirect to search results page
                window.location.href = `/events/search/?q=${encodeURIComponent(query)}`;
            }
        });
    }
}

// Smooth scrolling for anchor links
function initSmoothScrolling() {
    const links = document.querySelectorAll('a[href^="#"]');
    
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Newsletter form submission
function initNewsletterForm() {
    const newsletterForm = document.querySelector('.newsletter-form');
    
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const emailInput = this.querySelector('.newsletter-input');
            const submitButton = this.querySelector('.newsletter-button');
            const email = emailInput.value.trim();
            
            if (email && isValidEmail(email)) {
                // Disable button and show loading state
                submitButton.disabled = true;
                submitButton.textContent = 'Subscribing...';
                
                // Send subscription request to backend
                fetch('/api/newsletter/subscribe/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    body: JSON.stringify({ email: email })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'reactivated') {
                        showNotification(data.message, 'success');
                    } else if (data.message) {
                        showNotification(data.message, 'success');
                    } else {
                        showNotification('Successfully subscribed to our newsletter!', 'success');
                    }
                    emailInput.value = '';
                })
                .catch(error => {
                    console.error('Error:', error);
                    showNotification('Something went wrong. Please try again.', 'error');
                })
                .finally(() => {
                    // Re-enable button
                    submitButton.disabled = false;
                    submitButton.textContent = 'Subscribe';
                });
            } else {
                showNotification('Please enter a valid email address.', 'error');
            }
        });
    }
}

// Get CSRF token from cookies
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

// Mobile menu toggle
function initMobileMenu() {
    const mobileMenuButton = document.querySelector('.mobile-menu-button');
    const mobileMenu = document.querySelector('.mobile-menu');
    
    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', function() {
            mobileMenu.classList.toggle('active');
            this.classList.toggle('active');
        });
        
        // Close menu when clicking outside
        document.addEventListener('click', function(e) {
            if (!mobileMenu.contains(e.target) && !mobileMenuButton.contains(e.target)) {
                mobileMenu.classList.remove('active');
                mobileMenuButton.classList.remove('active');
            }
        });
    }
}

// Lazy loading for images
function initLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');
    
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        images.forEach(img => imageObserver.observe(img));
    } else {
        // Fallback for older browsers
        images.forEach(img => {
            img.src = img.dataset.src;
            img.classList.remove('lazy');
        });
    }
}

// Animations on scroll
function initAnimations() {
    const animatedElements = document.querySelectorAll('.animate-on-scroll');
    
    if ('IntersectionObserver' in window) {
        const animationObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animated');
                }
            });
        }, {
            threshold: 0.1
        });
        
        animatedElements.forEach(el => animationObserver.observe(el));
    }
}

// Utility functions
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    // Add styles
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        border-radius: 0.5rem;
        color: white;
        font-weight: 500;
        z-index: 1000;
        transform: translateX(100%);
        transition: transform 0.3s ease;
        max-width: 300px;
    `;
    
    // Set background color based on type
    switch (type) {
        case 'success':
            notification.style.backgroundColor = '#10B981';
            break;
        case 'error':
            notification.style.backgroundColor = '#EF4444';
            break;
        default:
            notification.style.backgroundColor = '#2563EB';
    }
    
    // Add to page
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Remove after 5 seconds
    setTimeout(() => {
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 5000);
}

// Category filter functionality
function filterEvents(category) {
    const eventCards = document.querySelectorAll('.event-card');
    
    eventCards.forEach(card => {
        const cardCategory = card.dataset.category;
        
        if (category === 'all' || cardCategory === category) {
            card.style.display = 'block';
            card.style.animation = 'fadeIn 0.3s ease';
        } else {
            card.style.display = 'none';
        }
    });
    
    // Update active filter button
    const filterButtons = document.querySelectorAll('.filter-button');
    filterButtons.forEach(btn => {
        btn.classList.remove('active');
        if (btn.dataset.category === category) {
            btn.classList.add('active');
        }
    });
}

// Event card hover effects
function initEventCardEffects() {
    const eventCards = document.querySelectorAll('.event-card');
    
    eventCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
}

// Stats counter animation
function animateStats() {
    const statNumbers = document.querySelectorAll('.stat-number');
    
    statNumbers.forEach(stat => {
        const target = parseInt(stat.textContent.replace(/\D/g, ''));
        const suffix = stat.textContent.replace(/\d/g, '');
        let current = 0;
        const increment = target / 50;
        
        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                current = target;
                clearInterval(timer);
            }
            stat.textContent = Math.floor(current) + suffix;
        }, 30);
    });
}

// Initialize stats animation when stats section is visible
function initStatsAnimation() {
    const statsSection = document.querySelector('.stats');
    
    if (statsSection && 'IntersectionObserver' in window) {
        const statsObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    animateStats();
                    statsObserver.unobserve(entry.target);
                }
            });
        });
        
        statsObserver.observe(statsSection);
    }
}

// Hero slider functionality
function initHeroSlider() {
    const heroSlider = document.querySelector('.hero-slider');
    const heroSlides = document.querySelectorAll('.hero-slide');
    const sliderDots = document.querySelectorAll('.hero-slider-dot');
    
    if (!heroSlider || heroSlides.length === 0) return;
    
    let currentSlide = 0;
    
    // Add click handlers to slides
    heroSlides.forEach(slide => {
        const eventSlug = slide.getAttribute('data-event-slug');
        slide.addEventListener('click', function() {
            if (eventSlug) {
                window.location.href = `/event/${eventSlug}/`;
            }
        });
    });
    
    let slideInterval;
    
    // Show first slide
    showSlide(0);
    
    // Auto-rotate slides
    function startAutoRotate() {
        slideInterval = setInterval(() => {
            currentSlide = (currentSlide + 1) % heroSlides.length;
            showSlide(currentSlide);
        }, 5000); // Change slide every 5 seconds
    }
    
    // Stop auto-rotation
    function stopAutoRotate() {
        if (slideInterval) {
            clearInterval(slideInterval);
        }
    }
    
    // Show specific slide
    function showSlide(index) {
        // Hide all slides and disable pointer events
        heroSlides.forEach(slide => {
            slide.classList.remove('active');
            slide.style.pointerEvents = 'none';
        });
        
        // Remove active class from all dots
        sliderDots.forEach(dot => {
            dot.classList.remove('active');
        });
        
        // Show current slide and enable pointer events
        if (heroSlides[index]) {
            heroSlides[index].classList.add('active');
            heroSlides[index].style.pointerEvents = 'auto';
        }
        
        // Activate current dot
        if (sliderDots[index]) {
            sliderDots[index].classList.add('active');
        }
        
        currentSlide = index;
    }
    
    // Add click handlers to dots
    sliderDots.forEach((dot, index) => {
        dot.addEventListener('click', (e) => {
            e.stopPropagation(); // Prevent slide click when clicking dot
            showSlide(index);
            stopAutoRotate();
            startAutoRotate(); // Restart auto-rotation
        });
    });
    
    // Pause auto-rotation on hover
    heroSlider.addEventListener('mouseenter', stopAutoRotate);
    heroSlider.addEventListener('mouseleave', startAutoRotate);
    
    // Start auto-rotation
    startAutoRotate();
    
    // Add keyboard navigation
    document.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowLeft') {
            currentSlide = (currentSlide - 1 + heroSlides.length) % heroSlides.length;
            showSlide(currentSlide);
            stopAutoRotate();
            startAutoRotate();
        } else if (e.key === 'ArrowRight') {
            currentSlide = (currentSlide + 1) % heroSlides.length;
            showSlide(currentSlide);
            stopAutoRotate();
            startAutoRotate();
        }
    });
    
    // Add touch/swipe support for mobile
    let touchStartX = 0;
    let touchEndX = 0;
    
    heroSlider.addEventListener('touchstart', (e) => {
        touchStartX = e.changedTouches[0].screenX;
    });
    
    heroSlider.addEventListener('touchend', (e) => {
        touchEndX = e.changedTouches[0].screenX;
        handleSwipe();
    });
    
    function handleSwipe() {
        const swipeThreshold = 50;
        const diff = touchStartX - touchEndX;
        
        if (Math.abs(diff) > swipeThreshold) {
            if (diff > 0) {
                // Swipe left - next slide
                currentSlide = (currentSlide + 1) % heroSlides.length;
            } else {
                // Swipe right - previous slide
                currentSlide = (currentSlide - 1 + heroSlides.length) % heroSlides.length;
            }
            showSlide(currentSlide);
            stopAutoRotate();
            startAutoRotate();
        }
    }
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .animate-on-scroll {
        opacity: 0;
        transform: translateY(30px);
        transition: all 0.6s ease;
    }
    
    .animate-on-scroll.animated {
        opacity: 1;
        transform: translateY(0);
    }
    
    .filter-button {
        transition: all 0.2s ease;
    }
    
    .filter-button.active {
        background-color: var(--primary-blue);
        color: white;
    }
    
    .event-card {
        transition: all 0.3s ease;
    }
    
    .mobile-menu {
        transform: translateX(-100%);
        transition: transform 0.3s ease;
    }
    
    .mobile-menu.active {
        transform: translateX(0);
    }
    
    .mobile-menu-button {
        transition: all 0.3s ease;
    }
    
    .mobile-menu-button.active .hamburger-line:nth-child(1) {
        transform: rotate(45deg) translate(5px, 5px);
    }
    
    .mobile-menu-button.active .hamburger-line:nth-child(2) {
        opacity: 0;
    }
    
    .mobile-menu-button.active .hamburger-line:nth-child(3) {
        transform: rotate(-45deg) translate(7px, -6px);
    }
`;
document.head.appendChild(style);

// Load hero events from API
function loadHeroEvents() {
    const heroSection = document.querySelector('.hero');
    if (!heroSection) return;
    
    // Check if we already have hero events (from template)
    const existingHeroEvents = document.querySelectorAll('.hero-slide');
    if (existingHeroEvents.length > 0) {
        // Hero events already loaded from template, just initialize slider
        initHeroSlider();
        return;
    }
    
    // Load hero events from API only if none exist in template
    fetch('/api/homepage/hero-events/')
        .then(response => response.json())
        .then(events => {
            if (events && events.length > 0) {
                updateHeroSection(events);
            }
        })
        .catch(error => {
            console.error('Error loading hero events:', error);
        });
}

// Update hero section with dynamic events
function updateHeroSection(events) {
    const heroSection = document.querySelector('.hero');
    if (!heroSection) return;
    
    // Create dynamic hero content - simplified without event data overlay
    const heroHTML = `
        <div class="hero-slider">
            ${events.map((event, index) => `
                <div class="hero-slide ${index === 0 ? 'active' : ''}" 
                     style="background-image: url('${event.hero_image || event.featured_image || 'https://images.unsplash.com/photo-1542751371-adc38448a05e?q=80&w=2070&auto=format&fit=crop'}')"
                     data-event-slug="${event.slug}">
                    <div class="hero-overlay"></div>
                    <div class="hero-content"></div>
                </div>
            `).join('')}
        </div>
        
        ${events.length > 1 ? `
            <div class="hero-slider-nav">
                ${events.map((_, index) => `
                    <button class="hero-slider-dot ${index === 0 ? 'active' : ''}" data-slide="${index}"></button>
                `).join('')}
            </div>
        ` : ''}
    `;
    
    // Replace static hero content with dynamic content
    heroSection.innerHTML = heroHTML;
    heroSection.classList.add('hero-dynamic');
    
    // Initialize slider after updating content
    initHeroSlider();
}

// Format date for display
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
        month: 'short', 
        day: 'numeric', 
        year: 'numeric' 
    });
}

// Format time for display
function formatTime(timeString) {
    const time = new Date(`2000-01-01T${timeString}`);
    return time.toLocaleTimeString('en-US', { 
        hour: 'numeric', 
        minute: '2-digit',
        hour12: true 
    });
} 