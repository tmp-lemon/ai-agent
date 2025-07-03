import os, subprocess

from google.genai import types


def run_python_file(working_directory, file_path):
    try:
        wd_abspath = os.path.abspath(working_directory)
            
        if file_path:
            file_abspath = os.path.abspath(os.path.join(working_directory, file_path))

        if not file_abspath.startswith(wd_abspath):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.exists(file_abspath):
            return f'Error: File "{file_path}" not found.'

        if not file_abspath.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'

        commands = ["python", file_abspath]

        completed_process = subprocess.run(
            args=commands, 
            text=True, 
            timeout=30, 
            capture_output=True, 
            cwd=wd_abspath
        )

        output = []

        if completed_process.stdout:
            output.append(f"STDOUT:\n{completed_process.stdout}")

        if completed_process.stderr:
            output.append(f"STDERR:\n{completed_process.stderr}")
            
        return_code = completed_process.returncode

        if return_code != 0:
            output.append(f"\nProcess exited with code {return_code}")

        return "\n".join(output) if output else "No output produced."

    except Exception as e:
        return f"Error: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file within the working directory and returns the output from the interpreter.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory.",
            ),
        },
    ),
)
