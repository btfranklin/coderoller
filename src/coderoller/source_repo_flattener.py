import os

# Dictionary mapping file extensions to their corresponding long form names
FILE_TYPES = {
    ".py": "python",
    ".js": "javascript",
    ".jsx": "jsx",
    ".ts": "typescript",
    ".tsx": "tsx",
    ".swift": "swift",
    ".go": "go",
    ".java": "java",
    ".c": "c",
    ".cpp": "c++",
    ".h": "c",
    ".hpp": "c++",
    ".cs": "csharp",
    ".lua": "lua",
    ".rb": "ruby",
    ".php": "php",
    ".pl": "perl",
    ".html": "html",
    ".css": "css",
    ".json": "json",
    ".toml": "toml",
    ".md": "markdown",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".conf": "config",
    ".ini": "ini",
    ".sh": "shell",
}


def find_readme(root_folder: str) -> str:
    """
    Find a README file in the root folder with any common README extension.

    Args:
        root_folder (str): The root folder to search in.

    Returns:
        str: The path to the README file if found, else an empty string.
    """
    for filename in os.listdir(root_folder):
        if filename.lower().startswith("readme"):
            return os.path.join(root_folder, filename)
    return ""


def flatten_repo(root_folder: str, output_folder: str | None = None):
    """
    Flatten the source repository into a single markdown file.

    Args:
        root_folder (str): The root folder of the repository.
        output_folder (str | None): The folder to save the flattened file. Defaults to the current working directory.
    """
    repo_name = os.path.basename(os.path.normpath(root_folder))
    if output_folder is None:
        output_folder = os.getcwd()
    flattened_file_path = os.path.join(output_folder, f"{repo_name}.flat.md")

    readme_path = find_readme(root_folder)

    with open(flattened_file_path, "w") as flat_file:
        flat_file.write(f"# Contents of {repo_name} source tree\n\n")

        # Handle README file
        if readme_path:
            with open(readme_path, "r") as readme_file:
                readme_contents = readme_file.read()
                flat_file.write("## README\n\n")
                flat_file.write("```markdown\n")
                flat_file.write(readme_contents)
                flat_file.write("\n```\n\n")
                print(f"Included README file: {readme_path}")

        # Recursively walk the repo and collect relevant files
        for dirpath, dirnames, filenames in os.walk(root_folder):
            # Exclude hidden directories
            dirnames[:] = [d for d in dirnames if not d.startswith(".")]

            for filename in filenames:
                if filename.startswith("."):
                    continue  # Exclude hidden files
                extension = os.path.splitext(filename)[1]
                full_path = os.path.join(dirpath, filename)
                if extension in FILE_TYPES and full_path != readme_path:
                    with open(full_path, "r") as file:
                        file_contents = file.read()
                        relative_path = os.path.relpath(full_path, root_folder)
                        flat_file.write(f"## File: {relative_path}\n\n")
                        flat_file.write(f"```{FILE_TYPES[extension]}\n")
                        flat_file.write(file_contents)
                        flat_file.write("\n```\n\n")
                        print(f"Included file: {full_path}")

    print(f"Flattening complete. Output saved to {flattened_file_path}")
