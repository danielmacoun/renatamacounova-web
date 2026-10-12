# Repository Guidelines

## Production Safety & Approval

- Preserve the website's current visual style, including typography, colors, spacing, and component appearance.
- Make routine requested content changes directly: text, prices, services, contact details, and opening hours.
- Before major changes to structure, design, or technical architecture, propose a concrete solution and wait for explicit approval before implementing it.
- Never modify other repositories or files outside this project. Keep all edits and generated files within the project directory.
- If a change could break production, prefer a safer implementation or a pull request for review before deployment. Do not deploy unverified changes.
- Prefer simple, robust solutions that a nontechnical user can maintain. Avoid unnecessary dependencies and tooling.

## Project Structure & Module Organization

This is a Czech-language static website for Renata Macounová. This directory (`site/` in the parent workspace) is both the Git repository root and the published web root. Paths below are relative to this directory.

- `index.html`: homepage and service overview.
- `kouc-detskych-srdci/` and `pet-tibetanu/`: service pages.
- `zamysleni/`: reading overview and individual excerpts, each in `<slug>/index.html`.
- `assets/`: shared CSS, vanilla JavaScript, and published images.
- `CNAME` and `sitemap.xml`: domain configuration and indexed URLs.

Social-post files in `../instagram/` and root-level HTML variants in the parent workspace are outside this Git repository; do not include them in website changes.

See `README.md` for the excerpt workflow.

## Build, Test, and Development Commands

Run from the repository root:

```sh
python3 -m http.server 8000 --bind 127.0.0.1 --directory .
```

Open `http://localhost:8000/`. Serving this directory as the root is necessary for root-relative links and the latest-excerpt fetch. No dependency installation, local build command, package scripts, or configured lint commands are present. GitHub Pages performs a Jekyll build and deployment after changes reach its publishing branch; never push or publish without authorization.

## Coding Style & Naming Conventions

Preserve UTF-8 Czech text and `lang="cs"`. Use lowercase, hyphen-separated, accent-free directory and asset names, such as `chybovani-je-dobra-zkusenost`.

Match surrounding formatting: two-space indentation for JavaScript and nested HTML where used; shared CSS uses compact one-rule-per-line formatting. JavaScript uses `const`, single-quoted strings, and semicolons. Reuse existing `reading-*` classes and CSS variables. Keep unrelated formatting changes out of patches; no formatter is configured.

## Testing Guidelines

After every change, verify the build and basic website functionality. Currently there is no local build step: report it as not applicable and check the static site through the local HTTP server instead. When publication is authorized, also verify the GitHub Pages build and deployment result. If a build is introduced later, run it after every change. Record checks performed and any limitations; never claim an unperformed check passed.

No automated test framework or coverage threshold is configured. Manually check changed pages at desktop and mobile widths, navigation, images, keyboard focus, and browser-console errors. Verify the homepage latest-excerpt link with JavaScript enabled and its static fallback with JavaScript disabled.

## Content Updates

For new excerpts, follow `README.md`: update page metadata and JSON-LD, retain the book association, place the newest overview card first, add the sitemap URL, and update related-excerpt navigation. Keep publication dates consistent across visible text and metadata.

## Commit & Pull Request Guidelines

Git history uses concise English imperative subjects, such as `Update SEO metadata and online tutoring copy`. Follow that convention. In pull requests, describe affected pages, link relevant issues, list manual checks, and include desktop/mobile screenshots for visual changes.
