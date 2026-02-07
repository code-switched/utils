# Renaming a Git Repository Locally and on GitHub

A step-by-step guide for renaming your repository both on GitHub and updating your local git configuration.

---

## Overview

When renaming a repository, you may need to:
1. **Rename on GitHub** (via web interface)
2. **Transfer to an organization** (optional, if moving from personal to org)
3. **Update local git remote** (update the URL your local repo points to)
4. **Update project files** (like `pyproject.toml`, `package.json`, etc.)

**Best Practice:** If you're both renaming AND transferring to an organization, do both on GitHub first, then update your local remote URL once to the final destination.

---

## Step 1: Rename on GitHub

### Option A: Rename Only
1. Go to your repository on GitHub
2. Click **Settings** → **General**
3. Scroll to the **Repository name** section
4. Enter the new name and click **Rename**

### Option B: Rename + Transfer (Recommended if doing both)
1. Go to your repository on GitHub
2. Click **Settings** → **General**
3. Scroll to the **Transfer ownership** section
4. Transfer to the organization first
5. Then rename the repository (Settings → General → Repository name)

**Why do both at once?**
- Only one remote URL update needed locally
- Cleaner process with less chance of confusion
- Single verification step

---

## Step 2: Update Local Git Remote

After completing the rename (and transfer, if applicable) on GitHub, update your local git remote URL.

### Check Current Remote
```bash
git remote -v
```

Example output:
```
origin  git@username.github.com:username/nightofworship-levites.git (fetch)
origin  git@username.github.com:username/nightofworship-levites.git (push)
```

### Update Remote URL

**If only renaming:**
```bash
git remote set-url origin git@github.com:username/new-repo-name.git
```

**If renaming AND transferring to organization:**
```bash
git remote set-url origin git@github.com:organization/new-repo-name.git
```

**Note:** Replace `git@github.com` with your actual GitHub SSH hostname if you use a custom one (e.g., `git@username.github.com`).

### Verify the Update
```bash
git remote -v
```

Example output after update:
```
origin  git@username.github.com:nightofworship/nowmanager.git (fetch)
origin  git@username.github.com:nightofworship/nowmanager.git (push)
```

### Test the Connection
```bash
git fetch origin
```

This verifies that your local repository can communicate with the renamed repository on GitHub.

---

## Step 3: Update Project Files

Search for references to the old repository name in your project files and update them.

### Common Files to Check
- `pyproject.toml` (Python projects)
- `package.json` (Node.js projects)
- `README.md`
- `.git/config` (usually auto-updated, but verify)
- Any documentation files

### Example: Updating pyproject.toml
```toml
[project]
name = "new-repo-name"  # Update this
version = "0.0.1"
# ... rest of config
```

### Commit the Changes
```bash
git add pyproject.toml  # or other files you updated
git commit -m "Rename project from old-name to new-name"
git push origin main
```

(Use `master` instead of `main` if that's your default branch)

---

## Step 4: Optional - Rename Local Directory

If you want your local directory name to match the new repository name:

```bash
cd ..
mv old-repo-name new-repo-name
cd new-repo-name
```

**Note:** This is purely cosmetic and optional. Git doesn't care about the directory name.

---

## Complete Example Workflow

Here's a complete example of renaming `nightofworship-levites` to `nowmanager` and transferring to the `nightofworship` organization:

### 1. On GitHub (Web Interface)
- Transfer repository to `nightofworship` organization
- Rename repository to `nowmanager`

### 2. Locally (Terminal)
```bash
# Check current remote
git remote -v

# Update remote URL
git remote set-url origin git@username.github.com:nightofworship/nowmanager.git

# Verify update
git remote -v

# Test connection
git fetch origin

# Update project files (e.g., pyproject.toml)
# ... edit files ...

# Commit and push changes
git add pyproject.toml
git commit -m "Rename project from hyphenated-repo to repomanager"
git push origin main
```

---

## Troubleshooting

### `git fetch origin` fails
- Verify the repository name on GitHub matches what you set in the remote URL
- Check that you have access to the repository (especially after transferring to an org)
- Verify your SSH key is set up correctly: `ssh -T git@github.com`

### Remote URL still shows old name
- Double-check the command: `git remote set-url origin <new-url>`
- Verify with: `git remote -v`
- Make sure you're in the correct repository directory

### Can't push after rename
- Ensure you've completed the rename on GitHub first
- Verify branch name matches: `git push origin main` vs `git push origin master`
- Check repository permissions if transferred to an organization

---

## Quick Reference

```bash
# View current remote
git remote -v

# Update remote URL
git remote set-url origin git@github.com:username/repo-name.git

# Verify and test
git remote -v
git fetch origin

# Commit project file updates
git add <files>
git commit -m "Rename project"
git push origin main
```

---

**Remember:** Always rename on GitHub first, then update your local remote URL. This ensures your local repository stays in sync with the remote.
