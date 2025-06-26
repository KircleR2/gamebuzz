(function($) {
    $(document).ready(function() {
        // Initialize icon picker
        function initIconPicker() {
            $('.icon-picker-select').each(function() {
                const select = $(this);
                const preview = select.next('.icon-picker-container').find('.icon-preview i');
                
                // Update preview when selection changes
                select.on('change', function() {
                    const selectedIcon = $(this).val();
                    preview.attr('class', selectedIcon);
                });
                
                // Add icons to dropdown options
                select.find('option').each(function() {
                    const iconClass = $(this).val();
                    const iconName = $(this).text();
                    
                    if (iconClass) {
                        // Store original text
                        $(this).data('original-text', iconName);
                        
                        // Set new text with icon
                        $(this).html(`<i class="${iconClass}"></i> ${iconName}`);
                    }
                });
            });
        }
        
        // Initialize on page load
        initIconPicker();
        
        // Also initialize when Django admin adds a new inline form
        $(document).on('formset:added', function() {
            initIconPicker();
        });
    });
})(django.jQuery); 