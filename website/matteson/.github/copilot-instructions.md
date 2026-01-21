# Matteson Housing Study Dashboard - AI Coding Guidelines

## Project Overview
This is a static HTML website for the Matteson Housing Needs and Workforce Housing Assessment dashboard. It presents housing data visualizations, demographic insights, and maps using embedded charts and static content. No build process or dynamic backend - all files are served directly.

## Architecture
- **Static Site Structure**: Multiple HTML pages (`index.html`, `munimap.html`) with shared styling and scripts.
- **Data Sources**: 
  - Embedded Datawrapper iframes for interactive charts (e.g., population trends, housing stock analysis).
  - Static CSV files (`rental_listings.csv`, `sales_listings.csv`) for real estate data.
  - Local images in `/images/` folder for illustrations.
- **External Dependencies**: Tailwind CSS (CDN), Material Icons, Google Fonts, Google Analytics.

## Key Patterns & Conventions
- **Layout Structure**: Use card-based design with `sm:mx-auto sm:max-w-3xl` containers. Each section follows: header (`px-4 py-5 sm:px-6`), content (`px-4 py-5 sm:p-6`), with flex layouts for text/images/charts.
- **Responsive Design**: Leverage Tailwind's responsive prefixes (`sm:`, `md:`, `lg:`). Example: `flex flex-col md:flex-row gap-6` for side-by-side content on larger screens.
- **Chart Integration**: Embed Datawrapper iframes with responsive scripts. Always include the height-adjustment script: `window.addEventListener("message", function(a) { ... });`
- **Interactive Elements**: Simple vanilla JS for toggles (e.g., mobile menu, expandable sections). Use `classList.toggle('hidden')` and event listeners.
- **SEO & Meta Tags**: Comprehensive meta tags for OpenGraph, Twitter Cards, and favicons. Update `og:image` and `og:url` for new pages.
- **Image Usage**: Reference images from `./images/` with descriptive alt text. Example: `<img src="images/townhome.png" alt="Townhome example">`

## Development Workflow
- **Editing**: Modify HTML files directly in VS Code. No compilation needed.
- **Testing**: Open files locally in browser or use VS Code's Live Server extension for real-time preview.
- **Deployment**: Push to GitHub; likely hosted on GitHub Pages or static server. No build commands required.
- **Data Updates**: Update CSV files manually; charts are managed externally in Datawrapper.
- **Version Control**: Commit HTML, images, and data files. Ignore `.DS_Store`.

## Common Tasks
- **Adding New Section**: Copy a card div from `index.html` (e.g., lines 300-400), update title, description, and embed new Datawrapper iframe.
- **Updating Charts**: Replace iframe `src` with new Datawrapper URL, ensure responsive script is included.
- **Styling Changes**: Use Tailwind classes; avoid custom CSS unless necessary (add to `<style>` tag).
- **New Page**: Duplicate `index.html` structure, update meta tags, and link from navigation.

## Key Files
- `index.html`: Main dashboard with population, housing, and affordability sections.
- `munimap.html`: Interactive map page with census and listing data.
- `images/`: Housing-related photos (e.g., `apts.jpg`, `townhome.png`).
- CSV files: Real estate data for analysis.