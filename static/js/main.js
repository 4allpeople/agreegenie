// JavaScript for Legal Contract Generator

document.addEventListener('DOMContentLoaded', function() {
    // Template selection handler - could be used to show/hide template-specific fields
    const templateSelect = document.getElementById('template');
    if (templateSelect) {
        templateSelect.addEventListener('change', function() {
            // You could use this to show/hide template-specific fields
            const selectedTemplate = this.value;
            console.log(`Selected template: ${selectedTemplate}`);
            
            // For future enhancement: Toggle visibility of template-specific form sections
        });
    }
    
    // Form validation
    const contractForm = document.getElementById('contractForm');
    if (contractForm) {
        contractForm.addEventListener('submit', function(event) {
            let isValid = true;
            
            // Get required fields
            const requiredFields = contractForm.querySelectorAll('[required]');
            
            // Clear previous error messages
            const errorMessages = contractForm.querySelectorAll('.invalid-feedback');
            errorMessages.forEach(msg => msg.remove());
            
            // Reset invalid styling
            const formControls = contractForm.querySelectorAll('.form-control, .form-select');
            formControls.forEach(field => field.classList.remove('is-invalid'));
            
            // Check each required field
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.classList.add('is-invalid');
                    
                    // Add error message
                    const errorDiv = document.createElement('div');
                    errorDiv.className = 'invalid-feedback';
                    errorDiv.textContent = 'This field is required.';
                    field.parentNode.appendChild(errorDiv);
                }
            });
            
            if (!isValid) {
                event.preventDefault();
                // Scroll to first error
                const firstError = contractForm.querySelector('.is-invalid');
                if (firstError) {
                    firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    firstError.focus();
                }
            }
        });
    }
    
    // Initialize any Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});
