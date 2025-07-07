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
    // Show appropriate tab based on what content is available
    const hasQRPreview = document.querySelector('.qr-preview');
    const hasSVGAnalysis = document.querySelector('.svg-analysis-results');
    
    if (hasSVGAnalysis) {
        showTab('svg');
    } else if (hasQRPreview) {
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
            
            // Handle color mask changes
            if (this.name === 'color_mask') {
                handleColorMaskChange(this.value);
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
    
    // Handle color mask change to show/hide custom color options
    function handleColorMaskChange(colorMask) {
        const customColors = document.getElementById('custom-colors');
        const gradientColors = document.getElementById('gradient-colors');
        const useGradientCheckbox = document.getElementById('use_gradient');
        
        if (colorMask === 'custom') {
            // Show custom color options
            if (customColors) customColors.style.display = 'block';
            
            // Show gradient colors if gradient is enabled
            if (useGradientCheckbox && useGradientCheckbox.checked) {
                if (gradientColors) gradientColors.style.display = 'block';
            }
        } else {
            // Hide custom color options
            if (customColors) customColors.style.display = 'none';
        }
    }
    
    // Initialize format state
    const selectedFormat = document.querySelector('input[name="export_format"]:checked');
    if (selectedFormat) {
        handleFormatChange(selectedFormat.value);
    }
    
    // Initialize radio button styles
    updateRadioStyles();
    
    // Add gradient checkbox listener
    const useGradientCheckbox = document.getElementById('use_gradient');
    if (useGradientCheckbox) {
        useGradientCheckbox.addEventListener('change', function() {
            const gradientColors = document.getElementById('gradient-colors');
            if (gradientColors) {
                gradientColors.style.display = this.checked ? 'block' : 'none';
            }
        });
    }
    
    // Initialize color mask state
    const selectedColorMask = document.querySelector('input[name="color_mask"]:checked');
    if (selectedColorMask) {
        handleColorMaskChange(selectedColorMask.value);
    }
    
    // Add SVG analysis functionality
    addSVGAnalysisFeature();
    
    // Add form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            // Special validation for SVG form
            if (form.id === 'svg-form') {
                const svgFile = form.querySelector('#svg_file');
                const svgText = form.querySelector('#svg_text');
                
                if (!svgFile.files.length && !svgText.value.trim()) {
                    e.preventDefault();
                    alert('Please upload an SVG file or paste SVG content');
                    return;
                }
                
                if (svgText.value.trim() && !svgText.value.includes('<svg')) {
                    e.preventDefault();
                    alert('Please provide valid SVG content');
                    return;
                }
            }
            
            // General validation for required fields
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

function addSVGAnalysisFeature() {
    // Add a button to analyze SVG colors when an SVG QR code is generated
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === 'childList') {
                // Check if an SVG preview was added
                const svgFrame = document.querySelector('.svg-frame');
                if (svgFrame && !document.querySelector('.svg-analyze-btn')) {
                    addSVGAnalyzeButton();
                }
            }
        });
    });
    
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
}

function addSVGAnalyzeButton() {
    const qrActions = document.querySelector('.qr-actions');
    if (qrActions && !document.querySelector('.svg-analyze-btn')) {
        const analyzeBtn = document.createElement('button');
        analyzeBtn.className = 'svg-analyze-btn new-btn';
        analyzeBtn.textContent = '🎨 Analyze Colors';
        analyzeBtn.onclick = analyzeSVGColors;
        qrActions.appendChild(analyzeBtn);
    }
}

async function analyzeSVGColors() {
    try {
        const svgFrame = document.querySelector('.svg-frame');
        if (!svgFrame) {
            alert('No SVG QR code found to analyze');
            return;
        }
        
        // Get SVG content from the frame
        const svgDoc = svgFrame.contentDocument || svgFrame.contentWindow.document;
        const svgElement = svgDoc.querySelector('svg');
        
        if (!svgElement) {
            alert('Could not access SVG content');
            return;
        }
        
        const svgContent = svgElement.outerHTML;
        
        // Send to analysis endpoint
        const response = await fetch('/analyze-svg-colors', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ svg_content: svgContent })
        });
        
        const result = await response.json();
        
        if (result.error) {
            alert('Error analyzing SVG: ' + result.error);
            return;
        }
        
        // Show analysis results and populate color picker
        showSVGAnalysisResults(result);
        
    } catch (error) {
        console.error('Error analyzing SVG:', error);
        alert('Error analyzing SVG colors: ' + error.message);
    }
}

