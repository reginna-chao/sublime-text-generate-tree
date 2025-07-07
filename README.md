# Generate Tree Plugin for Sublime Text

A powerful Sublime Text plugin for generating and displaying directory tree structures in the editor. Supports smart ignoring of unnecessary folders, helping you focus on important project files.

## ✨ Features

- 🌳 **Generate Directory Tree**: Simulates the output format of Windows `tree /a /f` command
- 🚫 **Smart Ignore**: Automatically ignores common folders like `node_modules`, `.git`, `__pycache__`, etc.
- ⚙️ **Custom Configuration**: Supports custom ignore lists
- 📂 **Two Modes**: Input any path or use the current file's directory

## 📋 Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Ignore List Settings](#ignore-list-settings)
- [Key Bindings](#key-bindings)
- [Configuration File](#configuration-file)
- [Example Output](#example-output)
- [FAQ](#faq)

## 🚀 Installation

### Method 1: Manual Installation

1. Open Sublime Text
2. Press `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (Mac) to open the command palette
3. Type "Browse Packages" and select it
4. In the opened folder, create a new folder: `GenerateTree`
5. Place the following files into this folder:
  - `GenTree.py`
  - `ignore_config.py`
  - `Default.sublime-commands`
  - `Main.sublime-menu`
  - `Default.sublime-keymap`
6. Restart Sublime Text

### File Structure
```
GenerateTree/
├── GenTree.py                     # Main code
├── ignore_config.py            # Ignore list configuration
├── Default.sublime-commands    # Command palette configuration
├── Main.sublime-menu           # Menu configuration
├── Default.sublime-keymap      # Key bindings configuration
└── README.md                   # Documentation
```

## 📖 Usage

### Command Palette

1. Press `Ctrl+Shift+P` to open the command palette
2. Type "GenTree" to see the following options:
  - **GenTree: Generate Directory Tree** - Input any folder path
  - **GenTree: Generate Tree for Current Directory** - Use the current file's directory

### Menu Operations

- **Tools → GenTree → Generate Directory Tree**
- **Tools → GenTree → Generate Tree for Current Directory**

### Workflow

1. After executing the command, choose an ignore mode:
  - **Web Development** - For frontend/fullstack projects
  - **Python Development** - For Python projects
  - **Java Development** - For Java projects
  - **Minimal** - Ignores only basic folders
  - **All Common** - Ignores all common folders
  - **Custom Ignore List** - Manually set folders to ignore
  - **Do Not Ignore Any Folder** - Show complete structure

2. The directory tree will be displayed in a new window, including:
  - Directory path
  - Selected ignore mode
  - List of ignored folders
  - Complete directory tree structure

## 🚫 Ignore List Settings

### Default Ignored Folders

The plugin includes the following commonly ignored folders:

#### Development Related
- `node_modules`, `bower_components` (Node.js/JavaScript)
- `__pycache__`, `venv`, `.venv` (Python)
- `target`, `bin` (Java/Maven)
- `vendor` (PHP/Go)

#### Version Control
- `.git`, `.svn`, `.hg`

#### IDE and Editors
- `.idea`, `.vscode`, `.vs`
- `.sublime-project`, `.sublime-workspace`

#### System Files
- `.DS_Store`, `Thumbs.db`

#### Cache and Build
- `.cache`, `.sass-cache`
- `dist`, `build`, `tmp`

### Preset Combinations

| Preset | Use Case | Main Ignored Items |
|--------|----------|-------------------|
| **Web Development** | Frontend/Fullstack | node_modules, dist, .sass-cache, coverage |
| **Python Development** | Python projects | __pycache__, venv, .pytest_cache, build |
| **Java Development** | Java projects | target, bin, .idea, .vscode |
| **Minimal** | Minimal ignore | node_modules, .git, __pycache__, dist |
| **All Common** | Full ignore | All common folders |

## ⌨️ Key Bindings

- `Ctrl+Alt+T` - Generate directory tree (input path)
- `Ctrl+Alt+Shift+T` - Generate tree for current directory

> 💡 You can customize key bindings in `Default.sublime-keymap`

## ⚙️ Configuration File

### Custom Ignore List

Edit `ignore_config.py` to customize the ignore list:

```python
# Add new folders to ignore
DEFAULT_IGNORE_FOLDERS.add('my_custom_folder')

# Create a new preset combination
PRESET_COMBINATIONS['my_preset'] = {
   'node_modules', '.git', 'custom_folder'
}
```

### Custom Preset Combinations

```python
# Create a preset for a specific framework
PRESET_COMBINATIONS['react_development'] = {
   'node_modules', 'build', 'public', '.git', 
   'coverage', '.env.local'
}
```

## 📋 Example Output

```
Directory Tree - F:\MyProject
==================================================
Ignore Mode: Web Development
Ignored Folders: .git, .sass-cache, coverage, dist, node_modules
--------------------------------------------------

MyProject
+---src
|   +---components
|   |   +---Header.js
|   |   +---Footer.js
|   +---styles
|   |   +---main.scss
|   |   +---variables.scss
|   +---utils
|       +---helpers.js
+---public
|   +---index.html
|   +---favicon.ico
+---package.json
+---README.md
+---.gitignore
```

## ❓ FAQ

### Q: Plugin fails to load?
**A:** Make sure the file structure is correct, all files are in the `GenerateTree` folder, and restart Sublime Text.

### Q: Can't see plugin commands in the command palette?
**A:** 
1. Check if the `Default.sublime-commands` file exists
2. Ensure the JSON syntax is correct
3. Press `Ctrl+\`` to open the console and check for error messages

### Q: Want to add new folders to ignore?
**A:** Edit the `ignore_config.py` file and add new items to `DEFAULT_IGNORE_FOLDERS`.

### Q: Directory tree format is incorrect?
**A:** The plugin will use the system's `tree` command if available, otherwise it uses a built-in implementation. Make sure there are no special characters in the path.

### Q: How to ignore specific file extensions?
**A:** Add extensions to `DEFAULT_IGNORE_EXTENSIONS` in `ignore_config.py`, or use the custom ignore list feature.

### Q: Can I save commonly used ignore settings?
**A:** Yes, add custom preset combinations in `PRESET_COMBINATIONS` in `ignore_config.py`.

## 🔧 Development Info

- **Version**: 1.0.0
- **Compatibility**: Sublime Text 3 & 4
- **License**: MIT License
- **Language**: Python 3

