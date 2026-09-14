# Zain Ul Abideen portfolio

A responsive, editable portfolio site focused on Computer Science, AI automation, and SEO systems.

## Run locally

From this directory:

```bash
python3 -m http.server 4173 --bind 0.0.0.0
```

Then open the live preview or visit `http://localhost:4173` locally.

## Test before deployment

```bash
python audit.py
node --check script.js
```

The audit checks local assets, links, section anchors, real-data placeholders, responsive hooks, navigation order, and the live deployment smoke test.

## Edit content

- Main copy and sections: `index.html`
- Colors, typography, layout, and responsive behavior: `styles.css`
- Mobile navigation and header behavior: `script.js`
- Local fonts and approved portrait assets: `assets/`
