import os
import subprocess


schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": (
            "Runs a Python file relative to the working directory with "
            "optional command-line arguments"
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": (
                        "Path to the Python file to run, relative to the "
                        "working directory"
                    ),
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional command-line arguments",
                },
            },
            "required": ["file_path"],
        },
    },
}


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        absolute_file_path = os.path.abspath(
            os.path.join(working_dir_abs, file_path)
        )

        # Make sure file is inside working directory
        if os.path.commonpath(
            [working_dir_abs, absolute_file_path]
        ) != working_dir_abs:
            return (
                f'Error: Cannot execute "{file_path}" '
                f"as it is outside the permitted working directory"
            )

        # Make sure file exists and is a regular file
        if not os.path.isfile(absolute_file_path):
            return (
                f'Error: "{file_path}" '
                f"does not exist or is not a regular file"
            )

        # Make sure it is a Python file
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        # Build command
        command = ["python", absolute_file_path]

        if args:
            command.extend(args)

        # Run Python file
        result = subprocess.run(
            command,
            cwd=working_dir_abs,
            capture_output=True,
            text=True,
            timeout=30,
        )

        output = []

        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")

        if not result.stdout and not result.stderr:
            output.append("No output produced")
        else:
            if result.stdout:
                output.append(f"STDOUT:\n{result.stdout}")

            if result.stderr:
                output.append(f"STDERR:\n{result.stderr}")

        return "\n".join(output)

    except Exception as e:
        return f"Error: executing Python file: {e}"