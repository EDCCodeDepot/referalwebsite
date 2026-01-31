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
    VENMO_USERNAME: 'evan-decorte',

    // ----------------------------------------
    // GOOGLE SHEETS INTEGRATION
    // ----------------------------------------
    // Google Apps Script URL (from your deployed script)
    // See README.md for setup instructions
    GOOGLE_SCRIPT_URL: 'https://script.google.com/macros/s/AKfycbw5FYqW0rsOnaqZjC3duW3cAAYjMYnJ33k9PXSB1lg6QT590mMU5HcTqG-70s7Oo1RO/exec',

    // ----------------------------------------
    // SELLER INFORMATION
    // ----------------------------------------
    // The Girl Scout's first name
    SELLER_NAME: 'Ilana',

    // Troop number
    TROOP_NUMBER: '1234',

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
    CONTACT_EMAIL: 'evandec@gmail.com'
};

// ============================================
// DO NOT EDIT BELOW THIS LINE
// ============================================
// Freeze the config object to prevent accidental modifications
Object.freeze(CONFIG);
