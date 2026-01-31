// ============================================
// GIRL SCOUT COOKIE ORDER WEBSITE
// Configuration File
// ============================================
// EDIT THESE VALUES FOR YOUR COOKIE SALE
// ============================================

const CONFIG = {
    // ----------------------------------------
    // VENMO SETTINGS
    // ----------------------------------------
    // Your Venmo username (without the @)
    VENMO_USERNAME: 'YourVenmoUsername',

    // ----------------------------------------
    // GOOGLE SHEETS INTEGRATION
    // ----------------------------------------
    // Google Apps Script URL (from your deployed script)
    // See README.md for setup instructions
    GOOGLE_SCRIPT_URL: 'YOUR_GOOGLE_APPS_SCRIPT_URL',

    // ----------------------------------------
    // SELLER INFORMATION
    // ----------------------------------------
    // The Girl Scout's first name
    SELLER_NAME: 'Emma',

    // Troop number
    TROOP_NUMBER: '45678',

    // Council name
    COUNCIL_NAME: 'Girl Scouts of Northeast Texas',

    // ----------------------------------------
    // PRICING
    // ----------------------------------------
    // Price per box of cookies (in dollars)
    PRICE_PER_BOX: 10,

    // ----------------------------------------
    // CONTACT INFORMATION
    // ----------------------------------------
    // Email address for order questions
    CONTACT_EMAIL: 'parent@email.com'
};

// ============================================
// DO NOT EDIT BELOW THIS LINE
// ============================================
// Freeze the config object to prevent accidental modifications
Object.freeze(CONFIG);
