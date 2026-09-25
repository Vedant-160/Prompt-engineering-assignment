import sys
import os

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from tools import scan_vulnerabilities


def test_hardcoded_secret():
    code = 'password = "admin123"'

    result = scan_vulnerabilities(code)

    assert any(
        finding["category"] == "Hardcoded Secret"
        for finding in result["findings"]
    )


def test_eval_detection():
    code = "result = eval(user_input)"

    result = scan_vulnerabilities(code)

    assert any(
        finding["category"] == "Code Injection"
        for finding in result["findings"]
    )


def test_sql_injection():
    code = 'query = "SELECT * FROM users WHERE id=" + user_id'

    result = scan_vulnerabilities(code)

    assert any(
        finding["category"] == "SQL Injection"
        for finding in result["findings"]
    )


def test_shell_true_detection():
    code = "subprocess.run(command, shell=True)"

    result = scan_vulnerabilities(code)

    assert any(
        finding["category"] == "Command Injection"
        for finding in result["findings"]
    )


def test_pickle_detection():
    code = "data = pickle.loads(user_data)"

    result = scan_vulnerabilities(code)

    assert any(
        finding["category"] == "Insecure Deserialization"
        for finding in result["findings"]
    )


def test_weak_hashing():
    code = "hash = md5(password)"

    result = scan_vulnerabilities(code)

    assert any(
        finding["category"] == "Weak Hashing"
        for finding in result["findings"]
    )


def test_clean_code():
    code = """
def add(a, b):
    return a + b
"""

    result = scan_vulnerabilities(code)

    assert result["findings"] == []


def test_missing_input_validation():
    code = 'username = input("Enter username: ")'

    result = scan_vulnerabilities(code)

    assert any(
        finding["category"] == "Missing Input Validation"
        for finding in result["findings"]
    )