# Decap CMS integration

This folder contains content managed by Decap CMS on the isolated `decap-cms-integration` branch.

## CMS collections

- Homepage: `cms/homepage.json` — homepage SEO, hero copy, headline, button, portrait and About copy.
- Global Website Settings: `cms/global-settings.json` — brand image/name, navigation, footer links, contact/social URLs and design tokens.
- Services: `cms/services/*.json` — the four existing service pages, including SEO fields and structured page sections.
- Portfolio Projects: `cms/projects/*.json` — project entries; the build step can generate a project detail page for each entry.
- Website Pages: `cms/pages/*.json` — create new static pages using the section builder.

## Publishing/build behavior

The Netlify build command is configured in `netlify.toml` and runs `python3 scripts/build.py`. The script uses only the Python standard library. It updates homepage SEO metadata, applies CMS service-page edits while retaining each existing page shell, creates static pages for new CMS entries, and adds their URLs to `sitemap.xml`.

The browser loader `cms-loader.js` applies editable homepage copy and global design/navigation/footer/contact settings. Existing HTML remains the fallback if JavaScript or CMS JSON is unavailable.

## Important limitations before production

- The homepage's non-hero sections and existing project-card grid are not yet fully CMS-driven.
- Generated pages use a separate responsive template; check their appearance on desktop and mobile before publishing.
- Test the Netlify branch deploy and Decap save/publish workflow before merging.
- Do not merge this integration branch into `main` until SEO metadata, canonical URLs, sitemap output, image paths and navigation have been checked.

## Safety

The CMS backend writes only to `decap-cms-integration`. Never put OAuth client secrets in this repository. The separate Pages CMS draft PR is not part of this integration.
