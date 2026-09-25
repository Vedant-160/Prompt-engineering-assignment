import re


def scan_vulnerabilities(code: str, language: str = "") -> dict:
    """
    Scan source code for common security vulnerabilities.

    Args:
        code: Source code to analyze.
        language: Optional programming language.

    Returns:
        Dictionary containing detected security findings.
    """

    findings = []

    if not code or not code.strip():
        return {
            "findings": [],
            "message": "No code was provided for scanning."
        }

    lines = code.splitlines()

    for line_number, line in enumerate(lines, start=1):

        # 1. Hardcoded secrets / API keys
        if re.search(
            r'(?i)(api[_-]?key|secret|password|token)\s*=\s*[\'"][^\'"]+[\'"]',
            line
        ):
            findings.append({
                "category": "Hardcoded Secret",
                "severity": "High",
                "line": line_number,
                "description": "A possible secret or credential is hardcoded.",
                "fix": "Store secrets in environment variables or a secure secret manager."
            })

        # 2. eval() / exec()
        if re.search(r'\b(eval|exec)\s*\(', line):
            findings.append({
                "category": "Code Injection",
                "severity": "High",
                "line": line_number,
                "description": "eval() or exec() may execute untrusted input.",
                "fix": "Avoid eval() or exec() with untrusted data and use safer alternatives."
            })

        # 3. SQL injection
        if re.search(
            r'(?i)(SELECT|INSERT|UPDATE|DELETE).*[\+\%]|f[\'"].*(SELECT|INSERT|UPDATE|DELETE)',
            line
        ):
            findings.append({
                "category": "SQL Injection",
                "severity": "High",
                "line": line_number,
                "description": "SQL query may be constructed using string concatenation or interpolation.",
                "fix": "Use parameterized queries or prepared statements."
            })

        # 4. subprocess shell=True
        if re.search(r'subprocess\..*shell\s*=\s*True', line):
            findings.append({
                "category": "Command Injection",
                "severity": "High",
                "line": line_number,
                "description": "subprocess is used with shell=True.",
                "fix": "Avoid shell=True and pass command arguments as a list."
            })

        # 5. pickle.loads()
        if re.search(r'\bpickle\.loads\s*\(', line):
            findings.append({
                "category": "Insecure Deserialization",
                "severity": "High",
                "line": line_number,
                "description": "pickle.loads() can execute malicious content from untrusted data.",
                "fix": "Avoid deserializing untrusted pickle data."
            })

        # 6. Unsafe yaml.load()
        if re.search(r'\byaml\.load\s*\(', line) and "SafeLoader" not in line:
            findings.append({
                "category": "Insecure Deserialization",
                "severity": "High",
                "line": line_number,
                "description": "yaml.load() may be unsafe without SafeLoader.",
                "fix": "Use yaml.safe_load() or explicitly use SafeLoader."
            })

        # 7. Weak hashing
        if re.search(r'\b(md5|sha1)\s*\(', line, re.IGNORECASE):
            findings.append({
                "category": "Weak Hashing",
                "severity": "Medium",
                "line": line_number,
                "description": "MD5 or SHA1 should not be used for password hashing.",
                "fix": "Use Argon2, bcrypt, or scrypt for password hashing."
            })

        # 8. Missing input validation
        if re.search(r'\binput\s*\(', line):
            findings.append({
                "category": "Missing Input Validation",
                "severity": "Medium",
                "line": line_number,
                "description": "User-controlled input is accepted without visible validation.",
                "fix": "Validate, sanitize, and constrain user input before processing it."
            })

    return {
        "findings": findings
    }