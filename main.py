import os, sys
from dotenv import load_dotenv

from google import genai
from google.genai import types

from available_functions import available_functions, function_map
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
        function_call_result = call_function(function_call_part)
        if not function_call_result.parts[0].function_response.response:
            raise Exception("Error while trying to call the function:", function_call_part.name)
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")


def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    function_call_part.args["working_directory"] = "./calculator"

    try:
        function_result = function_map[function_call_part.name](**function_call_part.args)
    except NameError:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": function_result},
            )
        ],
    )


if __name__ == "__main__":
    main()
