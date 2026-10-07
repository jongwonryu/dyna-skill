"""Send one short request using the legacy SDK used by the generation scripts."""

import os

import openai


def main():
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    if not openai.api_key:
        raise SystemExit("Set OPENAI_API_KEY before running this API check.")
    response = openai.ChatCompletion.create(
        model=os.environ.get("OPENAI_MODEL", "gpt-4-turbo"),
        messages=[{"role": "user", "content": "Reply with OK."}],
        max_tokens=10,
        temperature=0,
    )
    print(response.choices[0].message["content"].strip())


if __name__ == "__main__":
    main()
