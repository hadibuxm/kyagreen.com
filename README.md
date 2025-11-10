# KiyaGreen E-Commerce Website

A modern, eco-friendly e-commerce platform built with Django, Bootstrap 5, and jQuery. KiyaGreen provides a complete solution for managing products, services, and customer quote requests.

## Features

### Admin Panel Management
- **Homepage Management**: Modify hero sections, welcome content, and featured items
- **Product Management**: Add/edit products with images, specifications, and pricing
- **Category Management**: Hierarchical category structure with filtering
- **Service Management**: Manage services with features and descriptions
- **RFQ Management**: Track and manage customer quote requests
- **Content Pages**: Editable information and contact pages

### Customer Features
- **Product Catalog**: Browse products with category filters and search
- **Product Details**: Detailed product information with image gallery
- **Services Showcase**: Display services with detailed descriptions
- **RFQ System**: Request for quotation on any product or general inquiry
- **Contact Form**: Get in touch with the business
- **Responsive Design**: Mobile-friendly interface with Bootstrap 5

## Technology Stack

- **Backend**: Django 4.2+
- **Frontend**: Bootstrap 5, jQuery 3.7
- **Rich Text Editor**: CKEditor
- **Database**: SQLite (development) / PostgreSQL (production ready)
- **Icons**: Bootstrap Icons

## Color Theme

- **Primary Green**: #2d6a4f
- **Light Green**: #52b788
- **Accent**: #95d5b2
- **Cream**: #f8f9fa

## Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Setup Steps

1. **Clone the repository**
   ```bash
   cd kyagreen.com
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Collect static files** (for production)
   ```bash
   python manage.py collectstatic
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Website: http://localhost:8000
   - Admin Panel: http://localhost:8000/admin

## Project Structure

```
kyagreen.com/
├── core/                   # Core app (homepage, about, contact)
│   ├── models.py          # HomePage, InformationPage, ContactInfo
│   ├── views.py
│   ├── admin.py
│   └── templates/
├── products/              # Products app
│   ├── models.py          # Product, Category, ProductImage, ProductAttribute
│   ├── views.py
│   ├── admin.py
│   └── templates/
├── services/              # Services app
│   ├── models.py          # Service, ServiceFeature
│   ├── views.py
│   ├── admin.py
│   └── templates/
├── rfq/                   # Request for Quotation app
│   ├── models.py          # RFQRequest, RFQItem
│   ├── views.py
│   ├── forms.py
│   ├── admin.py
│   └── templates/
├── static/
│   ├── css/
│   │   └── style.css     # Custom styles
│   ├── js/
│   │   └── main.js       # jQuery functionality
│   └── images/
├── templates/
│   └── base.html         # Base template with navigation
├── media/                # Uploaded files
├── kiyagreen/           # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── requirements.txt
└── README.md
```

## Usage Guide

### Admin Panel

1. **Login to Admin**: Navigate to `/admin` and login with superuser credentials

2. **Manage Homepage**:
   - Go to "Core" → "Home Pages"
   - Add/edit homepage content, hero image, and welcome section
   - Only one homepage can be active at a time

3. **Add Products**:
   - Go to "Products" → "Products"
   - Fill in product details, upload images
   - Add product attributes and additional images inline
   - Mark products as "Featured" to show on homepage

4. **Manage Categories**:
   - Go to "Products" → "Categories"
   - Create parent and child categories
   - Set display order

5. **Add Services**:
   - Go to "Services" → "Services"
   - Add service details and features
   - Use Bootstrap icon classes for icons (e.g., bi-truck, bi-gear)

6. **Manage RFQ Requests**:
   - Go to "RFQ" → "RFQ Requests"
   - View customer requests
   - Update status (Pending, In Progress, Quoted, Completed)
   - Add admin notes

7. **Update Contact Information**:
   - Go to "Core" → "Contact Information"
   - Update address, phone, email, and map embed code

### Navigation Structure

- **Home**: Main landing page with featured products and services
- **Information**: About Us page with mission and vision
- **Products**: Product catalog with category filters
- **Services**: Services showcase
- **Contact**: Contact form and information
- **Request for Quotation**: Available on:
  - Navigation bar (general RFQ)
  - Product detail pages (product-specific RFQ)
  - Product listing cards

## Key Features Implementation

### Category Filtering
- Vertical list in product pages
- Hierarchical category support
- Parent/child relationships
- Filter products by category

### RFQ System
- **General RFQ**: From navigation or standalone page
- **Product-specific RFQ**: From product detail pages
- **Search/Select**: Autocomplete product search in forms
- Fields: Name, email, phone, company, address, quantity, message, attachments
- Status tracking in admin panel

### Search Functionality
- Product search by name, description, SKU
- AJAX autocomplete for quick selection
- jQuery-powered filtering

### Admin Content Management
- Rich text editor (CKEditor) for formatted content
- Image upload for products, services, pages
- Inline editing for related items (images, attributes, features)
- Bulk actions and filtering

## Customization

### Colors
Edit [static/css/style.css](static/css/style.css) to change theme colors:
```css
:root {
    --kiya-green: #2d6a4f;
    --kiya-green-dark: #1b4332;
    --kiya-green-light: #40916c;
    /* ... */
}
```

### Logo
Replace the leaf icon in [templates/base.html](templates/base.html#L22):
```html
<i class="bi bi-leaf-fill me-2"></i>KiyaGreen
```

### Footer
Edit [templates/base.html](templates/base.html#L76-L109) footer section

## Production Deployment

### Environment Variables
Create a `.env` file or set environment variables:
```
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=kiyagreen.com,www.kiyagreen.com
DATABASE_URL=postgresql://user:pass@localhost/dbname
```

### Settings Updates
Update [kiyagreen/settings.py](kiyagreen/settings.py):
- Set `DEBUG = False`
- Configure `ALLOWED_HOSTS`
- Use PostgreSQL database
- Configure email backend for RFQ notifications
- Set up static/media file serving (nginx/Apache)

### Security
- Change `SECRET_KEY`
- Enable HTTPS
- Configure CORS if needed
- Set up proper file upload restrictions
- Enable CSRF protection

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Mobile browsers

## License

Copyright © 2025 KiyaGreen. All rights reserved.

## Support

For issues or questions, please contact: info@kiyagreen.com

## Future Enhancements

- Email notifications for RFQ submissions
- PDF quote generation
- Customer accounts and order history
- Shopping cart functionality
- Payment gateway integration
- Multi-language support
- Advanced search filters
- Product reviews and ratings
