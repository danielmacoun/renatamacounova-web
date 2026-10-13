# Website checks

Every pull request targeting `main` runs the required `Website checks` job.
It validates HTML parsing, IDs, Czech language, titles, descriptions, canonical
and Open Graph metadata, JSON-LD, internal links and anchors, image files and the
sitemap. Chromium smoke checks cover all pages at 390px and 1280px, image loading,
horizontal overflow, JavaScript errors and the latest-excerpt fallback.

These are functional checks, not a visual redesign detector. Review screenshots
for layout changes. External services are excluded from the browser checks to
avoid outages elsewhere blocking publication; fonts use browser fallbacks.

Run locally from the repository root in an isolated Python 3.10+ environment:

```sh
python -m pip install -r .github/checks/requirements.txt
python .github/checks/check_site.py
python -m playwright install chromium
python .github/checks/check_browser.py
```

The workflow uses `pull_request`, a read-only token, no secrets and no publishing
steps. GitHub Pages deployment remains unchanged. Merge only after the checks
succeed and the owner authorizes publication, then verify Pages and the live site.
For rollback, use a revert pull request; never rewrite production history.

Keep `main` protected with pull requests required, zero required approvals for the
single maintainer, no admin bypass, no force pushes or deletions, and the
`Website checks` status required. An external assistant should get access only to
this repository and must not receive administration or protection-bypass rights.
