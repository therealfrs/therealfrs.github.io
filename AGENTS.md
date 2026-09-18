# AGENTS.md — Guide for AI Agents

This repository contains the source code for **Feras Aldahlawi's (`frs`) personal website**, hosted on GitHub Pages at [https://therealfrs.github.io](https://therealfrs.github.io).

## Project Overview

- **Architecture**: Pure static HTML5 and CSS3. Every `.html` file is standalone so it can be served directly by GitHub Pages or `python3 -m http.server` with zero runtime dependencies.
- **Markdown Blog Workflow**: Blog posts are written in Markdown inside `blog/posts/*.md` and compiled locally into styled HTML pages (`blog/*.html` and `blog/index.html`) via `python3 scripts/build_blog.py`.
- **Root-Relative Links**: All pages (`/*.html` and `/blog/*.html`) use root-relative paths (`/assets/style.css`, `/favicon.ico`, `/index.html`, `/about.html`, `/blog/index.html`) so boilerplate blocks remain identical at any directory depth.
- **Shared Layout Sync**: `scripts/sync_layout.py` is the single source of truth for the shared `<header>`, `<nav>`, `<aside>`, and `<footer>` blocks across all HTML pages.
- **Bilingual Support**: Primary pages feature bilingual content in **English** (LTR) and **Arabic** (RTL, `dir="rtl"`).
- **VCS**: Managed with Jujutsu (`jj`) / Git.

---

## Repository Structure

| Path | Description |
| :--- | :--- |
| `index.html` | Home page with welcome text, bilingual quick navigation, JSON-LD `Person` schema, and deferred Google Analytics (`G-HF0QQE6EX6`). |
| `about.html` | Biographical and career summary in English and Arabic. |
| `resume.html` | Full Curriculum Vitae / Resume in English and Arabic, plus links to the live Google Doc. |
| `podcast.html` | Embedded RedCircle audio players for podcast appearances. |
| `user_manual.html` | "Working with Feras" personal user manual in English and Arabic, plus links to the live document. |
| `blog/posts/*.md` | **Markdown source files** for blog posts (with YAML frontmatter). Edit or create posts here. |
| `blog/index.html` | Auto-generated technical blog index listing published articles. |
| `blog/<slug>.html` | Auto-generated standalone blog post pages built from `blog/posts/<slug>.md`. |
| `assets/style.css` | Global stylesheet defining the academic monospace theme, layout grid, bilingual typography, Markdown `.post-body` styles, and mobile responsiveness. |
| `assets/fonts/` | Self-hosted `.woff2` font (`aref-ruqaa.woff2` for traditional Arabic headers) and license. |
| `scripts/build_blog.py` | Compiles `blog/posts/*.md` into `blog/<slug>.html` and updates `blog/index.html`. Supports `--new <slug> ["Title"]` and `--check`. |
| `scripts/sync_layout.py` | Synchronizes the shared header, navigation bar, sidebar, and footer across all `.html` files. |
| `favicon.ico` | Site favicon kept at the root for default browser lookups. |
| `engineering_blogs.opml` | OPML subscription list of engineering blogs. |
| `dahlawis_family_tree/` | **Auto-generated** static genealogy site exported from **Gramps 5.1.6**. **Do not manually edit or format files in this directory** unless explicitly asked. |

---

## Design & Layout Conventions

### 1. Page Skeleton & `scripts/sync_layout.py`
Every main page (`*.html` and `blog/*.html`) shares a common structural shell managed by `scripts/sync_layout.py`:
1. **Container**: `<div class="academic-container">`
2. **Header**: `<header class="academic-header">` containing `.header-title-row` (`<h1>Feras Aldahlawi</h1>` and `<span class="arabic">فراس الدهلوي</span>`) and `<p class="header-subtitle">Software Engineer</p>`.
3. **Navigation Bar**: `<nav class="academic-nav">` containing root-relative links to `/index.html`, `/about.html`, `/resume.html`, `/podcast.html`, `/user_manual.html`, and `/blog/index.html`.
   - The link corresponding to the current page (or section, such as `/blog/index.html` for `blog/*.html`) gets `class="active"`.
