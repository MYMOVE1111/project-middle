# CSS Styling Documentation

## Overview
Complete CSS styling system for the Django Recipe Sharing Application using custom styles combined with Bootstrap 5.1.3.

## File Structure
```
static/css/
├── style.css           - Main custom styles (1000+ lines)
└── utilities.css       - Responsive utilities and helpers
```

## Static Files Configuration

### Django Settings (settings.py)
```python
STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
```

### URL Configuration (urls.py)
```python
from django.conf.urls.static import static
from django.conf import settings

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### Template Usage (base.html)
```django
{% load static %}
<link rel="stylesheet" href="{% static 'css/style.css' %}">
<link rel="stylesheet" href="{% static 'css/utilities.css' %}">
```

## Color Scheme

### Primary Palette
- **Primary Green**: `#2ecc71` - Main brand color
- **Primary Dark**: `#27ae60` - Hover/accent state
- **Primary Light**: `#52d273` - Highlights

### Supporting Colors
- **Secondary Blue**: `#3498db` - Secondary actions
- **Warning**: `#f39c12` - Warnings and alerts
- **Danger**: `#e74c3c` - Destructive actions
- **Success**: `#27ae60` - Success messages

### Neutral Colors
- **Dark**: `#2c3e50` - Text and dark backgrounds
- **Light**: `#ecf0f1` - Light backgrounds
- **Gray**: `#95a5a6` - Muted text
- **Gray Light**: `#bdc3c7` - Subtle borders

## CSS Variables

### Spacing System
```css
--spacing-xs: 0.25rem    /* 4px */
--spacing-sm: 0.5rem     /* 8px */
--spacing-md: 1rem       /* 16px */
--spacing-lg: 1.5rem     /* 24px */
--spacing-xl: 2rem       /* 32px */
--spacing-2xl: 3rem      /* 48px */
```

### Border Radius
```css
--border-radius-sm: 0.25rem    /* 4px */
--border-radius: 0.5rem        /* 8px */
--border-radius-lg: 1rem       /* 16px */
```

### Shadows
```css
--shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05)
--shadow: 0 1px 3px rgba(0, 0, 0, 0.1), 0 1px 2px rgba(0, 0, 0, 0.06)
--shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1), 0 2px 4px rgba(0, 0, 0, 0.06)
--shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1), 0 4px 6px rgba(0, 0, 0, 0.05)
--shadow-xl: 0 20px 25px rgba(0, 0, 0, 0.1), 0 10px 10px rgba(0, 0, 0, 0.04)
```

### Transitions
```css
--transition: all 0.3s ease
--transition-fast: all 0.15s ease
--transition-slow: all 0.5s ease
```

## Components

### Navbar
- Sticky positioning at top
- Green gradient background
- Responsive hamburger menu
- Icon-enhanced navigation links
- User welcome message when authenticated

```html
<nav class="navbar navbar-expand-lg">
    <!-- Navbar content with custom styling -->
</nav>
```

### Hero Section
- Page header with title and description
- Center-aligned text
- Call-to-action buttons
- Responsive padding

### Statistics Cards
Three card styles with gradients:
- `.stats-card` - Green gradient
- `.stats-card.blue` - Blue gradient
- `.stats-card.warning` - Orange gradient
- `.stats-card.danger` - Red gradient

```html
<div class="stats-card">
    <div class="stats-label">Total Recipes</div>
    <div class="stats-value">42</div>
</div>
```

### Recipe Cards
- Image placeholder with gradient background
- Title truncation
- Meta information (time, difficulty, rating)
- Tag badges
- Hover animation (lift effect)

```html
<div class="recipe-card">
    <img src="..." class="recipe-card-image">
    <div class="recipe-card-body">
        <h3 class="recipe-card-title">Recipe Title</h3>
        <p class="recipe-card-description">...</p>
        <div class="recipe-card-meta">...</div>
    </div>
</div>
```

### Category Cards
- Center-aligned content
- Icon display area
- Recipe count badge
- Hover animation

