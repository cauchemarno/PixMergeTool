import os

from PySide6.QtWidgets import QMessageBox, QWidget


EXTENSION_MAP = {
    '.c': 'c',
    '.cpp': 'cpp',
    '.cs': 'csharp',
    '.css': 'css',
    '.dart': 'dart',
    '.elixir': 'elixir',
    '.ex': 'elixir',
    '.exs': 'elixir',
    '.go': 'go',
    '.h': 'c',
    '.htm': 'html',
    '.html': 'html',
    '.java': 'java',
    '.js': 'javascript',
    '.json': 'json',
    '.kt': 'kotlin',
    '.less': 'less',
    '.markdown': 'markdown',
    '.md': 'markdown',
    '.php': 'php',
    '.pl': 'perl',
    '.py': 'python',
    '.r': 'r',
    '.rb': 'ruby',
    '.rs': 'rust',
    '.scss': 'scss',
    '.sh': 'bash',
    '.sql': 'sql',
    '.swift': 'swift',
    '.ts': 'typescript',
    '.tsx': 'typescriptreact',
    '.xml': 'xml',
    '.yaml': 'yaml',
    '.yml': 'yaml'
}


def is_text_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            f.read(1024)
        return True
    except (UnicodeDecodeError, Exception):
        return False


class FileProcessor:
    def __init__(self, ignored_dirs=None):
        if ignored_dirs is not None:
            self.ignored_dirs = set(ignored_dirs)
        else:
            self.ignored_dirs = {
                ".idea", ".vscode", ".venv", ".env", "venv", "env", "__pycache__",
                ".mypy_cache", ".pytest_cache", ".git", "node_modules", "dist",
                "build", "target", "out", ".next", ".expo", ".turbo", ".cache", ".coverage"
            }

    def _is_ignored(self, item_name):
        return item_name in self.ignored_dirs or item_name.lower().endswith("egg-info")

    def process_file(self, file_path, settings):
        if os.path.isdir(file_path):
            return self.generate_ascii_tree(file_path, show_ignored=settings.get('show_ignored', True))

        if not is_text_file(file_path):
            return None

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            QMessageBox.critical(QWidget(), "Error", f"Error reading file {file_path}: {e}")
            return None

        if settings.get('path_style') == 'filename':
            display_name = os.path.basename(file_path)
        elif settings.get('path_style') == 'full':
            display_name = file_path
        elif settings.get('path_style') == 'relative':
            project_root = settings.get('project_root')
            if project_root:
                normalized_path = os.path.normpath(file_path)
                path_parts = normalized_path.split(os.sep)
                if project_root in path_parts:
                    idx = path_parts.index(project_root)
                    display_name = os.sep.join(path_parts[idx:])
                else:
                    display_name = file_path
            else:
                display_name = file_path
        else:
            display_name = os.path.basename(file_path)

        format_type = settings.get('format', 'markdown')
        if format_type == 'markdown':
            _, ext = os.path.splitext(file_path)
            lang = EXTENSION_MAP.get(ext.lower(), '') if settings.get('add_language', True) else ''
            code_block = f"```{lang}\n{content}\n```" if lang else f"```\n{content}\n```"
            return f"{display_name}:\n{code_block}"
        else:
            return f"<{display_name}>\n{content}\n</{display_name}>"

    def generate_ascii_tree(self, folder_path, show_ignored=True, max_depth=None):
        lines = []
        folder_name = os.path.basename(os.path.normpath(folder_path))
        lines.append(folder_name)
        self._build_tree(folder_path, "", lines, show_ignored, current_depth=0, max_depth=max_depth)
        return "\n".join(lines)

    def _build_tree(self, folder, prefix, lines, show_ignored=True, current_depth=0, max_depth=None):
        if max_depth is not None and current_depth >= max_depth:
            return

        try:
            items = os.listdir(folder)
        except Exception as e:
            QMessageBox.critical(QWidget(), "Error", f"Error accessing folder {folder}: {e}")
            return

        items = sorted(items, key=lambda x: (not os.path.isdir(os.path.join(folder, x)), x.lower()))
        for index, item in enumerate(items):
            full_path = os.path.join(folder, item)
            connector = "└── " if index == len(items) - 1 else "├── "
            new_prefix = prefix + ("    " if index == len(items) - 1 else "│   ")

            if os.path.isdir(full_path):
                if self._is_ignored(item):
                    if show_ignored:
                        lines.append(prefix + connector + item)
                        lines.append(new_prefix + "...")
                    continue

            lines.append(prefix + connector + item)
            if os.path.isdir(full_path):
                self._build_tree(full_path, new_prefix, lines, show_ignored, current_depth + 1, max_depth)
