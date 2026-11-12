# Interactive Personal Site (Ruitao Feng)

Single-file academic homepage with an on-page guide, Barron-style publication list and one-click CV.

## Deploy on GitHub Pages
1. Create a repo named `<your-github-username>.github.io`.
2. Put `index.html`, `README.md` and the `papers/` folder in the repo root and push.
3. Settings → Pages → Source: `main` branch, `/ (root)`.
4. See `PAPERS_TODO.md` for the PDFs to place in `papers/`.

## Guide box
- Answers are in English; visitors can type questions in English or Chinese.
- Layer 1, intents: pre-written answers for full questions (keywords + character n-gram similarity to example questions). Intents for every paper, venue, year, unit and service area are generated from the page data automatically.
- Layer 2, page search: [MiniSearch](https://github.com/lucaong/minisearch) v7.2.0 (MIT, inlined) indexes every paper, research direction, unit, service item, contact row and "Work with me" card. Short keyword queries ("security paper", "fuzzing", "cloud") return the matching items with links. Typos and partial words work (prefix + fuzzy).
- If nothing on the page matches, the guide says so and points to email.
- To improve routing, add keywords (`kw`) or example questions (`ex`) to an intent. New papers, units and service items are searchable automatically.

## Security
- Links re-checked at render time: anchors must match `#[a-z0-9-]+`; external links must be `https:` and in `ALLOWED_HOSTS`.
- Input capped at 160 chars, Unicode-normalised, tags and control/bidi characters stripped, rendered via `textContent` only.
- CSP: inline scripts only, no network connections, no workers.

## Editing
- Publications: `P` array (`fig` for a real thumbnail, `rk` to override the rank badge).
- Teaching: `TEACH`. CV text: `CV`.
- Avatar is embedded as a data URI; the source image is `avatar-sketch.jpg`.

## CI/CD
- `.github/workflows/deploy.yml` runs on every push to `main` (and on pull requests, check only).
- Step 1 `tools/check_site.py`: page parses, all sections and guide anchors exist, every linked PDF is present in `papers/`, paper keys are unique.
- Step 2 deploys to GitHub Pages (Settings → Pages → Source: **GitHub Actions**).
- Custom domain: put the domain in a file named `CNAME` at the repo root (one line, e.g. `www.example.com`), add the DNS record at your registrar, then set the same domain in Settings → Pages.

## License
- Code (HTML, CSS, JavaScript, `tools/`, workflow): MIT License, see `LICENSE`.
- Third-party: MiniSearch v7.2.0, (c) Luca Ongaro, MIT License, inlined in `index.html` with its notice.
- Not covered by the MIT License: the papers in `papers/` (copyright remains with the authors and publishers under their own terms), the portrait in `assets/` and the written content of the page. Please do not reuse them without permission.