```html
<div class="category-card">
    <div class="category-icon">🍝</div>
    <h3 class="category-title">Category Name</h3>
    <div class="category-count">24 recipes</div>
</div>
```

### Comments
- Left border indicator
- Author name and timestamp
- Comment text
- Like counter
- Edit indicator

```html
<div class="comment">
    <div class="comment-author">Username</div>
    <div class="comment-meta">Posted on Date (Edited)</div>
    <div class="comment-text">Comment content...</div>
</div>
```

### Buttons
Multiple button styles:
- `.btn-primary` - Green gradient
- `.btn-secondary` - Blue
- `.btn-success` - Green
- `.btn-danger` - Red
- `.btn-warning` - Orange
- `.btn-outline-primary` - Outlined green

Sizes:
- `.btn-sm` - Small
- `.btn` - Default
- `.btn-lg` - Large

### Forms
- Blue border on focus
- Rounded corners
- Smooth transitions
- Custom label styling

```html
<input class="form-control" type="text">
<textarea class="form-control">...</textarea>
<select class="form-select">...</select>
```

### Badges
Color variants:
- `.badge.bg-primary` - Green
- `.badge.bg-success` - Green checkmark
- `.badge.bg-warning` - Orange
- `.badge.bg-danger` - Red
- `.badge.bg-info` - Blue
- `.badge.bg-light` - Light gray

### Alerts
Styled notification boxes:
- `.alert-success` - Green with left border
- `.alert-danger` - Red with left border
- `.alert-warning` - Orange with left border
- `.alert-info` - Blue with left border

### Lists
- `.list-group` - Styled list container
- `.list-group-item` - Individual items
- Hover effect with left padding increase
- Active state styling

### Pagination
- Green primary buttons
- Rounded corners
- Hover animations
- Disabled state support

### Breadcrumb
- Transparent background
- Link styling
- Active item styling
- Separator indicators

### Sidebar
- White background with shadow
- Title with bottom border
- Item list with dividers
- Count badges

```html
<div class="sidebar">
    <h3 class="sidebar-title">Sidebar Title</h3>
    <div class="sidebar-item">
        <a href="#" class="sidebar-link">Link</a>
        <span class="sidebar-count">42</span>
    </div>
</div>
```

### Footer
- Dark gradient background
- Multiple sections for links
- Social media icons
- Copyright information

## Animations

### Fade In
```css
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}
.fade-in { animation: fadeIn 0.3s ease; }
```

### Slide In Left
```css
@keyframes slideInLeft {
    from { opacity: 0; transform: translateX(-20px); }
    to { opacity: 1; transform: translateX(0); }
}
.slide-in-left { animation: slideInLeft 0.3s ease; }
```

### Pulse
```css
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}
.pulse { animation: pulse 1s ease-in-out infinite; }
```

## Responsive Breakpoints

### Bootstrap Breakpoints (inherited)
- `xs` - < 576px (mobile)
- `sm` - ≥ 576px (mobile landscape)
- `md` - ≥ 768px (tablet)
- `lg` - ≥ 992px (desktop)
- `xl` - ≥ 1200px (large desktop)
- `xxl` - ≥ 1400px (extra large)

### Media Queries Used
```css
@media (max-width: 768px) { /* Tablet and below */ }
@media (max-width: 576px) { /* Mobile devices */ }
```

### Responsive Adjustments
- Hero text sizes reduce on smaller screens
- Statistics cards stack vertically on mobile
- Recipe cards adjust image heights
- Navbar collapses to hamburger menu
- Sidebar moves below content on mobile
- Button widths adjust for mobile

## Utility Classes

### Display
- `.d-flex` - Display flex
- `.d-none` - Display none
- `.d-block` - Display block
- `.d-inline` - Display inline
- `.d-inline-block` - Display inline-block

### Flexbox
- `.flex-column` - Flex direction column
- `.flex-wrap` - Flex wrap
- `.justify-content-center` - Center content
- `.justify-content-between` - Space between
- `.align-items-center` - Center items

