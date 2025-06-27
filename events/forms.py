from django import forms
from django.utils.html import format_html
from django.utils.safestring import mark_safe

# Expanded list of Bootstrap icons for the dropdown
BOOTSTRAP_ICONS = [
    # Gaming & Entertainment
    ('bi-controller', 'Game Controller'),
    ('bi-joystick', 'Joystick'),
    ('bi-dice-5', 'Dice'),
    ('bi-puzzle', 'Puzzle'),
    ('bi-trophy', 'Trophy'),
    ('bi-award', 'Award'),
    ('bi-lightning', 'Lightning'),
    ('bi-stars', 'Stars'),
    ('bi-fire', 'Fire'),
    ('bi-emoji-smile', 'Smile'),
    ('bi-emoji-sunglasses', 'Cool'),
    ('bi-emoji-wink', 'Wink'),
    ('bi-emoji-heart-eyes', 'Love'),
    ('bi-emoji-laughing', 'Laugh'),
    
    # Media & Content
    ('bi-film', 'Film'),
    ('bi-camera', 'Camera'),
    ('bi-camera-video', 'Video Camera'),
    ('bi-music-note', 'Music'),
    ('bi-music-player', 'Music Player'),
    ('bi-headphones', 'Headphones'),
    ('bi-mic', 'Microphone'),
    ('bi-broadcast', 'Broadcast'),
    ('bi-tv', 'TV'),
    ('bi-display', 'Display'),
    ('bi-laptop', 'Laptop'),
    ('bi-phone', 'Phone'),
    ('bi-tablet', 'Tablet'),
    ('bi-book', 'Book'),
    ('bi-newspaper', 'Newspaper'),
    
    # Events & Calendar
    ('bi-calendar-event', 'Calendar Event'),
    ('bi-calendar-date', 'Calendar Date'),
    ('bi-calendar-check', 'Calendar Check'),
    ('bi-calendar-plus', 'Calendar Plus'),
    ('bi-calendar-week', 'Calendar Week'),
    ('bi-alarm', 'Alarm'),
    ('bi-clock', 'Clock'),
    ('bi-hourglass', 'Hourglass'),
    ('bi-stopwatch', 'Stopwatch'),
    
    # People & Social
    ('bi-people', 'People'),
    ('bi-person', 'Person'),
    ('bi-person-plus', 'Person Add'),
    ('bi-person-check', 'Person Check'),
    ('bi-person-badge', 'Person Badge'),
    ('bi-person-lines-fill', 'Person Details'),
    ('bi-chat', 'Chat'),
    ('bi-chat-dots', 'Chat Dots'),
    ('bi-chat-square', 'Chat Square'),
    ('bi-chat-quote', 'Chat Quote'),
    ('bi-megaphone', 'Megaphone'),
    ('bi-share', 'Share'),
    
    # Location & Travel
    ('bi-geo-alt', 'Location'),
    ('bi-map', 'Map'),
    ('bi-pin-map', 'Pin Map'),
    ('bi-compass', 'Compass'),
    ('bi-globe', 'Globe'),
    ('bi-house', 'House'),
    ('bi-building', 'Building'),
    ('bi-shop', 'Shop'),
    ('bi-signpost', 'Signpost'),
    ('bi-car-front', 'Car'),
    ('bi-truck', 'Truck'),
    ('bi-bus-front', 'Bus'),
    ('bi-airplane', 'Airplane'),
    ('bi-train-front', 'Train'),
    
    # Food & Drinks
    ('bi-cup', 'Cup'),
    ('bi-cup-hot', 'Hot Drink'),
    ('bi-cup-straw', 'Drink'),
    ('bi-egg', 'Egg'),
    ('bi-basket', 'Basket'),
    ('bi-cart', 'Cart'),
    ('bi-bag', 'Bag'),
    
    # UI Elements
    ('bi-bell', 'Bell'),
    ('bi-envelope', 'Envelope'),
    ('bi-search', 'Search'),
    ('bi-star', 'Star'),
    ('bi-heart', 'Heart'),
    ('bi-bookmark', 'Bookmark'),
    ('bi-flag', 'Flag'),
    ('bi-tag', 'Tag'),
    ('bi-tags', 'Tags'),
    ('bi-link', 'Link'),
    ('bi-eye', 'Eye'),
    ('bi-hand-thumbs-up', 'Thumbs Up'),
    ('bi-hand-thumbs-down', 'Thumbs Down'),
    
    # Tech & Devices
    ('bi-cpu', 'CPU'),
    ('bi-gpu-card', 'GPU'),
    ('bi-hdd', 'Hard Drive'),
    ('bi-usb-drive', 'USB Drive'),
    ('bi-router', 'Router'),
    ('bi-bluetooth', 'Bluetooth'),
    ('bi-wifi', 'WiFi'),
    ('bi-cast', 'Cast'),
    ('bi-battery', 'Battery'),
    ('bi-power', 'Power'),
    ('bi-lightning-charge', 'Charging'),
    
    # Business & Commerce
    ('bi-briefcase', 'Briefcase'),
    ('bi-cash', 'Cash'),
    ('bi-credit-card', 'Credit Card'),
    ('bi-wallet', 'Wallet'),
    ('bi-currency-dollar', 'Dollar'),
    ('bi-gift', 'Gift'),
    ('bi-ticket', 'Ticket'),
    ('bi-receipt', 'Receipt'),
    ('bi-graph-up', 'Graph Up'),
    ('bi-bar-chart', 'Bar Chart'),
    ('bi-pie-chart', 'Pie Chart'),
    
    # Tools & Settings
    ('bi-gear', 'Gear'),
    ('bi-tools', 'Tools'),
    ('bi-wrench', 'Wrench'),
    ('bi-sliders', 'Sliders'),
    ('bi-toggles', 'Toggles'),
    ('bi-hammer', 'Hammer'),
    ('bi-screwdriver', 'Screwdriver'),
    ('bi-magic', 'Magic'),
    ('bi-palette', 'Palette'),
    ('bi-brush', 'Brush'),
    
    # Arrows & Navigation
    ('bi-arrow-right', 'Arrow Right'),
    ('bi-arrow-left', 'Arrow Left'),
    ('bi-arrow-up', 'Arrow Up'),
    ('bi-arrow-down', 'Arrow Down'),
    ('bi-chevron-right', 'Chevron Right'),
    ('bi-chevron-left', 'Chevron Left'),
    ('bi-chevron-up', 'Chevron Up'),
    ('bi-chevron-down', 'Chevron Down'),
    ('bi-skip-forward', 'Skip Forward'),
    ('bi-skip-backward', 'Skip Backward'),
    ('bi-play', 'Play'),
    ('bi-pause', 'Pause'),
    ('bi-stop', 'Stop'),
    
    # Weather & Nature
    ('bi-cloud', 'Cloud'),
    ('bi-cloud-sun', 'Cloud Sun'),
    ('bi-cloud-rain', 'Rain'),
    ('bi-cloud-snow', 'Snow'),
    ('bi-sun', 'Sun'),
    ('bi-moon', 'Moon'),
    ('bi-wind', 'Wind'),
    ('bi-tornado', 'Tornado'),
    ('bi-tree', 'Tree'),
    ('bi-flower1', 'Flower'),
    ('bi-bug', 'Bug'),
]

