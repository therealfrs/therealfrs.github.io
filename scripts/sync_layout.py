#!/usr/bin/env python3
"""Synchronizes the shared layout shell (header, nav, sidebar, footer) across all HTML pages.

Usage:
  python3 scripts/sync_layout.py          # Update all HTML files in-place
  python3 scripts/sync_layout.py --check  # Verify all HTML files match the
  canonical layout
"""

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent

NAV_ITEMS = [
    ("/index.html", "Home"),
    ("/about.html", "About"),
    ("/resume.html", "Resume"),
    ("/podcast.html", "Podcasts"),
    ("/user_manual.html", "User Manual"),
    ("/blog/index.html", "Blog"),
]

NAV_ICONS = {
    "/index.html": "⌂",
    "/about.html": "👤",
    "/resume.html": "📄",
    "/podcast.html": "🎙️",
    "/user_manual.html": "📋",
    "/blog/index.html": "📝",
}

HEADER_HTML = """      <header class="academic-header portal-header">
        <div class="header-main">
          <div class="header-branding">
            <h1 class="portal-title">FERAS ALDAHLAWI</h1>
          </div>
        </div>
      </header>"""

FOOTER_HTML = """      <footer class="academic-footer portal-footer">
        <div class="footer-nav-row">
          <a href="/index.html">Home</a> &bull;
          <a href="/about.html">About</a> &bull;
          <a href="/resume.html">Resume</a> &bull;
          <a href="/podcast.html">Podcasts</a> &bull;
          <a href="/user_manual.html">User Manual</a> &bull;
          <a href="/blog/index.html">Blog</a> &bull;
          <a href="#top">Top of Page &uarr;</a>
        </div>
        <p class="footer-copy">
          Copyright &copy; 2026 Feras Aldahlawi &bull; Made in Seattle
        </p>
      </footer>"""


def build_nav_html(active_href: str) -> str:
  links = []
  for href, label in NAV_ITEMS:
    cls = ' class="active"' if href == active_href else ""
    icon = NAV_ICONS.get(href, "▸")
    links.append(f'        <a href="{href}"{cls}>{icon} {label}</a>')
  return (
      '      <nav class="academic-nav portal-nav">\n'
      + "\n".join(links)
      + "\n      </nav>"
  )


def build_sidebar_html(include_status: bool = False) -> str:
  return """        <aside class="academic-sidebar portal-sidebar">
          <div class="sidebar-box">
            <div class="sidebar-box-header">■ WEBMASTER</div>
            <div class="sidebar-box-body">
              <div class="webmaster-card">
                <div class="webmaster-avatar">frs</div>
                <div class="webmaster-details">
                  <div class="wm-row"><span class="wm-key">Handle:</span> <span class="wm-val">frs</span></div>
                  <div class="wm-row"><span class="wm-key">Role:</span> <span class="wm-val">Software Eng</span></div>
                  <div class="wm-row"><span class="wm-key">Org:</span> <span class="wm-val">Google Chrome</span></div>
                  <div class="wm-row"><span class="wm-key">Email:</span> <a href="mailto:frs@chromium.org" class="wm-link">frs@chromium.org</a></div>
                </div>
              </div>
              <div class="sidebar-cta">
                <a href="https://calendar.app.google/Po5uBfEutynhExWj8" target="_blank" class="btn-academic btn-portal">Schedule Meeting</a>
              </div>
            </div>
          </div>

          <div class="sidebar-box">
            <div class="sidebar-box-header">■ QUICK LINKS</div>
            <div class="sidebar-box-body">
              <ul class="channel-list">
                <li><a href="/index.html">&raquo; Portal Home</a></li>
                <li><a href="/about.html">&raquo; Bio &amp; Career</a></li>
                <li><a href="/resume.html">&raquo; Curriculum Vitae</a></li>
                <li><a href="/podcast.html">&raquo; Podcast Audio</a></li>
                <li><a href="/user_manual.html">&raquo; Collaboration Manual</a></li>
                <li><a href="/blog/index.html">&raquo; Tech Blog &amp; Notes</a></li>
                <li><a href="/engineering_blogs.opml" download>&raquo; OPML RSS Feeds</a></li>
              </ul>
            </div>
          </div>
        </aside>"""


def active_href_for_page(rel_path: Path) -> str:
  if rel_path.parts[0] == "blog":
    return "/blog/index.html"
  return f"/{rel_path.name}"


def sync_file(file_path: Path, check_only: bool = False) -> bool:
  rel_path = file_path.relative_to(ROOT)
  original = file_path.read_text(encoding="utf-8")
  updated = original

  active_href = active_href_for_page(rel_path)
  is_home = rel_path == Path("index.html")

  updated = re.sub(
      r"[ \t]*<header class=\"academic-header.*?\">.*?</header>",
      HEADER_HTML,
      updated,
      flags=re.DOTALL,
  )
  updated = re.sub(
      r"[ \t]*<nav class=\"academic-nav.*?\">.*?</nav>",
      build_nav_html(active_href),
      updated,
      flags=re.DOTALL,
  )
  updated = re.sub(
      r"[ \t]*<aside class=\"academic-sidebar.*?\">.*?</aside>",
      build_sidebar_html(include_status=is_home),
      updated,
      flags=re.DOTALL,
  )
  updated = re.sub(
      r"[ \t]*<footer class=\"academic-footer.*?\">.*?</footer>",
      FOOTER_HTML,
      updated,
      flags=re.DOTALL,
  )

  if updated != original:
    if not check_only:
      file_path.write_text(updated, encoding="utf-8")
    return True
  return False


def main() -> int:
  check_only = "--check" in sys.argv[1:]
  pages = sorted(ROOT.glob("*.html")) + sorted((ROOT / "blog").glob("*.html"))
  changed = []

  for page in pages:
    if sync_file(page, check_only=check_only):
      changed.append(page.relative_to(ROOT))

  if check_only and changed:
    print("Layout out of sync in:", ", ".join(str(p) for p in changed))
    return 1
  if changed:
    print("Updated layout in:", ", ".join(str(p) for p in changed))
  else:
    print("All pages are in sync with the canonical layout.")
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
