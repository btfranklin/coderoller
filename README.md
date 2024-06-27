# Coderoller

`Coderoller` is a Python utility that flattens a source code repository into a single markdown file. This tool collects all relevant source and configuration files, including Python, JavaScript, TypeScript, HTML, CSS, JSON, and more, and compiles them into a markdown document. The flattened file provides an organized overview of the repository's contents, making it easy to use in conjunction with LLMs. Simply copy the contents of the flattened file and paste it into your LLM chat context. The flattened form is also great for API-based uses of LLMs in automated workflows.

## Features

- **Flattens source code repositories** into a single markdown file.
- **Supports multiple file types** including `.py`, `.js`, `.jsx`, `.ts`, `.tsx`, `.swift`, `.go`, `.java`, `.c`, `.cpp`, `.h`, `.hpp`, `.cs`, `.lua`, `.rb`, `.php`, `.pl`, `.html`, `.css`, `.json`, `.toml`, `.md`, `.yaml`, `.yml`, `.conf`, `.ini`, and `.sh`.
- **Automatically includes README** files if present, placing it at the start of the flattened file.
- **Excludes hidden files and directories** (those starting with a dot).

## Installation

Coderoller requires Python 3.12 or later and PDM for package management.

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/coderoller.git
    cd coderoller
    ```

2. Install dependencies using PDM:

    ```bash
    pdm install
    ```

## Usage

To flatten a source repository, use the `coderoller-flatten-repo` script.

```bash
pdm run coderoller-flatten-repo /path/to/root/folder
```

This command will create a markdown file named `reponame.flat.md` in the current working directory, containing the flattened contents of the repository.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
