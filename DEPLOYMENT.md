# Deployment Guide for Voynich Morphemic Decryption

## Table of Contents
- [GitHub Setup](#github-setup)
- [Push to GitHub](#push-to-github)
- [Enable GitHub Features](#enable-github-features)
- [Docker Hub Setup](#docker-hub-setup)
- [PyPI Publishing](#pypi-publishing)
- [Zenodo Integration](#zenodo-integration)

---

## GitHub Setup

### 1. Create GitHub Repository

```bash
# Go to GitHub and create a new repository:
# https://github.com/new
# Repository name: voynich-morphemic-decryption
# Description: Advanced morphemic analysis & decryption of Voynich Manuscript
# Public repository
# Do NOT initialize with README (we already have one)
```

### 2. Add Remote and Push

```bash
# Add GitHub as remote
git remote add origin https://github.com/mati83moni/voynich-morphemic-decryption.git

# Push main branch
git push -u origin main

# Push other branches
git push origin develop
git push origin feature/api-enhancements
git push origin feature/advanced-analysis

# Push tags (if any)
git push --tags
```

---

## Enable GitHub Features

### 1. Issues

- Go to repository Settings → Features
- Enable Issues
- Issue templates are already configured in `.github/ISSUE_TEMPLATE/`

### 2. Discussions

- Go to Settings → Features → Enable Discussions
- Create categories:
  - General
  - Q&A
  - Research
  - Ideas

### 3. Projects

- Go to Projects tab
- Create new project: "Voynich Analysis Roadmap"
- Use Board view
- Add columns:
  - Backlog
  - To Do
  - In Progress
  - Done

### 4. Wiki

- Go to Wiki tab
- Create pages:
  - Home
  - Installation
  - API Documentation
  - Research Methods

### 5. GitHub Pages

- Go to Settings → Pages
- Source: GitHub Actions
- Will be automatically deployed by `.github/workflows/docs.yml`

### 6. Branch Protection

```bash
# Go to Settings → Branches
# Add rule for main branch:
```

- Require pull request reviews before merging
- Require status checks to pass before merging
- Require conversation resolution before merging
- Do not allow bypassing the above settings

---

## Docker Hub Setup

### 1. Create Docker Hub Account

- Sign up at https://hub.docker.com
- Create repository: `voynich-analysis`

### 2. Add Secrets to GitHub

```bash
# Go to GitHub repository → Settings → Secrets and variables → Actions
# Add new repository secrets:
```

- `DOCKER_USERNAME`: Your Docker Hub username
- `DOCKER_PASSWORD`: Your Docker Hub access token

### 3. Test Docker Build Locally

```bash
# Build image
docker build -t voynich-analysis:latest -f Docker/Dockerfile .

# Test run
docker run --rm voynich-analysis:latest python -c "import voynich_decryption; print(voynich_decryption.__version__)"

# Push to Docker Hub (manual)
docker tag voynich-analysis:latest yourusername/voynich-analysis:latest
docker push yourusername/voynich-analysis:latest
```

---

## PyPI Publishing

### 1. Create PyPI Account

- Sign up at https://pypi.org
- Verify email
- Enable 2FA (recommended)
- Create API token

### 2. Add PyPI Token to GitHub

```bash
# Go to GitHub repository → Settings → Secrets and variables → Actions
# Add new repository secret:
```

- `PYPI_API_TOKEN`: Your PyPI API token

### 3. Test Package Build

```bash
# Install build tools
pip install build twine

# Build package
python -m build

# Check package
twine check dist/*

# Test upload to TestPyPI (optional)
twine upload --repository testpypi dist/*

# Upload to PyPI (manual)
twine upload dist/*
```

### 4. Automated Release Process

```bash
# When ready to release:
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0

# This will trigger:
# 1. GitHub Release creation (.github/workflows/release.yml)
# 2. PyPI package upload
# 3. Docker image build and push
```

---

## Zenodo Integration

### 1. Connect GitHub to Zenodo

- Go to https://zenodo.org (or https://sandbox.zenodo.org for testing)
- Log in with GitHub
- Go to GitHub settings in Zenodo
- Enable webhook for `voynich-morphemic-decryption`

### 2. Create Release for DOI

```bash
# Create a release tag
git tag -a v1.0.0 -m "Initial release for Zenodo DOI"
git push origin v1.0.0
```

- Zenodo will automatically create a DOI
- Edit the Zenodo record to add:
  - Detailed description
  - Keywords
  - Funding information
  - License (MIT)

### 3. Manual Zenodo Upload

```bash
# Set environment variable
export ZENODO_TOKEN="your_zenodo_token_here"

# For testing (sandbox)
export ZENODO_SANDBOX=true

# Run deployment script
python scripts/deploy_zenodo.py
```

---

## CI/CD Pipeline

### Workflows Overview

The repository includes 3 GitHub Actions workflows:

#### 1. CI/CD Pipeline (`.github/workflows/ci-pipeline.yml`)

Runs on every push and pull request:
- Linting (Ruff, Black)
- Type checking (MyPy)
- Security scanning (Bandit)
- Tests on multiple OS (Ubuntu, macOS, Windows)
- Coverage reporting (Codecov)
- Docker build test

#### 2. Documentation (`.github/workflows/docs.yml`)

Runs on main branch pushes:
- Builds Sphinx documentation
- Deploys to GitHub Pages

#### 3. Release (`.github/workflows/release.yml`)

Runs on version tags:
- Creates GitHub Release
- Publishes to PyPI
- Builds and pushes Docker image

### Required Secrets

Add these to GitHub repository secrets:

```
CODECOV_TOKEN          # From codecov.io
DOCKER_USERNAME        # Docker Hub username
DOCKER_PASSWORD        # Docker Hub token
PYPI_API_TOKEN        # PyPI API token
ZENODO_TOKEN          # Zenodo API token (optional)
```

---

## Post-Deployment Checklist

### After First Push

- [ ] Verify GitHub Actions run successfully
- [ ] Check code coverage report on Codecov
- [ ] Test Docker image from Docker Hub
- [ ] Verify documentation on GitHub Pages
- [ ] Create first GitHub issue for tracking
- [ ] Set up GitHub Project board
- [ ] Enable GitHub Discussions
- [ ] Add repository topics/tags
- [ ] Add repository description and website
- [ ] Create first pull request (from develop to main)

### Before Public Release

- [ ] Review all documentation
- [ ] Ensure all tests pass
- [ ] Check security scan results
- [ ] Update CHANGELOG.md
- [ ] Create release notes
- [ ] Tag version
- [ ] Monitor automated workflows
- [ ] Verify PyPI package
- [ ] Verify Docker image
- [ ] Share on social media / research platforms

---

## Monitoring and Maintenance

### Regular Tasks

**Weekly:**
- Review and respond to issues
- Review pull requests
- Check CI/CD status
- Monitor dependency updates

**Monthly:**
- Update dependencies
- Review security alerts
- Update documentation
- Review analytics

**Quarterly:**
- Major version planning
- Community survey
- Performance benchmarks
- Infrastructure review

---

## Troubleshooting

### GitHub Actions Failing

```bash
# Check workflow logs
# Settings → Actions → View workflow runs

# Common fixes:
# 1. Update dependencies in requirements.txt
# 2. Check Python version compatibility
# 3. Review test failures
# 4. Check secret variables
```

### Docker Build Issues

```bash
# Test locally
docker build -t test -f Docker/Dockerfile .

# Check logs
docker logs <container_id>

# Debug mode
docker run -it --rm voynich-analysis:test /bin/bash
```

### PyPI Upload Fails

```bash
# Verify package
twine check dist/*

# Test with TestPyPI first
twine upload --repository testpypi dist/*
```

---

## Support

For deployment help:
- Open an issue on GitHub
- Email: mateuszpiesiak1990@gmail.com
- Check CONTRIBUTING.md for guidelines

---

**Last Updated:** 2025-11-07
