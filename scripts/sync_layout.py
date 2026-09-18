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

HEADER_HTML = """      <header class="academic-header">
        <div class="header-title-row">
          <h1>Feras Aldahlawi</h1>
          <span class="arabic">فراس الدهلوي</span>
        </div>
        <p class="header-subtitle">Software Engineer</p>
      </header>"""

FOOTER_HTML = """      <footer class="academic-footer">
        <p>Made in Seattle &copy; 2026</p>
      </footer>"""


def build_nav_html(active_href: str) -> str:
  links = []
  for href, label in NAV_ITEMS:
    cls = ' class="active"' if href == active_href else ""
    links.append(f'        <a href="{href}"{cls}>{label}</a>')
  return (
      '      <nav class="academic-nav">\n' + "\n".join(links) + "\n      </nav>"
  )


def build_sidebar_html(include_status: bool = False) -> str:
  status_block = ""
  if include_status:
    status_block = """

          <div class="sidebar-section">
            <h3>Page Status</h3>
            <p><span class="blink status-badge">[UNDER CONSTRUCTION]</span></p>
            <p class="arabic-modern" dir="rtl"><span class="blink status-badge">[تحت الإنشاء]</span></p>
          </div>"""
  return f"""        <aside class="academic-sidebar">
          <div class="sidebar-section">
            <h3>Contact</h3>
            <p>Email: <a href="mailto:frs@chromium.org">frs@chromium.org</a></p>
            <div class="sidebar-cta">
              <a href="https://calendar.app.google/Po5uBfEutynhExWj8" target="_blank" class="btn-academic">Schedule Meeting</a>
            </div>
          </div>{status_block}
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
      r"[ \t]*<header class=\"academic-header\">.*?</header>",
      HEADER_HTML,
      updated,
      flags=re.DOTALL,
  )
  updated = re.sub(
      r"[ \t]*<nav class=\"academic-nav\">.*?</nav>",
      build_nav_html(active_href),
      updated,
      flags=re.DOTALL,
  )
  updated = re.sub(
      r"[ \t]*<aside class=\"academic-sidebar\">.*?</aside>",
      build_sidebar_html(include_status=is_home),
      updated,
      flags=re.DOTALL,
  )
  updated = re.sub(
      r"[ \t]*<footer class=\"academic-footer\">.*?</footer>",
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
