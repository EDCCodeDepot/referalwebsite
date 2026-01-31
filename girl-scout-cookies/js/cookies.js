// ============================================
// GIRL SCOUT COOKIE ORDER WEBSITE
// Cookie Catalog Data
// ============================================

const COOKIES = [
    {
        id: 'thin-mints',
        name: 'Thin Mints',
        altName: null,
        description: 'Crisp chocolate cookies dipped in mint chocolaty coating',
        vegan: true,
        glutenFree: false,
        isNew: false,
        color: '#2d5a3d',
        emoji: '🍫',
        image: 'images/thin-mints.png'
    },
    {
        id: 'samoas',
        name: 'Samoas',
        altName: 'Caramel deLites',
        description: 'Crisp cookies with caramel, coconut, and chocolaty stripes',
        vegan: false,
        glutenFree: false,
        isNew: false,
        color: '#8b5a2b',
        emoji: '🥥',
        image: 'images/samoas.png'
    },
    {
        id: 'tagalongs',
        name: 'Tagalongs',
        altName: 'Peanut Butter Patties',
        description: 'Crispy cookies layered with peanut butter, covered in chocolate',
        vegan: true,
        glutenFree: false,
        isNew: false,
        color: '#5c4033',
        emoji: '🥜',
        image: 'images/tagalongs.png'
    },
    {
        id: 'do-si-dos',
        name: 'Do-si-dos',
        altName: 'Peanut Butter Sandwich',
        description: 'Crunchy oatmeal sandwich cookies with peanut butter filling',
        vegan: false,
        glutenFree: false,
        isNew: false,
        color: '#c4a35a',
        emoji: '🥪',
        image: 'images/do-si-dos.png'
    },
    {
        id: 'trefoils',
        name: 'Trefoils',
        altName: null,
        description: 'Classic shortbread cookies inspired by the original recipe',
        vegan: false,
        glutenFree: false,
        isNew: false,
        color: '#e6d5a8',
        emoji: '🍪',
        image: 'images/trefoils.png'
    },
    {
        id: 'lemonades',
        name: 'Lemonades',
        altName: null,
        description: 'Shortbread cookies topped with tangy lemon icing',
        vegan: true,
        glutenFree: false,
        isNew: false,
        color: '#fff44f',
        emoji: '🍋',
        image: 'images/lemonades.png'
    },
    {
        id: 'lemon-ups',
        name: 'Lemon-Ups',
        altName: null,
        description: 'Crispy lemon cookies baked with inspiring messages',
        vegan: false,
        glutenFree: false,
        isNew: false,
        color: '#ffd700',
        emoji: '✨',
        image: 'images/lemon-ups.png'
    },
    {
        id: 'adventurefuls',
        name: 'Adventurefuls',
        altName: null,
        description: 'Brownie-inspired cookies topped with caramel crème and sea salt',
        vegan: false,
        glutenFree: false,
        isNew: false,
        color: '#4a3728',
        emoji: '🏔️',
        image: 'images/adventurefuls.png'
    },
    {
        id: 'toffee-tastic',
        name: 'Toffee-tastic',
        altName: null,
        description: 'Rich, buttery cookies with sweet, crunchy toffee bits',
        vegan: false,
        glutenFree: true,
        isNew: false,
        color: '#d4a574',
        emoji: '🧈',
        image: 'images/toffee-tastic.png'
    },
    {
        id: 'caramel-chocolate-chip',
        name: 'Caramel Chocolate Chip',
        altName: null,
        description: 'Chewy cookies with caramel, chocolate chips, and sea salt',
        vegan: false,
        glutenFree: true,
        isNew: false,
        color: '#8b6914',
        emoji: '🍯',
        image: 'images/caramel-chocolate-chip.png'
    },
    {
        id: 'smores',
        name: "Girl Scout S'mores",
        altName: null,
        description: 'Crunchy graham sandwich cookies with chocolate and marshmallow filling',
        vegan: false,
        glutenFree: false,
        isNew: true,
        color: '#6b4423',
        emoji: '🏕️',
        image: 'images/smores.png'
    }
];

// ============================================
// Helper Functions
// ============================================

/**
 * Get a cookie by its ID
 * @param {string} id - The cookie ID
 * @returns {Object|undefined} - The cookie object or undefined if not found
 */
function getCookieById(id) {
    return COOKIES.find(cookie => cookie.id === id);
}

/**
 * Get all vegan cookies
 * @returns {Array} - Array of vegan cookie objects
 */
function getVeganCookies() {
    return COOKIES.filter(cookie => cookie.vegan);
}

/**
 * Get all gluten-free cookies
 * @returns {Array} - Array of gluten-free cookie objects
 */
function getGlutenFreeCookies() {
    return COOKIES.filter(cookie => cookie.glutenFree);
}

/**
 * Get all new cookies
 * @returns {Array} - Array of new cookie objects
 */
function getNewCookies() {
    return COOKIES.filter(cookie => cookie.isNew);
}

/**
 * Render a cookie image with fallback to emoji placeholder
 * @param {Object} cookie - The cookie object
 * @param {boolean} small - Whether to render a small version
 * @returns {string} - HTML string for the image
 */
function renderCookieImage(cookie, small = false) {
    if (cookie.image) {
        return `<img src="${cookie.image}"
                     alt="${cookie.name}"
                     loading="lazy"
                     onerror="this.parentElement.innerHTML='<span class=\\'cookie-emoji\\'>${cookie.emoji}</span>'"
                     class="cookie-img ${small ? 'cookie-img-small' : ''}">`;
    }
    return `<span class="cookie-emoji">${cookie.emoji}</span>`;
}

// Freeze the cookies array to prevent accidental modifications
Object.freeze(COOKIES);
COOKIES.forEach(cookie => Object.freeze(cookie));
