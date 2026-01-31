// ============================================
// GIRL SCOUT COOKIE ORDER WEBSITE
// Shopping Cart Functionality
// ============================================

const CART_STORAGE_KEY = 'girlScoutCookieCart';

// ============================================
// Cart Data Structure
// ============================================
// Cart is stored as an array of objects:
// [{ cookieId: 'thin-mints', quantity: 2 }, ...]

/**
 * Get the current cart from localStorage
 * @returns {Array} - The cart array
 */
function getCart() {
    try {
        const cart = localStorage.getItem(CART_STORAGE_KEY);
        return cart ? JSON.parse(cart) : [];
    } catch (error) {
        console.error('Error reading cart from localStorage:', error);
        return [];
    }
}

/**
 * Save the cart to localStorage
 * @param {Array} cart - The cart array to save
 */
function saveCart(cart) {
    try {
        localStorage.setItem(CART_STORAGE_KEY, JSON.stringify(cart));
    } catch (error) {
        console.error('Error saving cart to localStorage:', error);
    }
}

/**
 * Get a specific item from the cart
 * @param {string} cookieId - The cookie ID
 * @returns {Object|undefined} - The cart item or undefined
 */
function getCartItem(cookieId) {
    const cart = getCart();
    return cart.find(item => item.cookieId === cookieId);
}

/**
 * Add an item to the cart
 * @param {string} cookieId - The cookie ID
 * @param {number} quantity - The quantity to add
 */
function addToCart(cookieId, quantity = 1) {
    const cart = getCart();
    const existingItem = cart.find(item => item.cookieId === cookieId);

    if (existingItem) {
        existingItem.quantity += quantity;
    } else {
        cart.push({ cookieId, quantity });
    }

    saveCart(cart);
    console.log(`Added ${quantity} x ${cookieId} to cart`);
}

/**
 * Update the quantity of a cart item
 * @param {string} cookieId - The cookie ID
 * @param {number} newQuantity - The new quantity
 */
function updateCartItemQuantity(cookieId, newQuantity) {
    const cart = getCart();
    const item = cart.find(item => item.cookieId === cookieId);

    if (item) {
        if (newQuantity <= 0) {
            removeFromCart(cookieId);
        } else {
            item.quantity = newQuantity;
            saveCart(cart);
        }
    }
}

/**
 * Remove an item from the cart
 * @param {string} cookieId - The cookie ID
 */
function removeFromCart(cookieId) {
    let cart = getCart();
    cart = cart.filter(item => item.cookieId !== cookieId);
    saveCart(cart);
    console.log(`Removed ${cookieId} from cart`);
}

/**
 * Clear the entire cart
 */
function clearCart() {
    localStorage.removeItem(CART_STORAGE_KEY);
    console.log('Cart cleared');
}

/**
 * Get the total number of items in the cart
 * @returns {number} - Total quantity of all items
 */
function getCartItemCount() {
    const cart = getCart();
    return cart.reduce((total, item) => total + item.quantity, 0);
}

/**
 * Get the total price of the cart
 * @returns {number} - Total price in dollars
 */
function getCartTotal() {
    const cart = getCart();
    return cart.reduce((total, item) => total + (item.quantity * CONFIG.PRICE_PER_BOX), 0);
}

/**
 * Check if the cart is empty
 * @returns {boolean} - True if cart is empty
 */
function isCartEmpty() {
    return getCart().length === 0;
}

/**
 * Get a formatted summary of cart items
 * @returns {string} - Formatted string of items
 */
function getCartSummary() {
    const cart = getCart();
    return cart.map(item => {
        const cookie = getCookieById(item.cookieId);
        return cookie ? `${cookie.name} x${item.quantity}` : '';
    }).filter(Boolean).join(', ');
}
