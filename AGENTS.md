# AGENTS.md — Guide for AI Agents

This repository contains the source code for **Feras Aldahlawi's (`frs`) personal website**, hosted on GitHub Pages at [https://therealfrs.github.io](https://therealfrs.github.io).

## Project Overview

- **Architecture**: Minimal static HTML5 and CSS3. Single-column hub (`index.html`) plus bare leaf pages (`user_manual.html` and `blog/*.html`) with zero runtime dependencies.
- **Markdown Blog Workflow**: Blog posts are written in Markdown inside `blog/posts/*.md` and compiled into `blog/<slug>.html` (and synced into the Writing list on `index.html`) via `python3 scripts/build_blog.py`.
- **Root-Relative Links**: All pages use root-relative paths (`/assets/style.css`, `/favicon.ico`, `/`, `/user_manual.html`, `/blog/<slug>.html`).
- **VCS**: Managed with Jujutsu (`jj`) / Git.

---

## Repository Structure

| Path | Description |
| :--- | :--- |
| `index.html` | Single-column home page with header links (email, schedule, live Google Doc resume, user manual), bio + photo, Writing list, Work (Google Disco & Chromium), Appearances links, JSON-LD `Person` schema, and deferred Google Analytics (`G-HF0QQE6EX6`). |
| `user_manual.html` | "Working with Feras" collaboration manual (bare single-column leaf page with section anchors + link to live Google Doc). |
| `blog/posts/*.md` | **Markdown source files** for blog posts (with YAML frontmatter). Edit or create posts here. |
| `blog/<slug>.html` | Auto-generated standalone blog post pages built from `blog/posts/<slug>.md`. |
| `assets/style.css` | Global stylesheet: deep maroon (`#800000`) accent, warm gray (`#ebe8e1`) desktop background, classic typography, and `.doc-body` Markdown styles. |
| `assets/feras.webp` / `.png` | Portrait photo of Feras Aldahlawi displayed on `index.html`. |
| `scripts/build_blog.py` | Compiles `blog/posts/*.md` into `blog/<slug>.html` and updates the `<!-- BLOG_SECTION_START -->...<!-- BLOG_SECTION_END -->` block in `index.html` (hiding the Writing section when no posts exist). Supports `--new <slug> ["Title"]` and `--check`. |
| `favicon.ico` | Site favicon kept at the root for default browser lookups. |
| `engineering_blogs.opml` | OPML subscription list of engineering blogs. |
| `dahlawis_family_tree/` | **Auto-generated** static genealogy site exported from **Gramps 5.1.6**. **Do not manually edit or format files in this directory** unless explicitly asked. |

---

## Workflows for Common Edits

### Writing or Editing a Blog Post (Markdown)
1. Scaffold a new post (or create `blog/posts/<slug>.md` directly):
   ```bash
   python3 scripts/build_blog.py --new <slug> "Your Post Title"
   ```
2. Edit `blog/posts/<slug>.md`. Frontmatter fields: `title`, `date` (`YYYY-MM-DD`), `category`, `author`, `summary`, `draft`.
3. Build the HTML pages and update `index.html`:
   ```bash
   python3 scripts/build_blog.py
   ```

### Local Preview
```bash
python3 -m http.server 8000
```
