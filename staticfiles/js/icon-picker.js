// Icon Picker JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Initialize any icon pickers on the page
    initializeIconPickers();
});

function initializeIconPickers() {
    // Find all icon picker containers
    const iconPickers = document.querySelectorAll('.icon-picker-container');
    
    iconPickers.forEach(function(picker) {
        const selected = picker.querySelector('.icon-picker-selected');
        const dropdown = picker.querySelector('.icon-picker-dropdown');
        const input = picker.querySelector('input[type="hidden"]');
        const searchInput = picker.querySelector('.icon-picker-search');
        
        if (selected && dropdown) {
            // Toggle dropdown when clicking on the selected item
            selected.addEventListener('click', function(e) {
                e.stopPropagation();
                
                if (dropdown.style.display === 'none' || !dropdown.style.display) {
                    dropdown.style.display = 'block';
                    
                    // Adjust position if too close to right edge
                    adjustDropdownPosition(dropdown);
                    
                    // Focus search input if it exists
                    if (searchInput) {
                        setTimeout(function() {
                            searchInput.focus();
                        }, 100);
                    }
                } else {
                    dropdown.style.display = 'none';
                }
            });
            
            // Close dropdown when clicking outside
            document.addEventListener('click', function(e) {
                if (!dropdown.contains(e.target) && !selected.contains(e.target)) {
                    dropdown.style.display = 'none';
                }
            });
            
            // Handle window resize
            window.addEventListener('resize', function() {
                if (dropdown.style.display === 'block') {
                    adjustDropdownPosition(dropdown);
                }
            });
            
            // Set up icon selection
            const icons = dropdown.querySelectorAll('.icon-item');
            icons.forEach(function(icon) {
                icon.addEventListener('click', function() {
                    const iconClass = this.getAttribute('data-icon');
                    const iconLabel = this.getAttribute('data-label');
                    
                    // Update hidden input
                    if (input) {
                        input.value = iconClass;
                        
                        // Trigger change event for form validation
                        const event = new Event('change', { bubbles: true });
                        input.dispatchEvent(event);
                    }
                    
                    // Update selected display
                    const iconElement = selected.querySelector('i');
                    const labelElement = selected.querySelector('span');
                    
                    if (iconElement) {
                        iconElement.className = iconClass;
                    }
                    
                    if (labelElement) {
                        labelElement.textContent = iconLabel;
                    }
                    
                    // Highlight selected icon
                    icons.forEach(function(i) {
                        i.classList.remove('selected');
                    });
                    this.classList.add('selected');
                    
                    // Close dropdown
                    dropdown.style.display = 'none';
                });
            });
            
            // Set up search functionality
            if (searchInput) {
                searchInput.addEventListener('input', function() {
                    const query = this.value.toLowerCase();
                    let visibleCount = 0;
                    
                    icons.forEach(function(icon) {
                        const label = icon.getAttribute('data-label').toLowerCase();
                        if (label.includes(query)) {
                            icon.style.display = 'flex';
                            visibleCount++;
                        } else {
                            icon.style.display = 'none';
                        }
                    });
                    
                    // Show a message if no results found
                    let noResultsMsg = dropdown.querySelector('.no-results-message');
                    if (visibleCount === 0) {
                        if (!noResultsMsg) {
                            const grid = dropdown.querySelector('.icon-picker-grid');
                            noResultsMsg = document.createElement('div');
                            noResultsMsg.className = 'no-results-message';
                            noResultsMsg.style.gridColumn = '1 / -1';
                            noResultsMsg.style.padding = '20px';
                            noResultsMsg.style.textAlign = 'center';
                            noResultsMsg.style.color = '#666';
                            noResultsMsg.textContent = 'No icons found matching your search.';
                            grid.appendChild(noResultsMsg);
                        } else {
                            noResultsMsg.style.display = 'block';
                        }
                    } else if (noResultsMsg) {
                        noResultsMsg.style.display = 'none';
                    }
                });
            }
        }
    });
}

function adjustDropdownPosition(dropdown) {
    const rect = dropdown.getBoundingClientRect();
    
    // If dropdown extends beyond right edge of viewport
    if (rect.right > window.innerWidth) {
        // Calculate how much to shift left
        const shiftLeft = Math.min(rect.right - window.innerWidth + 20, rect.left - 20);
        dropdown.style.left = -shiftLeft + 'px';
    }
} 