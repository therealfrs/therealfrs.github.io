#!/usr/bin/env python3
"""Builds HTML blog posts and blog/index.html from Markdown files in blog/posts/*.md.

Usage:
  python3 scripts/build_blog.py                             # Build all posts &
  blog/index.html
  python3 scripts/build_blog.py --new <slug> ["Post Title"] # Create a new .md
  post template
  python3 scripts/build_blog.py --check                     # Check if generated
  HTML is up-to-date
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
import html
from pathlib import Path
import re
import sys

from sync_layout import FOOTER_HTML, HEADER_HTML, build_nav_html, build_sidebar_html

ROOT = Path(__file__).resolve().parent.parent
POSTS_DIR = ROOT / "blog" / "posts"
BLOG_DIR = ROOT / "blog"


@dataclass
class BlogPost:
  slug: str
  title: str
  pub_date: date
  category: str
  author: str
  summary: str
  direction: str
  draft: bool
  body_html: str
  source_path: Path

  @property
  def formatted_date(self) -> str:
    return (
        f"{self.pub_date.strftime('%B')} {self.pub_date.day},"
        f" {self.pub_date.year}"
    )

  @property
  def output_path(self) -> Path:
    return BLOG_DIR / f"{self.slug}.html"


def parse_frontmatter(raw_text: str) -> tuple[dict[str, str], str]:
  """Extracts YAML-like frontmatter between --- delimiters and returns (metadata, body)."""
  text = raw_text.lstrip("\ufeff")
  if not text.startswith("---\n") and not text.startswith("---\r\n"):
    return {}, text

  match = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n?(.*)$", text, flags=re.DOTALL)
  if not match:
    return {}, text

  fm_block, body = match.group(1), match.group(2)
  meta: dict[str, str] = {}
  for line in fm_block.splitlines():
    line = line.strip()
    if not line or line.startswith("#") or ":" not in line:
      continue
    key, val = line.split(":", 1)
    key = key.strip().lower()
    val = val.strip()
    if len(val) >= 2 and (
        (val[0] == '"' and val[-1] == '"') or (val[0] == "'" and val[-1] == "'")
    ):
      val = val[1:-1]
    meta[key] = val
  return meta, body.strip()


def _fallback_markdown_to_html(md_text: str) -> str:
  """Zero-dependency fallback Markdown renderer if python3-markdown is unavailable."""
  lines = md_text.splitlines()
  out: list[str] = []
  in_code = False
  code_buf: list[str] = []
  in_ul = False
  para_buf: list[str] = []

  def flush_para() -> None:
    if para_buf:
      text = " ".join(para_buf)
      text = _inline_format(text)
      out.append(f"<p>{text}</p>")
      para_buf.clear()

  def close_list() -> None:
    nonlocal in_ul
    if in_ul:
      out.append("</ul>")
      in_ul = False

  def _inline_format(s: str) -> str:
    s = html.escape(s, quote=False)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", s)
    s = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", r'<img alt="\1" src="\2">', s)
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', s)
    return s

  for line in lines:
    if line.strip().startswith("```"):
      flush_para()
      close_list()
      if in_code:
        out.append(
            "<pre><code>" + html.escape("\n".join(code_buf)) + "</code></pre>"
        )
        code_buf.clear()
        in_code = False
      else:
        in_code = True
      continue

    if in_code:
      code_buf.append(line)
      continue

    stripped = line.strip()
    if not stripped:
      flush_para()
      close_list()
      continue

    if re.match(r"^---+$", stripped):
      flush_para()
      close_list()
      out.append("<hr>")
      continue

    heading_match = re.match(r"^(#{1,4})\s+(.*)$", stripped)
    if heading_match:
      flush_para()
      close_list()
      level = len(heading_match.group(1))
      # Shift h1 inside post body to h2 so page title remains h2
      tag_level = min(level + 1 if level == 1 else level, 4)
      out.append(
          f"<h{tag_level}>{_inline_format(heading_match.group(2))}</h{tag_level}>"
      )
      continue

    if stripped.startswith(">"):
      flush_para()
      close_list()
      quote_text = stripped.lstrip(">").strip()
      out.append(
          f"<blockquote><p>{_inline_format(quote_text)}</p></blockquote>"
      )
      continue

    if stripped.startswith("- ") or stripped.startswith("* "):
      flush_para()
      if not in_ul:
        out.append("<ul>")
        in_ul = True
      out.append(f"  <li>{_inline_format(stripped[2:].strip())}</li>")
      continue

    close_list()
    para_buf.append(stripped)

  flush_para()
  close_list()
  return "\n".join(out)


def render_markdown(md_text: str) -> str:
  """Converts Markdown text to HTML using python-markdown if available, or fallback parser."""
  try:
    import markdown  # type: ignore

    return markdown.markdown(
        md_text,
        extensions=["fenced_code", "tables", "sane_lists", "smarty"],
        output_format="html",
    )
  except ImportError:
    return _fallback_markdown_to_html(md_text)


def load_post(md_path: Path) -> BlogPost:
  raw = md_path.read_text(encoding="utf-8")
  meta, body_md = parse_frontmatter(raw)

  slug = meta.get("slug", md_path.stem)
  title = meta.get("title", slug.replace("_", " ").replace("-", " ").title())
  date_str = meta.get("date", date.today().isoformat())
  try:
    pub_date = datetime.strptime(date_str, "%Y-%m-%d").date()
  except ValueError:
    pub_date = date.today()

  category = meta.get("category", "Engineering")
  author = meta.get("author", "frs")
  summary = meta.get("summary", "")
  direction = meta.get("dir", "ltr").lower()
  draft = meta.get("draft", "false").lower() in ("true", "yes", "1")

  body_html = render_markdown(body_md)
  if not summary:
    plain = re.sub(r"<[^>]+>", "", body_html).strip()
    summary = (plain[:180] + "...") if len(plain) > 180 else plain

  return BlogPost(
      slug=slug,
      title=title,
      pub_date=pub_date,
      category=category,
      author=author,
      summary=summary,
      direction=direction,
      draft=draft,
      body_html=body_html,
      source_path=md_path,
  )


def render_post_page(post: BlogPost) -> str:
  nav_html = build_nav_html("/blog/index.html")
  sidebar_html = build_sidebar_html(include_status=False)
  dir_attr = ' dir="rtl"' if post.direction == "rtl" else ""
  arabic_cls = " arabic-modern" if post.direction == "rtl" else ""

  indented_body = "\n".join(
      f"              {line}" if line.strip() else ""
      for line in post.body_html.splitlines()
  )

  return f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="description" content="{html.escape(post.summary, quote=True)}" />
    <title>{html.escape(post.title)} - Notes | المدونة</title>
    <link rel="stylesheet" href="/assets/style.css">
    <link rel="icon" href="/favicon.ico" sizes="32x32">
  </head>
  <body>
    <div class="academic-container">
{HEADER_HTML}
      
{nav_html}

      <div class="academic-layout">
{sidebar_html}

        <main class="academic-main">
          <article{dir_attr}>
            <div class="post-meta">
              Published: {post.formatted_date} &bull; Category: {html.escape(post.category)}
            </div>
            <h2>{html.escape(post.title)}</h2>
            
            <div class="post-body{arabic_cls}"{dir_attr}>
{indented_body}
            </div>
          </article>
          
          <div class="page-footer-nav">
            <a href="/blog/index.html" class="back-link">&laquo; Back to Blog Index</a>
            <a href="/index.html" class="back-link">&laquo; Home</a>
          </div>
        </main>
      </div>

{FOOTER_HTML}
    </div>
  </body>
</html>
"""


