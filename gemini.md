# Gemini / Antigravity Engineering & Governance Guidelines

This document defines the strict, binding operational mandates for all development, versioning, deployment, and release processes across all projects in this workspace.

---

## 1. Core Principles & Philosophy

1. **Independent Project Integrity:** Every project in this workspace is an autonomous production application with its own repository, assets, dependencies, and deployment lifecycle.
2. **Immutable Versioning:** Every project maintains an immutable, append-only version ledger (`version.md`).
3. **Continuous Production Deployments:** Every web project must produce and maintain a working GitHub Pages site. Deployment bugs, asset 404s, and execution errors must be diagnosed and resolved until 100% operational.
4. **Hardened Production Applications:** Any mobile application (Android or iOS) must ALWAYS be signed with production keys and delivered as a release-grade build.
5. **Cryptographic Provenance:** Every Git commit must be cryptographically signed with the user's SSH signing key so that GitHub displays the verified commit badge.

---

## 2. Mandate 1: Strict Append-Only `version.md` Protocol

### 2.1 The Ledger Rule
Every project directory **MUST** contain a `version.md` file at its root.
- **STRUCTURE RULE:** `version.md` uses an **APPEND-ONLY** structure.
- **IMMUTABILITY RULE:** Existing entries in `version.md` must **NEVER** be deleted, edited, truncated, or rewritten under any circumstances.
- **ADDITION RULE:** New releases, features, patches, and changes are exclusively added by appending to the end of the file.

### 2.2 Tooling & Execution Rule
When interacting with `version.md`:
- Agents and scripts must ONLY perform append operations:
  - In tool calls: `write_to_file` with `Append: true` (or shell `>>`).
  - `replace_file_content` or `write_to_file` with `Overwrite: true` is strictly prohibited on `version.md`.

### 2.3 Required Entry Schema
Each appended version entry must adhere to this structured format:

```markdown
## [vX.Y.Z] - YYYY-MM-DD
- **Commit:** <commit-sha> (Signed)
- **Author:** saltymother <saltymother@users.noreply.github.com>
- **Type:** Feature | Bugfix | Refactor | Deployment | Release
- **Status:** Deployed & Verified
- **GitHub Pages:** https://saltymother.github.io/<repo-name>/
- **Summary:**
  - Brief description of change 1
  - Brief description of change 2
  - Resolution of any layout/runtime issues
```

---

## 3. Mandate 2: GitHub Pages Production & Continuous Resolution

### 3.1 Uncompromising Quality Standard
- Every web application must have an active, functional GitHub Pages deployment.
- "Keep fixing them till they work properly": If a page fails to deploy, renders a blank screen, throws JavaScript exceptions, or fails to load assets, the agent must inspect, debug, and fix the code until the deployment succeeds and the page functions without errors.

### 3.2 Asset Pathing & Routing
- **Relative Paths Only:** Never use absolute paths (e.g., `/style.css`, `/assets/logo.png`) because GitHub Pages sites are served under a subpath (`https://<username>.github.io/<repo-name>/`).
  - Correct: `./style.css`, `styles.css`, `assets/model.glb`, `./js/app.js`
  - Incorrect: `/style.css`, `/assets/model.glb`
- **Jekyll Bypassing:** Every repository must contain an empty `.nojekyll` file in the root to ensure GitHub Pages does not ignore folders or assets starting with underscores or containing 3D/WASM assets.

### 3.3 Automated CI/CD Deployments
Every repository must include `.github/workflows/deploy.yml` with modern GitHub Pages deployment actions:

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: ["main"]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      - name: Setup Pages
        uses: actions/configure-pages@v4
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: '.'
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

### 3.4 Fallback Branch Support
Maintain a synchronized `gh-pages` branch alongside `main` to support legacy or alternative hosting configurations.

---

## 4. Mandate 3: Mobile Apps (Android & iOS) Production Signing

Whenever an application is built for Android or iOS:

### 4.1 Android Production Standards
1. **Production Signing Only:**
   - Unsigned APKs and debug-keystore APKs are strictly prohibited for production delivery.
   - Applications must be signed using a production release keystore via Gradle or `apksigner`:
     ```bash
     apksigner sign --ks release-keystore.jks --ks-key-alias <alias> --out app-release-signed.apk app-release-unsigned.apk
     ```
2. **Production Artifacts:**
   - Generate production release builds:
     - Android App Bundle (AAB): `./gradlew bundleRelease` (for Google Play Console distribution).
     - Signed Release APK: `./gradlew assembleRelease` (for standalone/direct distribution).
3. **Verification:**
   - Validate alignment: `zipalign -c -v 4 app-release-signed.apk`
   - Validate signature: `apksigner verify --verbose app-release-signed.apk`

