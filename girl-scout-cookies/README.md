# Girl Scout Cookie Order Website

A simple, mobile-friendly website for Girl Scouts to sell cookies online. Customers can browse cookies, place orders, and pay via Venmo. Orders are automatically logged to a Google Sheet for easy tracking.

## Features

- Mobile-first responsive design
- Clean, professional Girl Scout branding
- Cookie catalog with dietary filters (Vegan, Gluten-Free)
- Shopping cart with localStorage persistence
- Checkout form with delivery/pickup options
- Venmo payment integration (mobile deep links + web fallback)
- QR code for Venmo payments
- Google Sheets integration for order tracking
- Print-friendly order confirmations

## Quick Start

### 1. Configure Your Settings

Edit `js/config.js` to customize the website:

```javascript
const CONFIG = {
    // Your Venmo username (without the @)
    VENMO_USERNAME: 'Jane-Smith-123',

    // Google Apps Script URL (see setup below)
    GOOGLE_SCRIPT_URL: 'https://script.google.com/macros/s/YOUR_SCRIPT_ID/exec',

    // Seller Information
    SELLER_NAME: 'Emma',
    TROOP_NUMBER: '45678',
    COUNCIL_NAME: 'Girl Scouts of Northeast Texas',

    // Price per box
    PRICE_PER_BOX: 10,

    // Contact email for questions
    CONTACT_EMAIL: 'parent@email.com'
};
```

### 2. Set Up Google Sheets (Optional but Recommended)

Follow the steps below to enable automatic order logging.

### 3. Deploy to GitHub Pages

1. Push this code to a GitHub repository
2. Go to Settings > Pages
3. Select "Deploy from a branch" and choose `main`
4. Your site will be live at `https://yourusername.github.io/girl-scout-cookies/`

## Google Sheets Setup

### Step 1: Create a Google Sheet

1. Go to [Google Sheets](https://sheets.google.com) and create a new spreadsheet
2. Name it "Cookie Orders" (or whatever you prefer)
3. Add these column headers in Row 1:
   - A: Timestamp
   - B: Order ID
   - C: Customer Name
   - D: Email
   - E: Phone
   - F: Delivery Method
   - G: Address
   - H: Items
   - I: Total
   - J: Payment Status
   - K: Notes

### Step 2: Create the Google Apps Script

1. In your Google Sheet, go to **Extensions > Apps Script**
2. Delete any code in the editor and paste the following:

```javascript
function doPost(e) {
  try {
    const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    const data = JSON.parse(e.postData.contents);
    const orderId = generateOrderId();

    sheet.appendRow([
      new Date(),                    // Timestamp
      orderId,                       // Order ID
      data.customerName,             // Customer Name
      data.email,                    // Email
      data.phone,                    // Phone
      data.deliveryMethod,           // Delivery Method
      data.address || '',            // Address
      data.items,                    // Items
      '$' + data.total,              // Total
      'Pending',                     // Payment Status
      data.notes || ''               // Notes
    ]);

    return ContentService
      .createTextOutput(JSON.stringify({success: true, orderId: orderId}))
      .setMimeType(ContentService.MimeType.JSON);

  } catch (error) {
    return ContentService
      .createTextOutput(JSON.stringify({success: false, error: error.message}))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

function generateOrderId() {
  return 'GS-' + Date.now().toString(36).toUpperCase();
}

function doGet(e) {
  return ContentService.createTextOutput('Cookie order API is running!');
}
```

3. Click **Save** (give the project a name like "Cookie Orders Script")

### Step 3: Deploy as a Web App

1. Click **Deploy > New deployment**
2. Click the gear icon next to "Select type" and choose **Web app**
3. Fill in the settings:
   - Description: "Cookie Order API"
   - Execute as: **Me**
   - Who has access: **Anyone**
4. Click **Deploy**
5. **Important:** Click "Authorize access" and allow the permissions
6. Copy the **Web app URL** (it looks like `https://script.google.com/macros/s/ABC123.../exec`)

### Step 4: Add the URL to Your Config

Paste the Web app URL into `js/config.js`:

```javascript
GOOGLE_SCRIPT_URL: 'https://script.google.com/macros/s/YOUR_SCRIPT_ID/exec',
```

## Managing Orders

### Viewing Orders

All orders appear in your Google Sheet with:
- Timestamp of when the order was placed
- Unique Order ID
- Customer contact information
- Items ordered
- Total amount
- Payment status (defaults to "Pending")

### Tracking Payments

1. When a customer pays via Venmo, you'll see the notification in Venmo
2. Find the matching order in your Google Sheet by customer name or order ID
3. Update the "Payment Status" column to "Paid"

### Tips for Order Management

- Sort by Timestamp to see newest orders first
- Use Google Sheets filters to view only "Pending" payments
- Use conditional formatting to highlight unpaid orders
- Add notes in the Notes column for special instructions

## File Structure

```
girl-scout-cookies/
├── index.html          # Home page with cookie catalog
├── cart.html           # Cart and checkout page
├── confirmation.html   # Order confirmation with Venmo
├── css/
│   └── styles.css      # All styles (mobile-first)
├── js/
│   ├── config.js       # Configuration settings
│   ├── cookies.js      # Cookie catalog data
│   ├── cart.js         # Shopping cart functionality
│   └── checkout.js     # Checkout and order submission
├── images/             # Cookie images (if any)
└── README.md           # This file
```

## Customization

### Changing Cookie Prices

Edit `js/config.js`:
```javascript
PRICE_PER_BOX: 10,  // Change to your price
```

### Adding/Removing Cookies

Edit `js/cookies.js` to modify the `COOKIES` array. Each cookie has:
- `id`: Unique identifier
- `name`: Display name
- `altName`: Alternative name (optional)
- `description`: Short description
- `vegan`: Boolean for dietary filter
- `glutenFree`: Boolean for dietary filter
- `isNew`: Boolean to show "NEW!" badge
- `color`: Background color for placeholder image
- `emoji`: Emoji for placeholder image

### Changing Colors

Edit the CSS custom properties at the top of `css/styles.css`:
```css
:root {
    --color-primary: #00ae58;      /* Girl Scout green */
    --color-accent: #ffc627;       /* Gold highlights */
    /* ... other colors ... */
}
```

## Troubleshooting

### Orders not appearing in Google Sheets

1. Check that your Google Script URL is correct in `config.js`
2. Make sure the Google Apps Script is deployed with "Anyone" access
3. Check the browser console for error messages
4. Try the script URL directly in your browser - it should show "Cookie order API is running!"

### Venmo link not working

1. On mobile: Make sure the Venmo app is installed
2. On desktop: The link opens Venmo's website where users can log in
3. Check that your Venmo username is correct (without the @)

### Cart not persisting

1. Make sure localStorage is enabled in the browser
2. Check if the user is in private/incognito mode (localStorage may be limited)

### Styles look broken

1. Make sure `css/styles.css` is in the correct location
2. Check the browser console for 404 errors
3. Clear browser cache and refresh

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Mobile Safari (iOS)
- Chrome for Android

## License

This project is free to use for Girl Scout cookie sales.

## Support

For questions about this website, contact: [your email]

For questions about Girl Scout Cookies, visit: [girlscouts.org](https://www.girlscouts.org)

---

Made with love to support Girl Scouts!
