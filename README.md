# Feras Aldahlawi (`frs`) — Personal Website

Source code for [https://therealfrs.github.io](https://therealfrs.github.io).

## Writing a New Blog Post

Blog posts are written in Markdown inside [`blog/posts/`](blog/posts/) and compiled locally into static HTML. See **[`blog/README.md`](blog/README.md)** for full details.

```bash
# 1. Create a new Markdown post template
python3 scripts/build_blog.py --new my_post_slug "My Post Title"

# 2. Edit blog/posts/my_post_slug.md

# 3. Compile Markdown posts into blog/*.html and update blog/index.html
python3 scripts/build_blog.py

# 4. Preview locally at http://localhost:8000
python3 -m http.server 8000
```

## Updating Shared Site Layout (Header, Nav, Sidebar, Footer)

To update the navigation bar, header, contact sidebar, or footer across all pages at once:
1. Edit [`scripts/sync_layout.py`](scripts/sync_layout.py).
2. Run:
   ```bash
   python3 scripts/sync_layout.py
   ```