### 4.2 iOS Production Standards
1. **Production Code Signing:**
   - Unsigned apps or ad-hoc test builds are strictly prohibited for production releases.
   - Must be signed with a production Apple Distribution Certificate and matched with an App Store or Ad-Hoc Provisioning Profile.
2. **Production Artifacts:**
   - Archive build: `xcodebuild -workspace <App>.xcworkspace -scheme <App> -configuration Release archive -archivePath build/<App>.xcarchive`
   - Export production IPA: `xcodebuild -exportArchive -archivePath build/<App>.xcarchive -exportPath build/out -exportOptionsPlist exportOptions.plist`
3. **Verification:**
   - Validate signature: `codesign -dvv --deep build/out/<App>.ipa`

### 4.3 macOS App Bundles
- Any `.app` bundle must be properly signed with hardened runtime:
  ```bash
  codesign --force --options runtime --deep --sign "<Signing Identity>" AppName.app
  ```

---

## 5. Mandate 4: Cryptographically Verified Commits on GitHub

### 5.1 Verified Badge Requirement
Every commit pushed to GitHub must display GitHub's green **"Verified"** badge. Unsigned commits are strictly unacceptable.

### 5.2 Git SSH Signing Configuration
Git 2.34+ SSH commit signing is enforced globally across all repositories:
```bash
git config --global user.name "saltymother"
git config --global user.email "saltymother@users.noreply.github.com"
git config --global gpg.format ssh
git config --global user.signingkey ~/.ssh/id_ed25519_github.pub
git config --global commit.gpgsign true
git config --global gpg.ssh.allowedSignersFile ~/.ssh/allowed_signers
git config --global init.defaultBranch main
```

### 5.3 Allowed Signers Configuration
Ensure `~/.ssh/allowed_signers` contains the public key for local verification:
```
saltymother@users.noreply.github.com namespaces="git" ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAICAdmjS5LMIzfzSONhLdua3W7UZUOql8+cdBVeHb1IOx saltymother@users.noreply.github.com
```

### 5.4 GitHub Key Registration
For the "Verified" badge to show on GitHub:
- The SSH public key (`~/.ssh/id_ed25519_github.pub`) must be registered in GitHub account settings as a **Signing Key** (Settings > SSH and GPG keys > New SSH key > Key type: "Signing Key").

---

## 6. Repository & Project Directory Registry

| Project Directory | Repository Name | Live GitHub Pages URL |
| :--- | :--- | :--- |
| `physics_wonderland/` | `physics-wonderland` | https://saltymother.github.io/physics-wonderland/ |
| `mouse_the_tunnel_maze/` | `mouse-the-tunnel-maze` | https://saltymother.github.io/mouse-the-tunnel-maze/ |
| `penguin_beyond_the_door/` | `penguin-beyond-the-door` | https://saltymother.github.io/penguin-beyond-the-door/ |
| `tortoise_hare_3d/` | `tortoise-and-hare-3d` | https://saltymother.github.io/tortoise-and-hare-3d/ |
| `men_health_looksmaxxing/` | `men-health-looksmaxxing` | https://saltymother.github.io/men-health-looksmaxxing/ |
| `history_chronicles/` | `chronicles-of-bharatavarsha` | https://saltymother.github.io/chronicles-of-bharatavarsha/ |
| `shinigami_the_golden_pot/` | `shinigami-the-golden-pot` | https://saltymother.github.io/shinigami-the-golden-pot/ |
| `vietnam_cinematic/` | `vietnam-cinematic` | https://saltymother.github.io/vietnam-cinematic/ |
| `the_world_explained/` | `the-world-explained` | https://saltymother.github.io/the-world-explained/ |
| `global_arbitrage_nri/` | `global-arbitrage-nri` | https://saltymother.github.io/global-arbitrage-nri/ |
| `drongo_wildlife/` | `drongo-wildlife` | https://saltymother.github.io/drongo-wildlife/ |
| Root (`/`) | `scientific-calculator` | https://saltymother.github.io/scientific-calculator/ |

---

## 7. Change Execution Checklist

For any modification or addition to a project:
1. [ ] Implement code changes ensuring relative paths and web compliance.
2. [ ] Test locally (e.g. via `python3 server.py` or browser inspection).
3. [ ] Append new version entry to `version.md` (**strictly append-only**).
4. [ ] Verify `.nojekyll` and `.github/workflows/deploy.yml` exist.
5. [ ] Stage and commit with cryptographic signing (`git commit -S -m "..."`).
6. [ ] Verify commit signature with `git log --show-signature -n 1`.
7. [ ] Push to GitHub (`git push -u origin main` and `git push -u origin gh-pages`).
8. [ ] Validate that GitHub Actions workflow triggers, completes, and the live GitHub Pages site returns HTTP 200.
