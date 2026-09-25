import os

try:
    from google import genai
    from google.genai import types
except ImportError:
    genai = None
    types = None

from tools import scan_vulnerabilities
from prompts import SYSTEM_PROMPT


def main():
    if genai is None or types is None:
        print("Missing dependency: google-genai is not installed.")
        print("Install it with one of these commands:")
        print("  py -3.11 -m pip install -r requirements.txt")
        print("  python3 -m pip install google-genai")
        return

    # Get Gemini API key from environment variable
    api_key = os.getenv(GEMINI_API_KEY)

    if not api_key:
        print("Error: GEMINI_API_KEY environment variable is not set.")
        return

    # Create Gemini client
    client = genai.Client(api_key=api_key)

    # Display application title
    print("=" * 60)
    print("          AI SECURITY CODE REVIEWER")
    print("=" * 60)

    # Get user's security question
    query = input("\nEnter your security question: ")

    # Get code from the user
    print("\nPaste your code below.")
    print("Type END on a new line when finished.\n")

    code_lines = []

    while True:
        line = input()

        if line == "END":
            break

        code_lines.append(line)

    code = "\n".join(code_lines)

    # Check whether code was provided
    if not code.strip():
        print("\nError: Code snippet cannot be empty.")
        return

    # Get programming language
    language = input("\nEnter programming language (optional): ")

    # Prepare prompt for Gemini
    user_prompt = f"""
User question:
{query}

Programming language:
{language}

Code snippet:
```text
{code}
```

Review this code for security vulnerabilities.
"""

    try:
        # Send request to Gemini with the local security scanner as a tool
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=user_prompt,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                tools=[scan_vulnerabilities]
            )
        )

        # Display security review
        print("\n" + "=" * 60)
        print("SECURITY REVIEW")
        print("=" * 60)
        print(response.text)

    except Exception as e:
        print("\nError while communicating with Gemini:")
        print(str(e))


# Start the application
if __name__ == "__main__":
    main()