function showSVGAnalysisResults(result) {
    const { analysis, color_suggestions } = result;
    
    // Create analysis display
    let analysisHTML = `
        <div class="svg-analysis-results" style="margin-top: 20px; padding: 15px; background: rgba(102, 126, 234, 0.1); border-radius: 10px;">
            <h4>SVG Color Analysis</h4>
            <p><strong>Total shapes:</strong> ${analysis.total_shapes}</p>
            <p><strong>Unique colors:</strong> ${analysis.color_summary.unique_colors.length}</p>
            
            <div style="margin-top: 10px;">
                <strong>Colors found:</strong>
                <div style="display: flex; gap: 10px; margin-top: 5px; flex-wrap: wrap;">
    `;
    
    analysis.color_summary.unique_colors.forEach(color => {
        if (color && color.startsWith('#')) {
            analysisHTML += `
                <div style="display: flex; align-items: center; gap: 5px;">
                    <div style="width: 20px; height: 20px; background: ${color}; border: 1px solid #ccc; border-radius: 3px;"></div>
                    <span style="font-size: 12px;">${color}</span>
                    <button onclick="useColorInPicker('${color}')" style="font-size: 10px; padding: 2px 6px;">Use</button>
                </div>
            `;
        }
    });
    
    analysisHTML += `
                </div>
            </div>
        </div>
    `;
    
    // Add or update analysis display
    const existingAnalysis = document.querySelector('.svg-analysis-results');
    if (existingAnalysis) {
        existingAnalysis.outerHTML = analysisHTML;
    } else {
        const qrPreview = document.querySelector('.qr-preview');
        if (qrPreview) {
            qrPreview.insertAdjacentHTML('beforeend', analysisHTML);
        }
    }
    
    // Pre-populate color picker if available
    if (color_suggestions.foreground !== '#000000') {
        const fgInput = document.getElementById('foreground_color');
        if (fgInput) fgInput.value = color_suggestions.foreground;
    }
    
    if (color_suggestions.background !== '#ffffff') {
        const bgInput = document.getElementById('background_color');
        if (bgInput) bgInput.value = color_suggestions.background;
    }
}

function copyColor(color) {
    // Create temporary input to copy color
    const tempInput = document.createElement('input');
    tempInput.value = color;
    document.body.appendChild(tempInput);
    tempInput.select();
    
    try {
        document.execCommand('copy');
        
        // Visual feedback
        const copyBtn = event.target;
        const originalText = copyBtn.textContent;
        copyBtn.textContent = '✓';
        copyBtn.style.background = '#28a745';
        
        setTimeout(() => {
            copyBtn.textContent = originalText;
            copyBtn.style.background = '#667eea';
        }, 1500);
    } catch (err) {
        console.error('Failed to copy color: ', err);
    }
    
    document.body.removeChild(tempInput);
}

function useColorInPicker(color) {
    // Check which input to populate based on current context
    const customColorsDiv = document.getElementById('custom-colors');
    if (customColorsDiv && customColorsDiv.style.display !== 'none') {
        const fgInput = document.getElementById('foreground_color');
        if (fgInput) {
            fgInput.value = color;
            // Trigger change event
            fgInput.dispatchEvent(new Event('change'));
        }
    } else {
        // Switch to custom colors mode and set the color
        const customRadio = document.querySelector('input[name="color_mask"][value="custom"]');
        if (customRadio) {
            customRadio.checked = true;
            customRadio.dispatchEvent(new Event('change'));
            
            // Wait a bit for the UI to update, then set color
            setTimeout(() => {
                const fgInput = document.getElementById('foreground_color');
                if (fgInput) {
                    fgInput.value = color;
                    fgInput.dispatchEvent(new Event('change'));
                }
            }, 100);
        }
    }
}