def render_blog_index(posts: list[BlogPost]) -> str:
  nav_html = build_nav_html("/blog/index.html")
  sidebar_html = build_sidebar_html(include_status=False)

  items_html: list[str] = []
  for post in posts:
    dir_attr = ' dir="rtl"' if post.direction == "rtl" else ""
    arabic_cls = ' class="arabic-modern"' if post.direction == "rtl" else ""
    items_html.append(f"""            <li class="blog-list-item"{dir_attr}>
              <div class="post-meta">
                {post.formatted_date} &mdash; Written by {html.escape(post.author)} &bull; {html.escape(post.category)}
              </div>
              <h3{arabic_cls}>
                <a href="/blog/{post.slug}.html">{html.escape(post.title)}</a>
              </h3>
              <p{arabic_cls}>
                {html.escape(post.summary)}
              </p>
            </li>""")

  list_block = "\n".join(items_html)

  return f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="description" content="Blog posts by Feras Aldahlawi (frs)." />
    <title>Feras's Blog - Notes | المدونة</title>
    <link rel="stylesheet" href="/assets/style.css">
    <link rel="icon" href="/favicon.ico" sizes="32x32">
  </head>
  <body>
    <div class="academic-container">
{HEADER_HTML}
      
{nav_html}

      <div class="academic-layout">
{sidebar_html}

        <main class="academic-main">
          <h2>Technical Blog & Notes</h2>
          <p>
            A collection of engineering articles, notes, and thoughts on media player software, content protection systems, and cryptography.
          </p>

          <ul class="blog-list">
{list_block}
          </ul>
          
          <div class="page-footer-nav">
            <a href="/index.html" class="back-link">&laquo; Back to Home</a>
          </div>
        </main>
      </div>

