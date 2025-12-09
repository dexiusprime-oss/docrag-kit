# GitHub Actions Workflows

This directory contains automated workflows for DocRAG Kit.

## Workflows

### 1. Tests (`test.yml`)

**Triggers:**
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches

**Jobs:**
- **test**: Runs on Ubuntu and macOS with Python 3.10, 3.11, 3.12
  - Installs dependencies
  - Runs full test suite (57 tests)
  - Tests package installation
  
- **lint**: Code quality checks
  - flake8 for syntax errors
  - black for code formatting
  - mypy for type checking
  
- **security**: Security checks
  - Scans for exposed secrets
  - Verifies .env is gitignored

### 2. Release (`release.yml`)

**Triggers:**
- Push of version tags (e.g., `v0.1.0`, `v1.2.3`)

**Jobs:**
- **test**: Runs full test suite before release
- **build**: Builds distribution packages
- **publish**: Publishes to PyPI and creates GitHub release

**Usage:**
```bash
# Create and push a version tag
git tag v0.1.0
git push origin v0.1.0
```

### 3. PR Checks (`pr-check.yml`)

**Triggers:**
- Pull request opened, synchronized, or reopened

**Jobs:**
- **validate**: PR validation
  - Checks PR title follows conventional commits
  - Scans diff for secrets
  - Checks for large files
  
- **test**: Runs tests with coverage
  - Generates coverage report
  - Uploads to Codecov
  - Comments on PR with results

## Setup Requirements

### Secrets

Add these secrets to your GitHub repository:

1. **PYPI_API_TOKEN** (for releases)
   - Go to https://pypi.org/manage/account/token/
   - Create a new API token
   - Add to GitHub: Settings → Secrets → Actions → New repository secret

### Branch Protection

Recommended branch protection rules for `main`:

1. Require pull request reviews
2. Require status checks to pass:
   - `test (ubuntu-latest, 3.10)`
   - `test (macos-latest, 3.10)`
   - `lint`
   - `security`
3. Require branches to be up to date
4. Include administrators

## Badges

Add these badges to your README.md:

```markdown
![Tests](https://github.com/dexiusprime-oss/docrag-kit/workflows/Tests/badge.svg)
![Release](https://github.com/dexiusprime-oss/docrag-kit/workflows/Release/badge.svg)
[![codecov](https://codecov.io/gh/dexiusprime-oss/docrag-kit/branch/main/graph/badge.svg)](https://codecov.io/gh/dexiusprime-oss/docrag-kit)
```

## Local Testing

Test workflows locally using [act](https://github.com/nektos/act):

```bash
# Install act
brew install act  # macOS
# or
curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash

# Run tests workflow
act -j test

# Run PR checks
act pull_request -j validate
```

## Troubleshooting

### Tests fail on specific Python version
- Check if dependencies are compatible with that Python version
- Update `pyproject.toml` if needed

### Release workflow fails
- Ensure PYPI_API_TOKEN is set correctly
- Check that version in `pyproject.toml` is updated
- Verify all tests pass

### PR checks fail
- Follow conventional commit format for PR titles
- Remove any secrets from code
- Reduce file sizes if needed
