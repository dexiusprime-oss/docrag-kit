# Security Rules

## API Keys and Secrets Protection

### Critical Rules for Deployment

**NEVER commit API keys, tokens, or secrets to version control!**

Before any push or deployment:
1. **Scan for exposed secrets** - Check all changed files for API keys
2. **Use templates only** - Only `.env.example` files should be committed
3. **Verify .gitignore** - Ensure `.env` files are excluded
4. **Review diffs** - Always review `git diff` before pushing

### Patterns to Watch For

API keys and tokens that must NEVER be committed:
- `OPENAI_API_KEY=sk-...`
- `GOOGLE_API_KEY=...`
- `GITHUB_TOKEN=ghp_...`
- `AWS_SECRET_ACCESS_KEY=...`
- Any string starting with: `sk-`, `ghp_`, `gho_`, `Bearer `, etc.

### Required File Structure

**ALLOWED in git:**
- `.env.example` - Template with placeholder values like `your_key_here`
- `.gitignore` - Must include `.env` exclusion

**FORBIDDEN in git:**
- `.env` - Contains real API keys
- Any file with actual API keys or tokens

### Pre-Push Checklist

Before `git push`:
```bash
# 1. Check for exposed secrets
git diff --cached | grep -E "(sk-|ghp_|gho_|API_KEY=.{20,})"

# 2. Verify .env is ignored
git status | grep ".env$"  # Should show nothing

# 3. Review all changes
git diff --cached
```

### If Keys Are Exposed

If API keys were accidentally committed:
1. **Revoke the exposed keys immediately** at provider's dashboard
2. **Remove from git history** using `git filter-branch` or BFG Repo-Cleaner
3. **Generate new keys** and update `.env` locally
4. **Never reuse exposed keys**

### Code Review Requirements

All pull requests must:
- Not contain any `.env` files
- Only include `.env.example` with placeholders
- Have `.gitignore` properly configured
- Pass secret scanning checks

## Implementation in DocRAG Kit

The project implements these protections:
- Automatic `.gitignore` creation during `docrag init`
- `.env.example` templates with clear placeholders
- Security warnings in documentation
- Separate storage for secrets (`.env`) and config (`.docrag/config.yaml`)