{FOOTER_HTML}
    </div>
  </body>
</html>
"""


def create_new_post(slug: str, title: str | None = None) -> int:
  POSTS_DIR.mkdir(parents=True, exist_ok=True)
  clean_slug = re.sub(r"[^a-zA-Z0-9_-]", "_", slug.removesuffix(".md"))
  target = POSTS_DIR / f"{clean_slug}.md"
  if target.exists():
    print(f"Error: {target.relative_to(ROOT)} already exists.", file=sys.stderr)
    return 1

  post_title = title or clean_slug.replace("_", " ").replace("-", " ").title()
  today_str = date.today().isoformat()
  template = f"""---
title: "{post_title}"
date: {today_str}
category: Engineering
author: frs
summary: "Brief 1-2 sentence summary shown on the blog index page."
dir: ltr
draft: false
---

Write your post in **Markdown** here.

## Section Heading

- Bullet point 1
- Bullet point 2

```cpp
// Code snippet example
int main() {{
  return 0;
}}
```
"""
  target.write_text(template, encoding="utf-8")
  print(f"Created new Markdown post: {target.relative_to(ROOT)}")
  print("Run `python3 scripts/build_blog.py` when ready to publish.")
  return 0


def build_all(check_only: bool = False) -> tuple[bool, list[Path]]:
  POSTS_DIR.mkdir(parents=True, exist_ok=True)
  md_files = sorted(POSTS_DIR.glob("*.md"))
  posts = [load_post(p) for p in md_files]
  published_posts = [p for p in posts if not p.draft]
  published_posts.sort(key=lambda p: (p.pub_date, p.slug), reverse=True)

  changed_files: list[Path] = []

  for post in published_posts:
    rendered = render_post_page(post)
    out_path = post.output_path
    existing = out_path.read_text(encoding="utf-8") if out_path.exists() else ""
    if rendered != existing:
      changed_files.append(out_path.relative_to(ROOT))
      if not check_only:
        out_path.write_text(rendered, encoding="utf-8")

  index_path = BLOG_DIR / "index.html"
  rendered_index = render_blog_index(published_posts)
  existing_index = (
      index_path.read_text(encoding="utf-8") if index_path.exists() else ""
  )
  if rendered_index != existing_index:
    changed_files.append(index_path.relative_to(ROOT))
    if not check_only:
      index_path.write_text(rendered_index, encoding="utf-8")

  return bool(changed_files), changed_files


def main() -> int:
  args = sys.argv[1:]
  if "--new" in args:
    idx = args.index("--new")
    if idx + 1 >= len(args):
      print(
          'Usage: python3 scripts/build_blog.py --new <slug> ["Post Title"]',
          file=sys.stderr,
      )
      return 1
    slug = args[idx + 1]
    title = args[idx + 2] if idx + 2 < len(args) else None
    return create_new_post(slug, title)

  check_only = "--check" in args
  has_changes, changed = build_all(check_only=check_only)
  if check_only and has_changes:
    print(
        "Blog HTML out of sync with Markdown sources:",
        ", ".join(str(p) for p in changed),
    )
    return 1
  if has_changes:
    print("Built blog HTML:", ", ".join(str(p) for p in changed))
  else:
    print("All blog HTML files are up-to-date with blog/posts/*.md.")
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
