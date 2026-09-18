# Writing & Publishing Blog Posts

All blog posts are written in **Markdown** inside [`blog/posts/`](./posts/) and compiled locally into static HTML pages (`blog/<slug>.html` and [`blog/index.html`](./index.html)) using [`scripts/build_blog.py`](../scripts/build_blog.py).

---

## Quick Start (3 Steps)

### 1. Create a New Markdown Post
From the repository root, run:
```bash
python3 scripts/build_blog.py --new <slug> "Your Post Title"
```
**Example:**
```bash
python3 scripts/build_blog.py --new chrome_eme_latency "Optimizing Chrome EME Latency"
```
This creates `blog/posts/chrome_eme_latency.md` with pre-filled frontmatter.

---

### 2. Write Your Post in `blog/posts/<slug>.md`
Open `blog/posts/<slug>.md` in your editor. Every post starts with a metadata block between `---` lines:

```markdown
---
title: "Optimizing Chrome EME Latency"
date: 2026-09-18
category: Cryptography & Media
author: frs
summary: "How we reduced encrypted video playback startup latency by 10.3x in Chrome Desktop."
dir: ltr
draft: false
---

Write your content here using standard **Markdown**.

## Subheading

Here is inline `code` and a fenced code block:

```cpp
void InitializeCdm() {
  // ...
}
```

> Blockquotes, tables, bullet lists, and links are all automatically styled.
```

#### Frontmatter Fields Reference
| Field | Default | Description |
| :--- | :--- | :--- |
| `title` | Derived from filename | Title displayed on the post page and `blog/index.html`. |
| `date` | Today (`YYYY-MM-DD`) | Publication date. Posts on `blog/index.html` are sorted newest-first by this date. |
| `category` | `Engineering` | Topic tag displayed next to the publication date. |
| `author` | `frs` | Author name shown on `blog/index.html`. |
| `summary` | First 180 chars of post | Short description shown under the title on `blog/index.html`. |
| `dir` | `ltr` | Set to `ltr` for English posts, or `rtl` for Arabic posts (automatically applies right-to-left layout and Arabic typography). |
| `draft` | `false` | Set to `true` while working on a draft so `build_blog.py` skips publishing it. Set back to `false` when ready. |

---

### 3. Build HTML Locally & Preview
Compile your `.md` files into `blog/<slug>.html` and update `blog/index.html`:
```bash
python3 scripts/build_blog.py
```

Preview locally in your browser at `http://localhost:8000/blog/index.html`:
```bash
python3 -m http.server 8000
```

When everything looks good, commit and push both the `.md` source file and the generated `.html` files.

---

## Useful Commands Cheat Sheet

| Task | Command |
| :--- | :--- |
| Scaffold a new post | `python3 scripts/build_blog.py --new <slug> "Post Title"` |
| Build all blog HTML & update `blog/index.html` | `python3 scripts/build_blog.py` |
| Check if HTML files are in sync with `.md` sources | `python3 scripts/build_blog.py --check` |
| Sync global header/nav/sidebar/footer across site | `python3 scripts/sync_layout.py` |
| Preview site locally | `python3 -m http.server 8000` |
