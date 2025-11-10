# KiyaGreen - Product Image Guidelines

This document outlines the recommended image specifications for optimal performance and display quality on the KiyaGreen e-commerce platform.

## Product Images

### 1. Product Thumbnail (List/Grid View)
Used in product listing pages, category pages, and search results.

**Specifications:**
- **Dimensions:** 300x300 pixels (minimum 150x150, maximum 300x300)
- **Aspect Ratio:** Square (1:1 ratio)
- **File Format:** JPEG or WebP
- **File Size:** Under 100 KB
- **Compression:** High quality (85-90%)
- **Color Space:** sRGB

**Best Practices:**
- Center the product in the frame
- Use white or light neutral background
- Ensure good lighting with no harsh shadows
- Show the product from the front or most recognizable angle

### 2. Product Main Image (Detail Page)
Used as the primary image on product detail pages with zoom functionality.

**Specifications:**
- **Dimensions:** 800x800 to 1200x1200 pixels
- **Aspect Ratio:** Square (1:1) or product-specific (4:3, 16:9 for special items)
- **File Format:** JPEG for photos, WebP for better compression
- **File Size:** Under 500 KB (ideally 200-300 KB)
- **Compression:** Medium-high quality (80-85%)
- **Color Space:** sRGB

**Best Practices:**
- Use high resolution for zoom functionality
- Maintain consistent lighting across all product images
- Include product details visible at high zoom
- Remove background or use consistent background color
- Show product dimensions accurately

### 3. Product Gallery Images
Additional images showing different angles, details, or usage scenarios.

**Specifications:**
- **Dimensions:** 800x800 to 1200x1200 pixels (same as main image)
- **Aspect Ratio:** Square (1:1)
- **File Format:** JPEG or WebP
- **File Size:** Under 500 KB per image
- **Compression:** Medium-high quality (80-85%)

**Recommended Gallery Images:**
1. Front view (main image)
2. Back view
3. Side views (left/right)
4. Close-up of important details
5. Product in use/lifestyle shots
6. Size comparison or scale reference

### 4. Gallery Thumbnails
Small preview images for the gallery selector.

**Specifications:**
- **Dimensions:** 150x150 pixels
- **Aspect Ratio:** Square (1:1)
- **File Format:** JPEG or WebP
- **File Size:** Under 50 KB
- **Compression:** High quality (85-90%)

## Category Images

**Specifications:**
- **Dimensions:** 300x300 pixels
- **Aspect Ratio:** Square (1:1)
- **File Format:** JPEG or WebP
- **File Size:** Under 100 KB
- **Compression:** High quality (85-90%)

**Best Practices:**
- Use representative product or icon for the category
- Maintain consistent style across all category images
- Use clear, recognizable imagery

## Homepage/Hero Images

**Specifications:**
- **Dimensions:** 1920x1080 pixels (Full HD)
- **Aspect Ratio:** 16:9 or custom
- **File Format:** JPEG or WebP
- **File Size:** Under 500 KB
- **Compression:** Medium quality (70-80%)

## Technical Implementation

### Image Optimization Tools
- **Online Tools:**
  - TinyPNG (https://tinypng.com/)
  - Squoosh (https://squoosh.app/)
  - ImageOptim (Mac)

- **Command Line:**
  - ImageMagick
  - JPEGoptim
  - OptiPNG

### Lazy Loading
All product images use lazy loading to improve page load performance:
```html
<img src="product.jpg" loading="lazy" alt="Product Name">
```

### Responsive Images
Images automatically adapt to different screen sizes using CSS:
- Desktop: Full resolution
- Tablet: Scaled proportionally
- Mobile: Optimized for smaller screens

### WebP Format
WebP provides better compression than JPEG:
- 25-35% smaller file sizes
- Better quality at same file size
- Supported by all modern browsers

### Alt Text
Always include descriptive alt text for:
- Accessibility (screen readers)
- SEO optimization
- Fallback when images don't load

**Good Alt Text Examples:**
- ✅ "Green bamboo eco-friendly water bottle, 500ml capacity"
- ✅ "Recycled cotton tote bag with natural handles"
- ❌ "product image" (too generic)
- ❌ "IMG_1234.jpg" (not descriptive)

## Image Naming Conventions

Use descriptive, SEO-friendly filenames:

**Good Examples:**
- `bamboo-water-bottle-green-500ml.jpg`
- `organic-cotton-tshirt-blue-large.jpg`
- `recycled-yoga-mat-purple.jpg`

**Bad Examples:**
- `IMG_1234.jpg`
- `product1.jpg`
- `image-final-v2-FINAL.jpg`

## Quality Checklist

Before uploading product images, ensure:
- [ ] Image meets recommended dimensions
- [ ] File size is optimized (under recommended limits)
- [ ] Background is clean or removed
- [ ] Product is well-lit and in focus
- [ ] Colors are accurate and consistent
- [ ] No watermarks or competitor branding visible
- [ ] Aspect ratio is correct (preferably square 1:1)
- [ ] File has descriptive name
- [ ] Alt text is descriptive and SEO-friendly

## Django Admin Integration

When uploading images through Django admin, you'll see helpful guidelines:

- **Main Product Image:** "Recommended: 800x800 to 1200x1200px (Square 1:1), JPEG/WebP, under 500KB"
- **Gallery Images:** "Recommended: 800x800 to 1200x1200px (Square 1:1), JPEG/WebP, under 500KB"
- **Category Images:** "Recommended: 300x300px (Square 1:1), JPEG/WebP, under 100KB"

## Performance Tips

1. **Batch Optimization:** Optimize all images before uploading
2. **Consistent Dimensions:** Use the same dimensions for similar image types
3. **Progressive JPEGs:** Enable progressive rendering for large images
4. **CDN Usage:** Consider using a CDN for faster image delivery
5. **Responsive Images:** Use srcset for different screen sizes
6. **Image Sprites:** Combine small icons into sprites when possible

## Browser Support

All image optimizations are compatible with:
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+
- Mobile browsers (iOS Safari, Chrome Mobile)

## Questions?

For technical support or questions about image optimization, please contact the development team.

---

**Last Updated:** January 2025
**Version:** 1.0
