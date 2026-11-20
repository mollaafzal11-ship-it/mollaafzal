# Decap CMS integration (test branch)

This folder contains the Decap CMS admin application and configuration for the separate `decap-cms-integration` branch.

## Current scope

- The CMS backend targets this branch only. It does not write to `main`.
- Homepage content is stored in `cms/homepage.json`.
- Service, project, and page entries are stored as Markdown under their corresponding `cms/` folders.
- Uploaded media is stored under `portfolio_assets/`.

## Important publishing note

This portfolio is a static HTML site rather than a site generated from the CMS content folders. The CMS can edit and commit these content files, but the public HTML pages do not automatically consume those files yet. Do not treat an edited CMS entry as published website content until the front-end rendering integration has been completed and verified. Existing HTML pages are intentionally left untouched during this initial CMS setup.

## Authentication

The GitHub backend requires an OAuth authentication provider. Configure GitHub OAuth in the Netlify site settings using Netlify's documented OAuth callback before attempting to sign in. Never put an OAuth client secret in this repository.

## Safety

Test edits only on this branch. Do not merge into `main` until authentication, preview, content rendering, image paths, and SEO output have all been verified.
