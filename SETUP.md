# Publishing the map on GitHub Pages

You have two files: `index.html` (the map) and `README.md`. GitHub Pages will serve `index.html` as a live website for free. Here are two ways to do it — pick one.

---

## Option A — All in the browser (no software to install, easiest)

### 1. Create the repository
1. Sign in at [github.com](https://github.com).
2. Click the **+** (top-right) → **New repository**.
3. Name it `2060-settlement-atlas` (or anything you like).
4. Set it to **Public** (Pages needs Public on the free tier).
5. **Don't** check "Add a README" (you already have one).
6. Click **Create repository**.

### 2. Upload the files
1. On the new repo page, click **uploading an existing file** (the link in the "Quick setup" box).
2. Drag `index.html` and `README.md` into the browser window.
3. Scroll down, click **Commit changes**.

### 3. Turn on Pages
1. In the repo, click **Settings** (top menu).
2. Left sidebar → **Pages**.
3. Under **Source**, choose **Deploy from a branch**.
4. Branch: **main**, folder: **/ (root)**. Click **Save**.
5. Wait ~1 minute, then refresh. A green banner shows your URL:
   `https://YOURUSERNAME.github.io/2060-settlement-atlas/`
6. Open it. That's your live map — share the link with anyone.

### 4. (Optional) fix the README link
Edit `README.md` in the repo and replace `YOURUSERNAME` in the "Open the live map" line with your actual username, so the link works for visitors.

---

## Option B — Replacing your old v70 map

If you want to **reuse the existing repo** from the v70 days instead of making a new one:

1. Go to that old repository on GitHub.
2. Click on the old map file (e.g. the old `index.html` or whatever it was named).
3. Click the **pencil (Edit)** icon → select all → delete → paste the new `index.html` contents.
   *Or* delete the old file and upload the new one via **Add file → Upload files**.
4. Commit. If Pages was already enabled there, the new map replaces the old at the same URL within a minute.

**Fresh vs. replace:** a fresh repo is cleaner (the project has changed enormously since v70) and gives you a tidy URL. Replacing keeps the old link alive for anyone who bookmarked it. If in doubt, start fresh — you can always delete the old repo later.

---

## Updating the map later

Whenever there's a new version of the map:
1. Go to your repo → click `index.html` → **pencil (Edit)**.
2. Select-all, delete, paste the new file's contents, **Commit**.
3. The live site updates in about a minute (you may need to hard-refresh: Ctrl/Cmd-Shift-R).

Or use **Add file → Upload files** and overwrite.

---

## Troubleshooting

- **Blank page / 404:** Pages can take 1–2 minutes on first publish. Refresh. Confirm the file is named exactly `index.html` (lowercase).
- **Map loads but looks empty:** it needs internet for the D3 library (loaded from a CDN). On a normal connection it's fine.
- **Legend/toggles not showing:** hard-refresh (Ctrl/Cmd-Shift-R) to clear a cached old version.
- **Want it private?** GitHub Pages on free accounts requires a public repo. For a private option, tools like Netlify Drop (drag-and-drop, no account needed) also work — happy to give instructions if you'd prefer that.

---

That's it. Once it's up, the URL is permanent and you can share it with friends — they just click and explore, nothing to install.
