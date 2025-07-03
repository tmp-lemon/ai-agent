import os

from google.genai import types


def get_files_info(working_directory, directory=None):
    wd_abs_path = os.path.abspath(working_directory)
    d_abs_path = wd_abs_path

    if directory:
        d_abs_path = os.path.abspath(os.path.join(working_directory, directory))

    if not d_abs_path.startswith(wd_abs_path):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(d_abs_path):
        return f'Error: "{directory}" is not a directory'

    try:
        files_info = []
    
        for file in os.listdir(d_abs_path):
            file_abs_path = os.path.join(d_abs_path, file)
            file_size = os.path.getsize(file_abs_path)
            is_dir = os.path.isdir(file_abs_path)

            files_info.append(f"- {file}: file_size={file_size} bytes, is_dir={is_dir}")

        return "\n".join(files_info)
    except Exception as e:
        return f"Error: {e}"


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