class IconGridPickerWidget(forms.Widget):
    """Custom widget for selecting Bootstrap icons using a grid layout"""
    
    class Media:
        css = {
            'all': [
                'https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css',
            ]
        }
    
    def render(self, name, value, attrs=None, renderer=None):
        attrs = attrs or {}
        final_attrs = self.build_attrs(attrs, {'name': name})
        
        # Generate a unique ID for this widget instance
        if 'id' not in final_attrs:
            final_attrs['id'] = f"id_{name}"
        
        widget_id = final_attrs['id']
        dropdown_id = f"{widget_id}_dropdown"
        
        # Start building the HTML
        output = []
        
        # Add container with selected icon display
        output.append(f'''
        <div style="position: relative;">
            <div id="{widget_id}_selected" style="display: flex; align-items: center; border: 1px solid #ccc; border-radius: 4px; padding: 8px 12px; cursor: pointer; background-color: white; min-width: 200px;" onclick="toggleDropdown_{widget_id}()">
                <i id="{widget_id}_icon" class="{value or 'bi-question-circle'}" style="font-size: 1.2rem; margin-right: 10px;"></i>
                <span id="{widget_id}_label">{self.get_icon_label(value) or 'Select an icon'}</span>
                <i class="bi-chevron-down" style="margin-left: auto;"></i>
            </div>
        ''')
        
        # Add the hidden input field to store the selected value
        output.append(f'<input type="hidden" name="{name}" id="{widget_id}" value="{value or ""}">')
        
        # Add the dropdown with grid layout
        output.append(f'''
            <div id="{dropdown_id}" style="display: none; position: absolute; top: 100%; left: 0; z-index: 1000; background-color: white; border: 1px solid #ccc; border-radius: 4px; padding: 15px; width: 600px; max-height: 400px; overflow-y: auto; margin-top: 5px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                <div style="margin-bottom: 15px;">
                    <input type="text" id="{widget_id}_search" placeholder="Search icons..." style="width: 100%; padding: 8px; border: 1px solid #ccc; border-radius: 4px;" 
                           oninput="searchIcons_{widget_id}(this.value)">
                </div>
                <div id="{widget_id}_grid" style="display: grid; grid-template-columns: repeat(8, 1fr); gap: 12px;">
        ''')
        
        # Add icons to the grid
        for icon_class, icon_label in BOOTSTRAP_ICONS:
            is_selected = icon_class == value
            selected_class = 'background-color: #e9f5ff; border-color: #2563eb;' if is_selected else ''
            
            output.append(f'''
                <div class="icon-item" data-name="{icon_label.lower()}" style="display: flex; flex-direction: column; align-items: center; padding: 8px; border: 2px solid #ddd; border-radius: 4px; cursor: pointer; {selected_class}" 
                     onclick="selectIcon_{widget_id}('{icon_class}', '{icon_label}')">
                    <i class="{icon_class}" style="font-size: 1.5rem;"></i>
                    <span style="font-size: 0.7rem; margin-top: 5px; text-align: center; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; width: 100%;">{icon_label}</span>
                </div>
            ''')
        
        # Close the grid and dropdown
        output.append('</div></div>')
        
        # Add JavaScript for the dropdown functionality
        output.append(f'''
        <script type="text/javascript">
            function toggleDropdown_{widget_id}() {{
                var dropdown = document.getElementById("{dropdown_id}");
                if (dropdown.style.display === "none") {{
                    dropdown.style.display = "block";
                    
                    // Adjust position if too close to right edge
                    adjustDropdownPosition_{widget_id}();
                    
                    // Close when clicking outside
                    document.addEventListener("click", closeDropdown_{widget_id});
                    
                    // Focus search input
                    setTimeout(function() {{
                        document.getElementById("{widget_id}_search").focus();
                    }}, 100);
                }} else {{
                    dropdown.style.display = "none";
                }}
            }}
            
            function adjustDropdownPosition_{widget_id}() {{
                var dropdown = document.getElementById("{dropdown_id}");
                var rect = dropdown.getBoundingClientRect();
                
                // If dropdown extends beyond right edge of viewport
                if (rect.right > window.innerWidth) {{
                    // Calculate how much to shift left
                    var shiftLeft = Math.min(rect.right - window.innerWidth + 20, rect.left - 20);
                    dropdown.style.left = -shiftLeft + "px";
                }}
            }}
            
            function closeDropdown_{widget_id}(event) {{
                var dropdown = document.getElementById("{dropdown_id}");
                var selected = document.getElementById("{widget_id}_selected");
                
                if (!dropdown.contains(event.target) && !selected.contains(event.target)) {{
                    dropdown.style.display = "none";
                    document.removeEventListener("click", closeDropdown_{widget_id});
                }}
            }}
            
            function selectIcon_{widget_id}(iconClass, iconLabel) {{
                // Update hidden input value
                var input = document.getElementById("{widget_id}");
                input.value = iconClass;
                
                // Update the displayed icon and label
                var iconElement = document.getElementById("{widget_id}_icon");
                var labelElement = document.getElementById("{widget_id}_label");
                
                iconElement.className = iconClass;
                labelElement.textContent = iconLabel;
                
                // Highlight the selected icon
                var icons = document.querySelectorAll("#{dropdown_id} .icon-item");
                icons.forEach(function(icon) {{
                    icon.style.backgroundColor = "";
                    icon.style.borderColor = "#ddd";
                }});
                
                event.currentTarget.style.backgroundColor = "#e9f5ff";
                event.currentTarget.style.borderColor = "#2563eb";
                
                // Close the dropdown
                var dropdown = document.getElementById("{dropdown_id}");
                dropdown.style.display = "none";
                
                // Trigger change event for form validation
                if ("createEvent" in document) {{
                    var evt = document.createEvent("HTMLEvents");
                    evt.initEvent("change", false, true);
                    input.dispatchEvent(evt);
                }} else {{
                    input.fireEvent("onchange");
                }}
            }}
            
            function searchIcons_{widget_id}(query) {{
                query = query.toLowerCase();
                var icons = document.querySelectorAll("#{widget_id}_grid .icon-item");
                var visibleCount = 0;
                
                icons.forEach(function(icon) {{
                    var name = icon.getAttribute("data-name");
                    if (name.includes(query)) {{
                        icon.style.display = "flex";
                        visibleCount++;
                    }} else {{
                        icon.style.display = "none";
                    }}
                }});
                
                // Show a message if no results found
                var noResultsMsg = document.getElementById("{widget_id}_no_results");
                if (visibleCount === 0) {{
                    if (!noResultsMsg) {{
                        var grid = document.getElementById("{widget_id}_grid");
                        noResultsMsg = document.createElement("div");
                        noResultsMsg.id = "{widget_id}_no_results";
                        noResultsMsg.style.gridColumn = "1 / -1";
                        noResultsMsg.style.padding = "20px";
                        noResultsMsg.style.textAlign = "center";
                        noResultsMsg.style.color = "#666";
                        noResultsMsg.textContent = "No icons found matching your search.";
                        grid.appendChild(noResultsMsg);
                    }} else {{
                        noResultsMsg.style.display = "block";
                    }}
                }} else if (noResultsMsg) {{
                    noResultsMsg.style.display = "none";
                }}
            }}
            
            // Close dropdown when clicking outside (initial setup)
            document.addEventListener("DOMContentLoaded", function() {{
                var dropdown = document.getElementById("{dropdown_id}");
                var selected = document.getElementById("{widget_id}_selected");
                
                // Prevent dropdown from closing when clicking inside it
                dropdown.addEventListener("click", function(event) {{
                    event.stopPropagation();
                }});
                
                // Handle window resize
                window.addEventListener("resize", function() {{
                    if (dropdown.style.display === "block") {{
                        adjustDropdownPosition_{widget_id}();
                    }}
                }});
            }});
        </script>
        ''')
        
        # Close the container
        output.append('</div>')
        
        return mark_safe('\n'.join(output))
    
    def get_icon_label(self, icon_class):
        """Get the label for an icon class"""
        if not icon_class:
            return None
            
        for value, label in BOOTSTRAP_ICONS:
            if value == icon_class:
                return label
        
        return icon_class

class IconField(forms.CharField):
    """Custom form field for icon selection"""
    
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('widget', IconGridPickerWidget)
        super().__init__(*args, **kwargs) 