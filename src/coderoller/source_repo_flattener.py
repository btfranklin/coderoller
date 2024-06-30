import os
import pathspec

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


def load_gitignore_patterns(root_folder: str) -> list[str]:
    """
    Load .gitignore patterns from the root folder.

    Args:
        root_folder (str): The root folder of the repository.

    Returns:
        list[str]: A list of patterns from the .gitignore file.
    """
    gitignore_path = os.path.join(root_folder, ".gitignore")
    if os.path.exists(gitignore_path):
        with open(gitignore_path, "r") as f:
            patterns = f.read().splitlines()
        return patterns
    return []


def should_include_path(file_path: str, spec: pathspec.PathSpec) -> bool:
    """
    Determine if a path should be included based on .gitignore patterns and specific exclusions.

    Args:
        file_path (str): The path of the file or directory to check.
        spec (pathspec.PathSpec): The PathSpec object containing the .gitignore patterns.

    Returns:
        bool: True if the path should be included, False otherwise.
    """
    # Specific exclusions
    specific_exclusions = [
        "build",
        "dist",
        "node_modules",
        "__pycache__",
        ".flat.md",
        ".lock",
        "-lock.json",
        ".hidden",
    ]

    # Check if the file or directory matches specific exclusions
    if any(exclusion in file_path for exclusion in specific_exclusions):
        return False

    # Check against .gitignore patterns
    return not spec.match_file(file_path)


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


def flatten_repo(
    root_folder: str, output_folder: str = None, repo_name: str = None
) -> None:
    """
    Flatten the source repository into a single markdown file.

    Args:
        root_folder (str): The root folder of the repository.
        output_folder (str | None): The folder to save the flattened file. Defaults to the current working directory.
        repo_name (str | None): The name of the repository.
    """
    if repo_name is None:
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

        # Collect patterns from .gitignore
        gitignore_patterns = load_gitignore_patterns(root_folder)
        spec = pathspec.PathSpec.from_lines(
            pathspec.patterns.GitWildMatchPattern, gitignore_patterns
        )

        # Recursively walk the repo and collect relevant files
        for dirpath, dirnames, filenames in os.walk(root_folder):
            # Exclude directories and files matching .gitignore patterns and specific exclusions
            dirnames[:] = [
                d
                for d in dirnames
                if should_include_path(os.path.join(dirpath, d), spec)
            ]
            filenames[:] = [
                f
                for f in filenames
                if should_include_path(os.path.join(dirpath, f), spec)
            ]

            for filename in filenames:
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
