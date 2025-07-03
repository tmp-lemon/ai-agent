import os

from google.genai import types


def write_file(working_directory, file_path, content):
    try:
        wd_abspath = os.path.abspath(working_directory)
            
        if file_path:
            file_abspath = os.path.abspath(os.path.join(working_directory, file_path))

        if not file_abspath.startswith(wd_abspath):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        dirs_abspath = "/".join(file_abspath.split("/")[:-1]) + "/"
        if not os.path.exists(dirs_abspath):
            os.makedirs(dirs_abspath)

        with open(file_abspath, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file within the working directory. Creates the file if it doesn't exist.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the file.",
            ),
        },
    ),
)
