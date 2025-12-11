from django import forms
from django.utils.safestring import mark_safe
import json


class DynamicTagWidget(forms.Widget):
    """
    Custom widget for JSON list fields with dynamic tag addition/removal.
    Users can add tags one by one using a button, or enter multiple at once.
    """
    
    template_name = 'admin/widgets/dynamic_tag_widget.html'
    
    def __init__(self, attrs=None, placeholder='Add a tag'):
        self.placeholder = placeholder
        default_attrs = {'class': 'dynamic-tag-input'}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs)
    
    def render(self, name, value, attrs=None, renderer=None):
        """
        Render the dynamic tag input widget with JavaScript.
        """
        if attrs is None:
            attrs = {}
        
        # Parse the value
        tags = []
        if value:
            if isinstance(value, str):
                try:
                    tags = json.loads(value)
                except (json.JSONDecodeError, ValueError, TypeError):
                    tags = [v.strip() for v in value.split(',') if v.strip()]
            elif isinstance(value, list):
                tags = value
        
        # Generate unique ID for this widget
        widget_id = attrs.get('id', name)
        
        # Build the HTML
        html = f'''
        <div class="dynamic-tag-widget" id="{widget_id}_container">
            <div class="tag-list" id="{widget_id}_tags">
        '''
        
        # Add existing tags
        for tag in tags:
            html += f'''
                <span class="tag-item">
                    {tag}
                    <button type="button" class="tag-remove" onclick="removeTag(this)">×</button>
                </span>
            '''
        
        html += f'''
            </div>
            <div class="tag-input-row">
                <input type="text" 
                       id="{widget_id}_input" 
                       placeholder="{self.placeholder}"
                       class="vTextField tag-input-field"
                       onkeypress="handleTagKeyPress(event, '{widget_id}')">
                <button type="button" 
                        class="button tag-add-btn" 
                        onclick="addTag('{widget_id}')">
                    + Add
                </button>
            </div>
            <input type="hidden" name="{name}" id="{widget_id}" value='{json.dumps(tags)}'>
            <small class="help">Press Enter or click "+ Add" to add a tag. You can add one or multiple tags.</small>
        </div>
        
        <style>
            .dynamic-tag-widget {{
                max-width: 600px;
            }}
            .tag-list {{
                display: flex;
                flex-wrap: wrap;
                gap: 8px;
                margin-bottom: 10px;
                min-height: 32px;
                padding: 8px;
                background: #f8f8f8;
                border: 1px solid #ddd;
                border-radius: 4px;
            }}
            .tag-item {{
                display: inline-flex;
                align-items: center;
                background: #417690;
                color: white;
                padding: 4px 8px;
                border-radius: 3px;
                font-size: 13px;
                gap: 6px;
            }}
            .tag-remove {{
                background: none;
                border: none;
                color: white;
                font-size: 18px;
                cursor: pointer;
                padding: 0;
                line-height: 1;
                font-weight: bold;
            }}
            .tag-remove:hover {{
                color: #ffcccc;
            }}
            .tag-input-row {{
                display: flex;
                gap: 8px;
                align-items: center;
            }}
            .tag-input-field {{
                flex: 1;
                margin: 0 !important;
            }}
            .tag-add-btn {{
                background: #417690;
                color: white;
                border: none;
                padding: 8px 16px;
                cursor: pointer;
                border-radius: 4px;
                font-size: 13px;
                white-space: nowrap;
            }}
            .tag-add-btn:hover {{
                background: #2e5266;
            }}
            .dynamic-tag-widget small.help {{
                display: block;
                margin-top: 5px;
                color: #666;
                font-size: 12px;
            }}
        </style>
        
        <script>
            function addTag(widgetId) {{
                const input = document.getElementById(widgetId + '_input');
                const tagValue = input.value.trim();
                
                if (!tagValue) return;
                
                const tagList = document.getElementById(widgetId + '_tags');
                const hiddenInput = document.getElementById(widgetId);
                
                // Get current tags
                let tags = [];
                try {{
                    tags = JSON.parse(hiddenInput.value || '[]');
                }} catch(e) {{
                    tags = [];
                }}
                
                // Check if tag already exists
                if (tags.includes(tagValue)) {{
                    alert('This tag already exists!');
                    return;
                }}
                
                // Add new tag
                tags.push(tagValue);
                
                // Create tag element
                const tagElement = document.createElement('span');
                tagElement.className = 'tag-item';
                tagElement.innerHTML = tagValue + 
                    ' <button type="button" class="tag-remove" onclick="removeTag(this)">×</button>';
                
                tagList.appendChild(tagElement);
                
                // Update hidden input
                hiddenInput.value = JSON.stringify(tags);
                
                // Clear input
                input.value = '';
                input.focus();
            }}
            
            function removeTag(button) {{
                const tagElement = button.parentElement;
                const tagValue = tagElement.textContent.replace('×', '').trim();
                const container = tagElement.closest('.dynamic-tag-widget');
                const hiddenInput = container.querySelector('input[type="hidden"]');
                
                // Get current tags
                let tags = [];
                try {{
                    tags = JSON.parse(hiddenInput.value || '[]');
                }} catch(e) {{
                    tags = [];
                }}
                
                // Remove tag
                tags = tags.filter(t => t !== tagValue);
                
                // Update hidden input
                hiddenInput.value = JSON.stringify(tags);
                
                // Remove tag element
                tagElement.remove();
            }}
            
            function handleTagKeyPress(event, widgetId) {{
                if (event.key === 'Enter') {{
                    event.preventDefault();
                    addTag(widgetId);
                }}
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

