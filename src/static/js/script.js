// JavaScript for Utility Tools

function showTab(tabName) {
    // Hide all sections
    const sections = document.querySelectorAll('.tool-section');
    sections.forEach(section => {
        section.classList.remove('active');
    });
    
    // Remove active class from all tab buttons
    const tabButtons = document.querySelectorAll('.tab-button');
    tabButtons.forEach(button => {
        button.classList.remove('active');
    });
    
    // Show selected section
    document.getElementById(tabName + '-section').classList.add('active');
    
    // Add active class to selected tab button
    document.getElementById(tabName + '-tab').classList.add('active');
}

function copyToClipboard(inputId) {
    const input = document.getElementById(inputId);
    input.select();
    input.setSelectionRange(0, 99999); // For mobile devices
    
    try {
        document.execCommand('copy');
        
        // Visual feedback
        const copyBtn = event.target;
        const originalText = copyBtn.textContent;
        copyBtn.textContent = 'Copied!';
        copyBtn.style.background = '#28a745';
        
        setTimeout(() => {
            copyBtn.textContent = originalText;
            copyBtn.style.background = '#667eea';
        }, 2000);
    } catch (err) {
        console.error('Failed to copy: ', err);
        alert('Failed to copy to clipboard');
    }
}

function generateNew() {
    // Show the form again and clear the preview
    const form = document.getElementById('qr-form');
    const preview = document.querySelector('.qr-preview');
    
    if (form && preview) {
        form.classList.remove('collapsed');
        preview.style.display = 'none';
    }
    
    // Clear only the text input and file input, keep radio selections
    document.getElementById('data').value = '';
    document.getElementById('image').value = '';
    
    // Update radio button styles after showing form again
    updateRadioStyles();
    
    // Clear session data by making a request to clear endpoint
    fetch('/clear-qr-session', { method: 'POST' })
        .then(() => {
            console.log('Session cleared');
        })
        .catch(err => {
            console.error('Error clearing session:', err);
        });
    
    // Focus on the data input
    document.getElementById('data').focus();
}

function updateRadioStyles() {
    // Update radio button styling for better browser compatibility
    const radioButtons = document.querySelectorAll('input[type="radio"]');
    radioButtons.forEach(radio => {
        const label = radio.closest('label');
        if (label) {
            if (radio.checked) {
                label.classList.add('checked');
            } else {
                label.classList.remove('checked');
            }
        }
    });
}

// Initialize page
document.addEventListener('DOMContentLoaded', function() {
    // Show QR tab by default if no QR preview, otherwise show the preview
    const hasQRPreview = document.querySelector('.qr-preview');
    if (hasQRPreview) {
        showTab('qr');
    } else {
        showTab('qr');
    }
    
    // Add radio button change listeners for styling
    const radioButtons = document.querySelectorAll('input[type="radio"]');
    radioButtons.forEach(radio => {
        radio.addEventListener('change', function() {
            // Remove checked class from all labels in the same group
            const groupName = this.name;
            const groupRadios = document.querySelectorAll(`input[type="radio"][name="${groupName}"]`);
            groupRadios.forEach(groupRadio => {
                const label = groupRadio.closest('label');
                if (label) {
                    label.classList.remove('checked');
                }
            });
            
            // Add checked class to the selected label
            const selectedLabel = this.closest('label');
            if (selectedLabel) {
                selectedLabel.classList.add('checked');
            }
            
            // Handle export format changes
            if (this.name === 'export_format') {
                handleFormatChange(this.value);
            }
        });
    });
    
    // Handle format change to show/hide styling options
    function handleFormatChange(format) {
        const svgInfo = document.getElementById('svg-info');
        const moduleGroup = document.querySelector('input[name="module_drawer"]').closest('.form-group');
        const colorGroup = document.querySelector('input[name="color_mask"]').closest('.form-group');
        
        if (format === 'svg') {
            // Show SVG limitations warning
            if (svgInfo) svgInfo.style.display = 'block';
            
            // Disable/dim styling options for SVG
            if (moduleGroup) moduleGroup.style.opacity = '0.5';
            if (colorGroup) colorGroup.style.opacity = '0.5';
        } else {
            // Hide warning
            if (svgInfo) svgInfo.style.display = 'none';
            
            // Re-enable styling options for PNG
            if (moduleGroup) moduleGroup.style.opacity = '1';
            if (colorGroup) colorGroup.style.opacity = '1';
        }
    }
    
    // Initialize format state
    const selectedFormat = document.querySelector('input[name="export_format"]:checked');
    if (selectedFormat) {
        handleFormatChange(selectedFormat.value);
    }
    
    // Initialize radio button styles
    updateRadioStyles();
    
    // Add form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('input[required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.style.borderColor = '#e74c3c';
                } else {
                    field.style.borderColor = '#ddd';
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                alert('Please fill in all required fields');
            }
        });
    });
});