import os
import sys
import shutil
import tempfile
from git import Repo
from coderoller.source_repo_flattener import flatten_repo


def get_repo_name(input_path: str) -> str:
    """
    Infer the repository name from the input path or URL.

    Args:
        input_path (str): The path or URL of the repository.

    Returns:
        str: The inferred repository name.
    """
    if (
        input_path.startswith("http://")
        or input_path.startswith("https://")
        or input_path.startswith("git@")
    ):
        repo_name = os.path.basename(input_path).replace(".git", "")
    else:
        repo_name = os.path.basename(os.path.normpath(input_path))
    return repo_name


def main():
    if len(sys.argv) != 2:
        print("Usage: coderoller-flatten-repo <root_folder_or_git_url>")
        sys.exit(1)

    input_path = sys.argv[1]
    repo_name = get_repo_name(input_path)

    # Check if the input is a Git URL
    if (
        input_path.startswith("http://")
        or input_path.startswith("https://")
        or input_path.startswith("git@")
    ):
        # Clone the repository to a temporary directory
        temp_dir = tempfile.mkdtemp()
        try:
            print(f"Cloning repository from {input_path} to {temp_dir}")
            Repo.clone_from(input_path, temp_dir)
            flatten_repo(temp_dir, repo_name=repo_name)
        finally:
            # Clean up the temporary directory
            shutil.rmtree(temp_dir)
            print(f"Deleted temporary directory {temp_dir}")
    else:
        flatten_repo(input_path, repo_name=repo_name)


if __name__ == "__main__":
    main()