### Spacing
- `.mt-1` to `.mt-4` - Margin top
- `.mb-1` to `.mb-4` - Margin bottom
- `.px-1` to `.px-3` - Padding horizontal
- `.py-1` to `.py-3` - Padding vertical
- `.gap-1` to `.gap-3` - Gap between flex items

### Text
- `.text-center` - Text align center
- `.text-primary` - Green text
- `.text-secondary` - Blue text
- `.text-muted` - Gray text
- `.text-dark` - Dark text
- `.text-white` - White text

### Backgrounds
- `.bg-light` - Light background
- `.bg-primary` - Green background
- `.bg-secondary` - Blue background

### Rounded
- `.rounded` - Border radius lg
- `.rounded-sm` - Border radius sm
- `.rounded-full` - Full circular

### Shadows
- `.shadow` - Default shadow
- `.shadow-md` - Medium shadow
- `.shadow-lg` - Large shadow

### Other
- `.cursor-pointer` - Pointer cursor
- `.no-decoration` - Remove text decoration
- `.hidden` - Display none
- `.visible` - Display block
- `.opacity-50` - 50% opacity
- `.opacity-75` - 75% opacity
- `.text-truncate` - Truncate text with ellipsis

## Grid Layout

### CSS Grid Classes
```css
.grid - Display grid
.grid-cols-1 - 1 column
.grid-cols-2 - 2 columns
.grid-cols-3 - 3 columns (2 on tablet, 1 on mobile)
.grid-cols-4 - 4 columns (2 on tablet, 1 on mobile)
```

## Accessibility Features

- ✅ Color contrast meets WCAG AA standards
- ✅ Semantic HTML structure
- ✅ Focus states for interactive elements
- ✅ Reduced motion support
- ✅ Print-friendly styles
- ✅ Font icons from Font Awesome
- ✅ Responsive text sizes

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## Performance

- Minified CSS on production
- CSS variables for easy customization
- Optimized media queries
- Efficient selectors
- No unnecessary animations

## Dark Mode Support

Future implementation placeholder:
```css
@media (prefers-color-scheme: dark) {
    /* Dark mode styles */
}
```

## Print Styles

- `.no-print` - Hidden when printing
- Navigation and footer hidden
- White background
- Black text
- Black links with underline
- Page break support

## Customization

To customize colors, modify CSS variables in `style.css`:

```css
:root {
    --primary: #2ecc71;           /* Change primary color */
    --primary-dark: #27ae60;      /* Change primary dark */
    --spacing-md: 1rem;           /* Change spacing */
    --border-radius: 0.5rem;      /* Change radius */
}
```

## Integration

### In Django Templates
```django
{% load static %}

<!-- In head -->
<link rel="stylesheet" href="{% static 'css/style.css' %}">

<!-- In HTML -->
<div class="btn btn-primary">Click me</div>
<div class="stats-card">Content</div>
```

### Bootstrap Classes Used
- `.container`, `.container-fluid`
- `.row`, `.col-*`
- `.card`, `.card-body`, `.card-header`
- `.btn`, `.btn-*`
- `.nav`, `.navbar`
- `.alert`, `.badge`
- `.form-control`, `.form-select`
- `.pagination`, `.list-group`

## File Sizes

- `style.css` - ~45KB (unminified)
- `utilities.css` - ~15KB (unminified)
- **Total**: ~60KB (easily minified to ~20KB)

## Loading Performance

All CSS loaded synchronously in `<head>`:
1. Bootstrap CDN (latest)
2. Font Awesome CDN (latest)
3. Custom style.css
4. Utilities CSS

No render-blocking JavaScript before content.

## Conclusion

Comprehensive CSS styling system with:
- ✅ Custom color scheme
- ✅ Reusable components
- ✅ Responsive design
- ✅ Smooth animations
- ✅ Accessibility support
- ✅ Easy customization
- ✅ Bootstrap integration
