# Security Policy

## Supported Versions

We release patches for security vulnerabilities. Which versions are eligible for receiving such patches depends on the CVSS v3.0 Rating:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take the security of Voynich Morphemic Decryption seriously. If you believe you have found a security vulnerability, please report it to us as described below.

### Where to Report

**Please do NOT report security vulnerabilities through public GitHub issues.**

Instead, please report them via email to:
- **Email:** mateuszpiesiak1990@gmail.com
- **Subject:** [SECURITY] Voynich Morphemic Decryption Vulnerability

### What to Include

Please include the following information in your report:

- Type of issue (e.g., buffer overflow, SQL injection, cross-site scripting, etc.)
- Full paths of source file(s) related to the manifestation of the issue
- The location of the affected source code (tag/branch/commit or direct URL)
- Any special configuration required to reproduce the issue
- Step-by-step instructions to reproduce the issue
- Proof-of-concept or exploit code (if possible)
- Impact of the issue, including how an attacker might exploit it

### Response Timeline

- **Initial Response:** Within 48 hours of report receipt
- **Confirmation:** Within 5 business days
- **Fix Timeline:** Depends on severity and complexity
- **Disclosure:** Coordinated disclosure after fix is released

## Security Update Process

1. Security vulnerability is reported privately
2. Team confirms the vulnerability and determines severity
3. Fix is developed and tested
4. Security advisory is drafted
5. Fix is released
6. Security advisory is published

## Preferred Languages

We prefer all communications to be in English or Polish.

## Security Best Practices

When using Voynich Morphemic Decryption:

### API Security

- Always use HTTPS in production
- Implement rate limiting
- Validate all input data
- Use environment variables for sensitive data
- Never commit secrets to version control

### Docker Security

- Use specific image tags, not `latest`
- Run containers as non-root user
- Scan images for vulnerabilities
- Keep base images updated

### Dependency Security

- Regularly update dependencies
- Use `pip-audit` or `safety` to check for known vulnerabilities
- Pin dependency versions in production

```bash
# Check for known vulnerabilities
pip-audit

# Or using safety
safety check
```

### Environment Variables

Never commit sensitive information. Use `.env` files (gitignored):

```bash
cp .env.example .env
# Edit .env with your sensitive data
```

## Known Security Considerations

### Input Validation

All user inputs are validated using Pydantic models. However:

- Very large inputs may cause memory issues
- Complex regex in word patterns could lead to ReDoS

### API Rate Limiting

Currently, API does not implement rate limiting. For production:

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
```

### Data Privacy

This project analyzes text data. Ensure:

- You have rights to analyze the data
- No personal/sensitive information in analyzed text
- Compliance with GDPR if applicable

## Security Checklist for Contributors

Before submitting code:

- [ ] No hardcoded secrets or credentials
- [ ] Input validation for all user-provided data
- [ ] SQL injection prevention (N/A - we use JSON)
- [ ] XSS prevention in any HTML output
- [ ] CSRF protection for state-changing operations
- [ ] Secure random number generation where needed
- [ ] Proper error handling (no sensitive data in errors)
- [ ] Dependencies are up to date
- [ ] Code has been scanned with Bandit

```bash
# Run security scan
bandit -r src/

# Check dependencies
safety check
```

## Acknowledgments

We thank the following researchers for responsibly disclosing vulnerabilities:

(None reported yet)

---

**Last Updated:** 2025-11-07
