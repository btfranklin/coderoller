import sys
from coderoller.source_repo_flattener import flatten_repo


def main():
    if len(sys.argv) != 2:
        print("Usage: coderoller-flatten-repo <root_folder>")
        sys.exit(1)

    root_folder = sys.argv[1]
    flatten_repo(root_folder)


if __name__ == "__main__":
    main()
