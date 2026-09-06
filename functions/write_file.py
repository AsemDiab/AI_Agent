import os


schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": (
            "Writes content to a file relative to the working directory, "
            "creating parent directories when needed"
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": (
                        "Path to the file to write, relative to the "
                        "working directory"
                    ),
                },
                "content": {
                    "type": "string",
                    "description": "Content to write to the file",
                },
            },
            "required": ["file_path", "content"],
        },
    },
}


def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)

        target_file = os.path.normpath(
            os.path.join(working_dir_abs, file_path)
        )

        # Make sure the target is inside working_directory
        valid_target_file = (
            os.path.commonpath([working_dir_abs, target_file])
            == working_dir_abs
        )

        if not valid_target_file:
            return (
                f'Error: Cannot write to "{file_path}" '
                f'as it is outside the permitted working directory'
            )

        # Cannot write to an existing directory
        if os.path.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        # Create missing parent directories
        parent_dir = os.path.dirname(target_file)
        os.makedirs(parent_dir, exist_ok=True)

        # Write/overwrite the file
        with open(target_file, "w") as f:
            f.write(content)

        return (
            f'Successfully wrote to "{file_path}" '
            f'({len(content)} characters written)'
        )

    except Exception as e:
        return f"Error: {e}"