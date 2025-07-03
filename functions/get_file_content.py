import os

from google.genai import types


def get_file_content(working_directory, file_path):
    try:
        wd_abspath = os.path.abspath(working_directory)
        
        if file_path:
            file_abspath = os.path.abspath(os.path.join(working_directory, file_path))

        if not file_abspath.startswith(wd_abspath):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(file_abspath):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        MAX_CHARS = 10000

        with open(file_abspath, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            
            if len(file_content_string) >= MAX_CHARS:
                file_content_string += '\n[...File "{file_path}" truncated at 10000 characters]'
            
            return file_content_string
    
    except Exception as e:
        return f"Error: {e}"


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads and returns the first 10000 characters of the content from a specified file within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file whose content should be read, relative to the working directory.",
            ),
        },
    ),
)
