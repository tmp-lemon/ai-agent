import os, subprocess


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

        command = ["python3", file_abspath]
        completed_process = subprocess.run(args=command, timeout=30, capture_output=True, cwd=wd_abspath)

        stdout = completed_process.stdout

        if not stdout:
            return f"No output produced."

        stderr = completed_process.stderr
        return_code = completed_process.returncode

        output = [f"STDOUT: {stdout}", f"STDERR: {stderr}"]

        if return_code != 0:
            output.append(f"Process exited with code {return_code}")

        return "\n".join(output)

    except Exception as e:
        return f"Error: {e}"
