# 🧩 Pix Merge Tool

**PixMergeTool** is a tool that helps you merge multiple text/code files and generate visual folder structures — perfect for preparing content for Large Language Models (LLMs) like ChatGPT, Claude, DeepSeek, Grok, Gemini etc. or for organizing your own projects.

## 🚀 Installation

### ✅ A ready-to-use installer for Windows:
👉 [Download PixMergeTool Installer](https://github.com/cauchemarno/PixMergeTool/releases)

## ✨ Features

- 📂 **Text & Code File Merger**
  - Combine multiple files into a single document.
  - Add automatic Markdown or XML code blocks with optional language detection.
  - Optionally include a custom prompt field before the content.
- 🗂️ **ASCII Folder Tree Generator**
  - Drop a folder to instantly generate its ASCII directory tree.
  - Configure ignored folders:
    - Collapse them with ellipsis (`...`).
    - Hide them entirely.
- 🔀 **File Path Display Modes**
  - Choose how file paths are displayed:
    - Filename only
    - Full path
    - Relative to a custom project root
- 📎 **Drag & Drop Support**
  - Drop multiple files or folders into the window.
  - Append new content or overwrite the current view.
- 💾 **Persistent Settings**
  - Automatically saves:
    - Window position and size
    - User preferences (format, display mode, ignored folders)
    - Field content (optional)
- 🧠 **Custom Prompt Editor**
  - Toggle a prompt input field.
  - Supports rich text and Markdown highlighting.
- 📤 **Output Options**
  - Copy the result to clipboard.
  - Export as `.txt`.
- 🔢 **Live Character Counter**
  - Displays the total number of characters (prompt + merged content).
  - **TODO**: Add token counter.

## 🖥 Screenshot

![Screenshot1](https://i.imgur.com/dWogsnk.png)

## 🧪 Run from Source

1. Clone the repository:

```bash
git clone https://github.com/cauchemarno/PixMergeTool.git
cd PixMergeTool
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python main.py
```

## 🛠 Build Your Own Executable
You can build PixMergeTool using PyInstaller.
```bash
pip install pyinstaller
```

### 📦 One-folder build (recommended)
```bash
pyinstaller main.py --name PixMergeTool --noconsole --icon=resources/icons/icon.ico
```

🧍 Optional: One-file build
```bash
pyinstaller main.py --name PixWatermark --onefile --noconsole --icon=resources/icons/icon.ico
```

## 💬 Feedback & Contributions
Feel free to report issues or suggest features on GitHub.

## 📜 License

This project is licensed under the [GPL-3.0](https://www.gnu.org/licenses/gpl-3.0.html) License.

App logo is an emoji graphic from [Twemoji](https://github.com/twitter/twemoji) by Twitter(X), used under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
