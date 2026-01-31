// ============================================
// GIRL SCOUT COOKIE ORDER WEBSITE
// Checkout & Order Submission
// ============================================

/**
 * Submit an order to Google Sheets via Google Apps Script
 * @param {Object} orderData - The order data to submit
 * @returns {Promise<Object>} - The response from the server
 */
async function submitOrder(orderData) {
    // Check if Google Script URL is configured
    if (!CONFIG.GOOGLE_SCRIPT_URL || CONFIG.GOOGLE_SCRIPT_URL === 'YOUR_GOOGLE_APPS_SCRIPT_URL') {
        console.warn('Google Apps Script URL not configured. Order will be saved locally only.');
        return { success: true, orderId: generateOrderId(), local: true };
    }

    try {
        const response = await fetch(CONFIG.GOOGLE_SCRIPT_URL, {
            method: 'POST',
            mode: 'no-cors', // Google Apps Script requires no-cors mode
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(orderData)
        });

        // With no-cors mode, we can't read the response
        // So we assume success if no error was thrown
        console.log('Order submitted to Google Sheets');
        return { success: true, orderId: generateOrderId() };

    } catch (error) {
        console.error('Error submitting order:', error);
        throw error;
    }
}

/**
 * Generate a unique order ID
 * @returns {string} - The generated order ID
 */
function generateOrderId() {
    return 'GS-' + Date.now().toString(36).toUpperCase();
}

/**
 * Validate email format
 * @param {string} email - The email to validate
 * @returns {boolean} - True if valid
 */
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

/**
 * Validate phone number format
 * @param {string} phone - The phone number to validate
 * @returns {boolean} - True if valid (basic validation)
 */
function isValidPhone(phone) {
    // Remove common formatting characters
    const cleaned = phone.replace(/[\s\-\(\)\.]/g, '');
    // Check if it's at least 10 digits
    return /^\+?\d{10,}$/.test(cleaned);
}

/**
 * Format phone number for display
 * @param {string} phone - The phone number to format
 * @returns {string} - Formatted phone number
 */
function formatPhone(phone) {
    const cleaned = phone.replace(/\D/g, '');
    if (cleaned.length === 10) {
        return `(${cleaned.slice(0, 3)}) ${cleaned.slice(3, 6)}-${cleaned.slice(6)}`;
    }
    return phone;
}

/**
 * Validate the checkout form
 * @param {Object} formData - The form data to validate
 * @returns {Object} - { valid: boolean, errors: string[] }
 */
function validateCheckoutForm(formData) {
    const errors = [];

    if (!formData.customerName || formData.customerName.trim().length < 2) {
        errors.push('Please enter your full name');
    }

    if (!formData.email || !isValidEmail(formData.email)) {
        errors.push('Please enter a valid email address');
    }

    if (!formData.phone || !isValidPhone(formData.phone)) {
        errors.push('Please enter a valid phone number');
    }

    if (!formData.deliveryMethod) {
        errors.push('Please select a delivery method');
    }

    if (formData.deliveryMethod === 'delivery' && (!formData.address || formData.address.trim().length < 10)) {
        errors.push('Please enter a complete delivery address');
    }

    return {
        valid: errors.length === 0,
        errors
    };
}

/**
 * Generate Venmo payment link
 * @param {number} amount - The payment amount
 * @param {string} note - The payment note
 * @returns {string} - The Venmo URL
 */
function generateVenmoLink(amount, note) {
    const encodedNote = encodeURIComponent(note);
    const isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);

    if (isMobile) {
        // Venmo deep link for mobile
        return `venmo://paycharge?txn=pay&recipients=${CONFIG.VENMO_USERNAME}&amount=${amount}&note=${encodedNote}`;
    }
    // Venmo web link for desktop
    return `https://venmo.com/${CONFIG.VENMO_USERNAME}?txn=pay&amount=${amount}&note=${encodedNote}`;
}

/**
 * Format currency for display
 * @param {number} amount - The amount to format
 * @returns {string} - Formatted currency string
 */
function formatCurrency(amount) {
    return '$' + amount.toFixed(2);
}

/**
 * Format date for display
 * @param {Date|string} date - The date to format
 * @returns {string} - Formatted date string
 */
function formatDate(date) {
    const d = new Date(date);
    return d.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}
