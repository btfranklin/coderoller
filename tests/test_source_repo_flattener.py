import os
import tempfile
import shutil
from unittest.mock import patch
from git import Repo
from coderoller.source_repo_flattener import flatten_repo
from coderoller.flatten_repo import main


def test_flatten_repo():
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a mock repository structure
        os.makedirs(os.path.join(temp_dir, "src"))

        readme_content = "# This is the README"
        with open(os.path.join(temp_dir, "README.md"), "w") as f:
            f.write(readme_content)

        python_content = 'print("Hello, World!")'
        with open(os.path.join(temp_dir, "src", "main.py"), "w") as f:
            f.write(python_content)

        json_content = '{"key": "value"}'
        with open(os.path.join(temp_dir, "config.json"), "w") as f:
            f.write(json_content)

        output_dir = tempfile.mkdtemp()
        flatten_repo(temp_dir, output_dir)

        # Check if the flattened file is created
        flattened_file_path = os.path.join(
            output_dir, f"{os.path.basename(temp_dir)}.flat.md"
        )
        assert os.path.exists(flattened_file_path), "Flattened file was not created"

        with open(flattened_file_path, "r") as f:
            flattened_content = f.read()

        # Check if the README content is included
        assert "## README" in flattened_content, "README section is missing"
        assert (
            "```markdown" in flattened_content
        ), "README content is not properly formatted"
        assert readme_content in flattened_content, "README content is incorrect"

        # Check if the Python file content is included
        assert (
            "## File: src/main.py" in flattened_content
        ), "Python file section is missing"
        assert (
            "```python" in flattened_content
        ), "Python content is not properly formatted"
        assert python_content in flattened_content, "Python content is incorrect"

        # Check if the JSON file content is included
        assert (
            "## File: config.json" in flattened_content
        ), "JSON file section is missing"
        assert "```json" in flattened_content, "JSON content is not properly formatted"
        assert json_content in flattened_content, "JSON content is incorrect"


def test_hidden_files_and_directories():
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a hidden directory and file
        os.makedirs(os.path.join(temp_dir, ".hidden_dir"))
        with open(os.path.join(temp_dir, ".hidden_file.py"), "w") as f:
            f.write('print("This should not be included")')

        output_dir = tempfile.mkdtemp()
        flatten_repo(temp_dir, output_dir)

        # Check if the flattened file is created
        flattened_file_path = os.path.join(
            output_dir, f"{os.path.basename(temp_dir)}.flat.md"
        )
        assert os.path.exists(flattened_file_path), "Flattened file was not created"

        with open(flattened_file_path, "r") as f:
            flattened_content = f.read()

        # Check if hidden files and directories are excluded
        assert (
            ".hidden_dir" not in flattened_content
        ), "Hidden directory should be excluded"
        assert (
            ".hidden_file.py" not in flattened_content
        ), "Hidden file should be excluded"


@patch.object(Repo, "clone_from")
def test_flatten_repo_from_git(mock_clone_from):
    with tempfile.TemporaryDirectory() as temp_dir:
        # Mock the clone_from method to copy a local repository structure instead
        def mock_clone(repo_url, to_path):
            shutil.copytree(temp_dir, to_path, dirs_exist_ok=True)

        mock_clone_from.side_effect = mock_clone

        # Create a mock repository structure
        os.makedirs(os.path.join(temp_dir, "src"))

        readme_content = "# This is the README"
        with open(os.path.join(temp_dir, "README.md"), "w") as f:
            f.write(readme_content)

        python_content = 'print("Hello, World!")'
        with open(os.path.join(temp_dir, "src", "main.py"), "w") as f:
            f.write(python_content)

        json_content = '{"key": "value"}'
        with open(os.path.join(temp_dir, "config.json"), "w") as f:
            f.write(json_content)

        # Test the CLI with a mock GitHub URL
        with patch(
            "sys.argv", ["coderoller-flatten-repo", "https://github.com/mock/repo.git"]
        ):
            main()

        # Check if the flattened file is created
        flattened_file_path = os.path.join(os.getcwd(), "repo.flat.md")
        assert os.path.exists(flattened_file_path), "Flattened file was not created"

        with open(flattened_file_path, "r") as f:
            flattened_content = f.read()

        # Check if the README content is included
        assert "## README" in flattened_content, "README section is missing"
        assert (
            "```markdown" in flattened_content
        ), "README content is not properly formatted"
        assert readme_content in flattened_content, "README content is incorrect"

        # Check if the Python file content is included
        assert (
            "## File: src/main.py" in flattened_content
        ), "Python file section is missing"
        assert (
            "```python" in flattened_content
        ), "Python content is not properly formatted"
        assert python_content in flattened_content, "Python content is incorrect"

        # Check if the JSON file content is included
        assert (
            "## File: config.json" in flattened_content
        ), "JSON file section is missing"
        assert "```json" in flattened_content, "JSON content is not properly formatted"
        assert json_content in flattened_content, "JSON content is incorrect"

        # Clean up the flattened file
        os.remove(flattened_file_path)