4. **Two-Column Layout**: `<div class="academic-layout">`
   - `<aside class="academic-sidebar">`: Contact email (`frs@chromium.org`), Google Calendar scheduling button (`.btn-academic`), and optional status blocks on `index.html`.
   - `<main class="academic-main">`: The primary content area for the page.
5. **Footer**: `<footer class="academic-footer">` (`Made in Seattle &copy; 2026`).

### 2. Styling & Reusable CSS Classes (`assets/style.css`)
- **Primary Accent**: Maroon (`#800000`), hover states (`#d11a2a` for links, `#5a0000` for nav tabs).
- **Fonts**:
  - Default / English: System `ui-monospace` stack (`ui-monospace, SFMono-Regular, SF Mono, Menlo, Consolas, "Liberation Mono", monospace`).
  - Arabic Display Header (`.arabic`): `'Aref Ruqaa', serif`.
  - Arabic Body Copy (`.arabic-modern`): `"Tahoma", "Arial", "Simplified Arabic", sans-serif` with `direction: rtl`.
- **Semantic Component Classes** (prefer these over inline `style="..."` attributes):
  - Bilingual / RTL utilities: `.bilingual-block`, `.arabic-section`, `.arabic-section--relaxed`, `.arabic-accent-heading`.
  - Resume: `.resume-contact-header`, `.resume-section-title`, `.experience-entry`, `.education-entry`, `.entry-header`, `.entry-subtitle`.
  - User Manual: `.manual-section`, `.manual-header`.
  - Podcasts: `.podcast-list`, `.podcast-container`, `.podcast-iframe`.
  - Blog & Markdown: `.blog-list`, `.blog-list-item`, `.post-meta`, `.post-body` (styles headings, `code`, `pre`, `blockquote`, `table`, `img`, `hr`, and `dir="rtl"`).
  - Shared Callouts & Footer Nav: `.doc-callout`, `.doc-callout-label`, `.doc-callout-actions`, `.page-footer-nav`, `.back-link`.

---

## Workflows for Common Edits

### Writing or Editing a Blog Post (Markdown)
1. Scaffold a new post (or create `blog/posts/<slug>.md` directly):
   ```bash
   python3 scripts/build_blog.py --new <slug> "Your Post Title"
   ```
2. Edit `blog/posts/<slug>.md`. Frontmatter fields supported:
   - `title`: Post title
   - `date`: `YYYY-MM-DD` (controls sorting on `blog/index.html`)
   - `category`: Topic label (e.g., `Cryptography & Media`)
   - `author`: Defaults to `frs`
   - `summary`: Short description displayed on `blog/index.html`
   - `dir`: `ltr` (default, English) or `rtl` (Arabic)
   - `draft`: `true` to hide from build/index, `false` to publish
3. Build the HTML pages and index locally before committing/pushing:
   ```bash
   python3 scripts/build_blog.py
   ```

### Updating the Header, Navigation Bar, Sidebar, or Footer
1. Edit `NAV_ITEMS`, `HEADER_HTML`, `build_sidebar_html()`, or `FOOTER_HTML` inside `scripts/sync_layout.py`.
2. Run:
   ```bash
   python3 scripts/sync_layout.py
   ```
   This updates all HTML files in the root and `blog/` directories in-place and sets `class="active"` on the appropriate navigation link.

### Updating Bilingual Content
When asked to update biographical info, resume bullets, or user manual entries, always check whether the page has a corresponding Arabic section (`dir="rtl"`) and keep both English and Arabic versions synchronized unless instructed otherwise.

### Local Preview
To preview or test the site locally:
```bash
python3 -m http.server 8000
```
