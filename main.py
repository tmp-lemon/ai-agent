import os, sys
from dotenv import load_dotenv

from google import genai
from google.genai import types

from available_functions import available_functions
from system_prompt import system_prompt


def main():
    if len(sys.argv) < 2:
        print("prompt not provided")
        sys.exit(1)
    
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    model = "gemini-2.0-flash-001"
    
    user_prompt = sys.argv[1]
    verbose = len(sys.argv) > 2 and sys.argv[2] == "--verbose"
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    generate_content(client, model, messages, user_prompt, verbose)


def generate_content(client, model, messages, user_prompt, verbose):
    response = client.models.generate_content(
        model=model, 
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt
        )
    )

    if verbose:
        print("User prompt:", user_prompt)
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)    
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    if not response.function_calls:
        return response.text
    
    for function_call_part in response.function_calls:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")  


if __name__ == "__main__":
    main()
