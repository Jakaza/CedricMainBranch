from django import forms
from django.utils.safestring import mark_safe
import json


class RoomSpecificationWidget(forms.Widget):
    """
    Custom widget for managing room specifications with name and quantity pairs.
    Users can add multiple rooms with their quantities dynamically.
    """
    
    def __init__(self, attrs=None):
        default_attrs = {'class': 'room-spec-input'}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs)
    
    def render(self, name, value, attrs=None, renderer=None):
        """
        Render the room specification widget with JavaScript.
        """
        if attrs is None:
            attrs = {}
        
        # Parse the value
        rooms = []
        if value:
            if isinstance(value, str):
                try:
                    rooms = json.loads(value)
                except (json.JSONDecodeError, ValueError, TypeError):
                    rooms = []
            elif isinstance(value, list):
                rooms = value
        
        # Generate unique ID for this widget
        widget_id = attrs.get('id', name)
        
        # Build the HTML
        html = f'''
        <div class="room-spec-widget" id="{widget_id}_container">
            <div class="room-spec-list" id="{widget_id}_list">
        '''
        
        # Add existing room specifications
        for i, room in enumerate(rooms):
            room_name = room.get('name', '')
            room_quantity = room.get('quantity', 1)
            html += f'''
                <div class="room-spec-row">
                    <input type="text" 
                           class="vTextField room-name-input" 
                           placeholder="Room name (e.g., Study Room)"
                           value="{room_name}"
                           onchange="updateRoomSpecs('{widget_id}')">
                    <input type="number" 
                           class="vTextField room-quantity-input" 
                           placeholder="Qty"
                           value="{room_quantity}"
                           min="1"
                           onchange="updateRoomSpecs('{widget_id}')">
                    <button type="button" 
                            class="button room-remove-btn" 
                            onclick="removeRoomSpec(this, '{widget_id}')">
                        Remove
                    </button>
                </div>
            '''
        
        html += f'''
            </div>
            <button type="button" 
                    class="button room-add-btn" 
                    onclick="addRoomSpec('{widget_id}')">
                + Add Room
            </button>
            <input type="hidden" name="{name}" id="{widget_id}" value='{json.dumps(rooms)}'>
            <small class="help">Add custom room types with their quantities (e.g., Study Room: 2, Gym: 1)</small>
        </div>
        
        <style>
            .room-spec-widget {{
                max-width: 700px;
            }}
            .room-spec-list {{
                margin-bottom: 10px;
            }}
            .room-spec-row {{
                display: flex;
                gap: 8px;
                margin-bottom: 8px;
                align-items: center;
            }}
            .room-name-input {{
                flex: 2;
                margin: 0 !important;
            }}
            .room-quantity-input {{
                flex: 0 0 80px;
                margin: 0 !important;
            }}
            .room-remove-btn {{
                background: #ba2121;
                color: white;
                border: none;
                padding: 8px 12px;
                cursor: pointer;
                border-radius: 4px;
                font-size: 13px;
                white-space: nowrap;
            }}
            .room-remove-btn:hover {{
                background: #8b1a1a;
            }}
            .room-add-btn {{
                background: #417690;
                color: white;
                border: none;
                padding: 8px 16px;
                cursor: pointer;
                border-radius: 4px;
                font-size: 13px;
            }}
            .room-add-btn:hover {{
                background: #2e5266;
            }}
            .room-spec-widget small.help {{
                display: block;
                margin-top: 5px;
                color: #666;
                font-size: 12px;
            }}
        </style>
        
        <script>
            function addRoomSpec(widgetId) {{
                const list = document.getElementById(widgetId + '_list');
                
                const row = document.createElement('div');
                row.className = 'room-spec-row';
                row.innerHTML = `
                    <input type="text" 
                           class="vTextField room-name-input" 
                           placeholder="Room name (e.g., Study Room)"
                           onchange="updateRoomSpecs('${{widgetId}}')">
                    <input type="number" 
                           class="vTextField room-quantity-input" 
                           placeholder="Qty"
                           value="1"
                           min="1"
                           onchange="updateRoomSpecs('${{widgetId}}')">
                    <button type="button" 
                            class="button room-remove-btn" 
                            onclick="removeRoomSpec(this, '${{widgetId}}')">
                        Remove
                    </button>
                `;
                
                list.appendChild(row);
                
                // Focus on the new room name input
                const nameInput = row.querySelector('.room-name-input');
                nameInput.focus();
            }}
            
            function removeRoomSpec(button, widgetId) {{
                const row = button.parentElement;
                row.remove();
                updateRoomSpecs(widgetId);
            }}
            
            function updateRoomSpecs(widgetId) {{
                const container = document.getElementById(widgetId + '_container');
                const hiddenInput = document.getElementById(widgetId);
                const rows = container.querySelectorAll('.room-spec-row');
                
                const rooms = [];
                rows.forEach(row => {{
                    const nameInput = row.querySelector('.room-name-input');
                    const quantityInput = row.querySelector('.room-quantity-input');
                    
                    const name = nameInput.value.trim();
                    const quantity = parseInt(quantityInput.value) || 1;
                    
                    if (name) {{
                        rooms.push({{
                            name: name,
                            quantity: quantity
                        }});
                    }}
                }});
                
                hiddenInput.value = JSON.stringify(rooms);
            }}
        </script>
        '''
        
        return mark_safe(html)
    
    def value_from_datadict(self, data, files, name):
        """
        Extract value from form data.
        Returns the raw JSON string so Django's JSONField can handle the parsing.
        """
        return data.get(name)
