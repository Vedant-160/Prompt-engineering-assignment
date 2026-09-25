Yes. Use the same README structure I provided, but remove all emoji characters. The project title and headings should be clean and professional:

````markdown
# CodeSentry — AI-Powered Security Code Reviewer

CodeSentry is a Python-based AI security code reviewer that uses Google's Gemini API to analyze source code for potential security vulnerabilities.

The application combines an LLM-based security expert with a local static-analysis tool called `scan_vulnerabilities`. The Gemini model automatically decides when the vulnerability scanner should be invoked based on the user's question and the submitted code.

## Features

- AI-powered security code review using Google Gemini
- Automatic vulnerability detection
- Local `scan_vulnerabilities` tool exposed to the Gemini model
- Detection of common security issues:
  - Hardcoded secrets and API keys
  - `eval()` / `exec()` with potentially untrusted input
  - SQL injection risks
  - `subprocess(..., shell=True)` usage
  - Insecure deserialization
  - Weak hashing algorithms such as MD5 and SHA-1
  - Missing input validation
- Structured security findings
- Severity classification
- Line references for detected vulnerabilities
- Suggested fixes
- Plain-language security explanations
- Unit-testable vulnerability scanner
- Error handling for API and tool failures

## Project Structure

```text
code_sentry/
│
├── main.py                  # Application entry point
├── tools.py                 # scan_vulnerabilities implementation
├── prompts.py               # Gemini system prompt
│
├── tests/
│   └── test_tools.py        # Unit tests for vulnerability scanner
│
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variable template
└── README.md                # Project documentation
````

## Requirements

* Python 3.10+
* Google Gemini API key
* Google Gen AI Python SDK

## Installation

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd code_sentry
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

Or:

```bash
pip install google-genai
```

## Environment Configuration

Set your Gemini API key using the `GEMINI_API_KEY` environment variable.

Windows PowerShell:

```powershell
$env:GEMINI_API_KEY="your_api_key_here"
```

Windows CMD:

```cmd
set GEMINI_API_KEY=your_api_key_here
```

Linux/macOS:

```bash
export GEMINI_API_KEY="your_api_key_here"
```

Never commit your API key to the repository.

## Running the Application

Run:

```bash
python main.py
```

The application accepts:

1. A natural-language security question
2. A source-code snippet

Example:

```text
Query:
Is this function safe to use in production?

Code:
import subprocess

def run_command(command):
    return subprocess.run(
        command,
        shell=True,
        capture_output=True
    )
```

The Gemini model analyzes the request and determines whether the local vulnerability scanner should be called.

## Vulnerability Detection

The `scan_vulnerabilities` function performs local heuristic-based analysis of the submitted code.

The scanner checks for:

| Vulnerability            | Example                                     |
| ------------------------ | ------------------------------------------- |
| Hardcoded secrets        | `API_KEY = "abc123"`                        |
| Dangerous evaluation     | `eval(user_input)`                          |
| Code execution           | `exec(user_input)`                          |
| SQL Injection            | `"SELECT * FROM users WHERE id=" + user_id` |
| Command Injection        | `subprocess.run(cmd, shell=True)`           |
| Insecure deserialization | `pickle.loads(data)`                        |
| Unsafe YAML loading      | `yaml.load(data)`                           |
| Weak hashing             | `hashlib.md5(password)`                     |
| Weak hashing             | `hashlib.sha1(password)`                    |
| Missing validation       | Direct use of user-controlled input         |

## AI Tool Calling

A key requirement of this project is that Gemini decides whether to call `scan_vulnerabilities`.

The scanner is not hardcoded to run for every request.

The workflow is:

```text
User
  |
  v
Query + Code Snippet
  |
  v
Gemini Security Agent
  |
  +----------------------+
  |                      |
  v                      v
Clean Code          Potential Risk
  |                      |
  |                      v
  |              scan_vulnerabilities()
  |                      |
  |                      v
  |                 Scan Results
  |                      |
  +----------+-----------+
             |
             v
      Gemini Final Review
             |
             v
     Structured Response
```

## System Prompt

Gemini is configured with a system instruction that establishes it as a security expert.

The model is responsible for:

* Reviewing source code for security vulnerabilities
* Understanding the user's security question
* Calling `scan_vulnerabilities` when appropriate
* Explaining detected risks
* Recommending fixes
* Communicating findings in developer-friendly language

## Output Format

The final response follows a consistent structure:

```text
Summary Verdict
---------------
Needs Attention

