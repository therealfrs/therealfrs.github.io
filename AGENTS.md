# AGENTS.md — Guide for AI Agents

This repository contains the source code for **Feras Aldahlawi's (`frs`) personal website**, hosted on GitHub Pages at [https://therealfrs.github.io](https://therealfrs.github.io).

## Project Overview

- **Architecture**: Pure static HTML5 and CSS3. There is **no build step**, bundler, package manager (`package.json`), or static site generator (Jekyll/Hugo). Files are served directly as committed.
- **Bilingual Support**: Most primary pages feature bilingual content in **English** (LTR) and **Arabic** (RTL, `dir="rtl"`).
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
| `blog/index.html` | Technical blog index listing published articles. |
| `blog/blog_post_*.html` | Individual blog post pages (use `../` relative paths for root stylesheet and navigation). |
| `style.css` | Global stylesheet defining the academic monospace theme, layout grid, bilingual typography, and mobile responsiveness. |
| `fonts/` | Self-hosted `.woff2` fonts (`aref-ruqaa.woff2` for traditional Arabic headers, `vt323.woff2`) and licenses. |
| `images/` & `favicon.ico` | Static icons and SVG graphics. |
| `engineering_blogs.opml` | OPML subscription list of engineering blogs. |
| `dahlawis_family_tree/` | **Auto-generated** static genealogy site exported from **Gramps 5.1.6**. **Do not manually edit or format files in this directory** unless explicitly asked. |

---

## Design & Layout Conventions

### 1. Page Skeleton
Because there is no templating engine, every main page (`*.html` and `blog/*.html`) duplicates a shared structural shell:
1. **Container**: `<div class="academic-container">`
2. **Header**: `<header class="academic-header">` containing `.header-title-row` (`<h1>Feras Aldahlawi</h1>` and `<span class="arabic">فراس الدهلوي</span>`) and `<p class="header-subtitle">Software Engineer</p>`.
3. **Navigation Bar**: `<nav class="academic-nav">` containing links to `Home`, `About`, `Resume`, `Podcasts`, `User Manual`, and `Blog`.
   - The link corresponding to the current page (or section, such as `Blog` for `blog/*.html`) must have `class="active"`.
   - Pages inside `blog/` must prefix root-level links and `style.css` with `../`.
4. **Two-Column Layout**: `<div class="academic-layout">`
   - `<aside class="academic-sidebar">`: Contact email (`frs@chromium.org`), Google Calendar scheduling button (`.btn-academic`), and optional status blocks.
   - `<main class="academic-main">`: The primary content area for the page.
5. **Footer**: `<footer class="academic-footer">` (`Made in Seattle &copy; 2026`).

### 2. Styling & Color Palette (`style.css`)
- **Primary Accent**: Maroon (`#800000`), hover states (`#d11a2a` for links, `#5a0000` for nav tabs).
- **Fonts**:
  - Default / English: System `ui-monospace` stack (`ui-monospace, SFMono-Regular, SF Mono, Menlo, Consolas, "Liberation Mono", monospace`).
  - Arabic Display Header (`.arabic`): `'Aref Ruqaa', serif`.
  - Arabic Body Copy (`.arabic-modern`): `"Tahoma", "Arial", "Simplified Arabic", sans-serif` with `direction: rtl`.
- **Responsive Breakpoint**: `@media (max-width: 768px)` stacks `.academic-layout` vertically and adjusts padding.

### 3. Bilingual Content Pattern
- Page `<title>` and `<h2>` headers typically include both languages separated by `|` or `/` (e.g., `About Feras Aldahlawi (frs) | عن فراس الدهلوي`).
- Short dual-language sections use `.bilingual-block`, placing the English paragraph first and the Arabic translation below it inside `<div class="arabic-section arabic-modern" dir="rtl">`.
- Longer pages (`resume.html`, `user_manual.html`) place the complete English version first, followed by a `.arabic-section.arabic-modern[dir="rtl"]` containing the complete Arabic version.

---

## Workflows for Common Edits

### Adding or Renaming Navigation Items
Because `<nav class="academic-nav">` is static across files, any change to the top navigation bar must be applied to **all** of the following files:
- `index.html` (also update the "Quick Navigation" `<ul>` in `<main>`)
- `about.html`
- `resume.html`
- `podcast.html`
- `user_manual.html`
- `blog/index.html`
- `blog/blog_post_1.html` (and any newer posts in `blog/`)

### Adding a New Blog Post
1. Duplicate `blog/blog_post_1.html` to `blog/<new_post_name>.html`.
2. Verify `<link rel="stylesheet" href="../style.css">` and `../` navigation links are intact, and `Blog` has `class="active"`.
3. Add a new `<li>` entry at the top of the article list in `blog/index.html` with the date, author (`frs`), link, and summary.

### Updating Bilingual Content
When asked to update biographical info, resume bullets, or user manual entries, always check whether the page has a corresponding Arabic section (`dir="rtl"`) and keep both English and Arabic versions synchronized unless instructed otherwise.

### Local Preview
To preview or test the site locally without external dependencies:
```bash
python3 -m http.server 8000
```