Findings
--------
1. Command Injection
   Severity: High
   Line: 4

   Issue:
   The application executes a command using shell=True.

   Suggested Fix:
   Avoid shell=True and pass command arguments as a list.

Explanation
-----------
The command may be influenced by untrusted user input.
An attacker could potentially execute unintended operating
system commands.
```

## Example: SQL Injection

Input:

```python
user_id = input("Enter user ID: ")

query = "SELECT * FROM users WHERE id = " + user_id

cursor.execute(query)
```

Query:

```text
Is this code safe from SQL injection?
```

Example output:

```text
Summary Verdict:
High Risk

Findings:

1. SQL Injection
   Severity: High
   Line: 3

   Issue:
   The SQL query is constructed using string concatenation
   with user-controlled input.

   Suggested Fix:
   Use parameterized queries instead of concatenating
   user input directly into SQL statements.

Explanation:
An attacker may manipulate the user_id value to alter the
SQL query and potentially access or modify unauthorized data.
```

## Example: Hardcoded Secret

Input:

```python
API_KEY = "sk-example-secret-key"

def connect():
    return connect_to_service(API_KEY)
```

Query:

```text
Can I safely commit this code to GitHub?
```

Example output:

```text
Summary Verdict:
High Risk

Findings:

1. Hardcoded Secret
   Severity: High
   Line: 1

   Issue:
   A secret/API key is directly embedded in the source code.

   Suggested Fix:
   Store the secret in an environment variable or secure
   secret-management system.

Explanation:
Anyone who gains access to the repository may obtain the
credential. The key should be removed from the source code
and rotated if it has already been exposed.
```

## Example: Clean Code

Input:

```python
def add_numbers(a, b):
    return a + b
```

Query:

```text
Are there any obvious security vulnerabilities here?
```

Example output:

```text
Summary Verdict:
Safe

Findings:
No obvious security vulnerabilities detected.

Explanation:
The function performs a simple arithmetic operation and does
not contain any of the risky patterns checked by the scanner.
```

## Testing

Run the unit tests using:

```bash
python -m unittest discover
```

Or, if using pytest:

```bash
pytest
```

The tests should cover:

```text
Hardcoded API key detection
eval() detection
exec() detection
SQL injection detection
shell=True detection
pickle.loads detection
Unsafe yaml.load detection
MD5/SHA-1 detection
Clean code
Empty code
```

## Error Handling

The application handles common failures gracefully, including:

* Missing Gemini API key
* Gemini API errors
* Invalid tool arguments
* Empty code snippets
* Unexpected scanner errors
* Invalid user input

Instead of crashing, the application should return a clear error message.

## Design Assumptions

1. Submitted code is provided as plain text.
2. The local scanner uses regex/heuristic-based detection.
3. Detection does not constitute a complete security audit.
4. A detected pattern represents a potential security issue and may require further investigation.
5. Gemini is responsible for deciding when the local scanner should be invoked.
6. The scanner does not execute the submitted source code.
7. API credentials are supplied through environment variables.
8. The scanner provides supporting security findings to the LLM rather than replacing human security review.

## Limitations

CodeSentry is intended as an educational security-review assistant and should not replace:

* Professional penetration testing
* Manual code review
* SAST/DAST platforms
* Dependency vulnerability scanners
* Security architecture reviews
* Production security audits

Regex and heuristic-based detection can produce both false positives and false negatives.

## Future Improvements

Potential improvements include:

* Bandit integration
* Support for additional programming languages
* Dependency vulnerability scanning
* CVE database integration
* OWASP Top 10 mapping
* CWE classification
* Improved line-level analysis
* JSON output mode
* Web interface
* GitHub Pull Request integration
* Automated security reports
* Multi-file project analysis

## Assignment Requirements

This project implements the requirements specified in Assignment 6:

* Python 3.10+
* Google Gen AI SDK
* Natural-language query and code input
* Security-focused system prompt
* Local `scan_vulnerabilities` function
* Automatic model-driven tool invocation
* Structured vulnerability findings
* Error handling
* Unit-testable scanner
* README documentation
* Demonstration examples

## Author

**Dhiraj Joshi**

AI & Data Science Student

GitHub: [https://github.com/dhiraj-dev-19](https://github.com/dhiraj-dev-19)

## License

This project is created for educational and assignment purposes.

```

This version is cleaner for a GitHub repository and stays aligned with the assignment requirements, including the required project structure and README contents. :contentReference[oaicite:0]{index=0}
```
