# DirectoryTreePlugin/Main.py
import sublime
import sublime_plugin
import os
import subprocess
import sys

# 導入忽略清單配置
try:
    from .ignore_config import (
        DEFAULT_IGNORE_FOLDERS, 
        PRESET_COMBINATIONS, 
        get_ignore_list, 
        get_available_presets,
        add_custom_ignore
    )
except ImportError:
    # 如果導入失敗，使用基本的預設值
    DEFAULT_IGNORE_FOLDERS = {'node_modules', '.git', '__pycache__', 'dist', 'build'}
    PRESET_COMBINATIONS = {'all_common': DEFAULT_IGNORE_FOLDERS}
    
    def get_ignore_list(preset_name='all_common'):
        return DEFAULT_IGNORE_FOLDERS.copy()
    
    def get_available_presets():
        return ['all_common']
    
    def add_custom_ignore(ignore_set, custom_folders):
        if isinstance(custom_folders, str):
            custom_folders = [custom_folders]
        for folder in custom_folders:
            if folder:
                ignore_set.add(folder.strip())
        return ignore_set

class GenerateTreeCommand(sublime_plugin.WindowCommand):
    def __init__(self, window):
        super().__init__(window)
        # 從配置文件載入預設忽略清單
        self.default_ignore_folders = get_ignore_list('all_common')
        self.available_presets = get_available_presets()
    
    def run(self):
        # 顯示輸入對話框讓用戶輸入資料夾路徑
        self.window.show_input_panel(
            "輸入資料夾路徑:",
            "",
            self.on_path_done,
            None,
            None
        )
    
    def on_path_done(self, path):
        """處理用戶輸入的路徑後，詢問是否要使用忽略清單"""
        if not path:
            return
        
        # 檢查路徑是否存在
        if not os.path.exists(path):
            sublime.error_message("路徑不存在: " + path)
            return
        
        if not os.path.isdir(path):
            sublime.error_message("不是資料夾: " + path)
            return
        
        self.target_path = path
        
        # 建立選項清單
        options = []
        
        # 添加預設組合選項
        preset_descriptions = {
            'web_development': 'Web 開發 (忽略 node_modules, dist, .sass-cache 等)',
            'python_development': 'Python 開發 (忽略 __pycache__, venv, .pytest_cache 等)',
            'java_development': 'Java 開發 (忽略 target, bin, .idea 等)',
            'minimal': '最小忽略清單 (只忽略最常見的資料夾)',
            'all_common': '完整忽略清單 (忽略所有常見資料夾)'
        }
        
        for preset in self.available_presets:
            description = preset_descriptions.get(preset, '預設組合: ' + preset)
            options.append([preset.replace('_', ' ').title(), description])
        
        # 添加自定義和無忽略選項
        options.extend([
            ["自定義忽略清單", "手動輸入要忽略的資料夾名稱"],
            ["不忽略任何資料夾", "顯示所有資料夾和文件"]
        ])
        
        self.window.show_quick_panel(options, self.on_ignore_option_selected)
    
    def on_ignore_option_selected(self, selected_index):
        """處理忽略選項選擇"""
        if selected_index == -1:  # 用戶取消
            return
        
        preset_count = len(self.available_presets)
        
        if selected_index < preset_count:  # 選擇了預設組合
            preset_name = self.available_presets[selected_index]
            self.ignore_folders = get_ignore_list(preset_name)
            self.selected_preset = preset_name
            self.generate_and_show_tree()
        elif selected_index == preset_count:  # 自定義忽略清單
            default_list = ", ".join(sorted(self.default_ignore_folders))
            self.window.show_input_panel(
                "輸入要忽略的資料夾名稱 (用逗號分隔):",
                default_list,
                self.on_custom_ignore_done,
                None,
                None
            )
        else:  # 不忽略任何資料夾
            self.ignore_folders = set()
            self.selected_preset = "無忽略"
            self.generate_and_show_tree()
    
    def on_custom_ignore_done(self, ignore_text):
        """處理自定義忽略清單"""
        self.ignore_folders = set()
        if ignore_text:
            # 使用配置文件的函數來處理自定義忽略清單
            folders_list = [folder.strip() for folder in ignore_text.split(',') if folder.strip()]
            self.ignore_folders = add_custom_ignore(self.ignore_folders, folders_list)
        
        self.selected_preset = "自定義"
        self.generate_and_show_tree()
    
    def generate_and_show_tree(self):
        """生成並顯示目錄樹"""
        # 生成目錄樹
        tree_output = self.generate_tree(self.target_path)
        
        # 在新的視窗中顯示結果
        self.show_tree_output(tree_output, self.target_path)
    
    def on_done(self, path):
        """保留原有的簡單介面（向後相容）"""
        if not path:
            return
        
        # 檢查路徑是否存在
        if not os.path.exists(path):
            sublime.error_message("路徑不存在: " + path)
            return
        
        if not os.path.isdir(path):
            sublime.error_message("不是資料夾: " + path)
            return
        
        self.target_path = path
        self.ignore_folders = set()  # 不忽略任何資料夾
        self.generate_and_show_tree()
    
    def generate_tree(self, path):
        """生成目錄樹結構"""
        try:
            # 檢查系統類型並執行相應命令
            if sys.platform == "win32":
                # Windows 系統使用 tree 命令
                result = subprocess.run(
                    ["tree", "/A", path],
                    capture_output=True,
                    text=True,
                    encoding='utf-8',
                    shell=True
                )
                if result.returncode == 0:
                    return result.stdout
            else:
                # Unix/Linux/macOS 系統使用 tree 命令（如果有的話）
                if self.command_exists("tree"):
                    result = subprocess.run(
                        ["tree", "-a", path],
                        capture_output=True,
                        text=True
                    )
                    if result.returncode == 0:
                        return result.stdout
        except Exception as e:
            pass
        
        # 如果上面的方法都失敗，使用自定義實現
        return self.custom_tree(path, "", True)
    
    def command_exists(self, command):
        """檢查命令是否存在"""
        try:
            subprocess.run([command, "--version"], capture_output=True)
            return True
        except FileNotFoundError:
            return False
    
    def custom_tree(self, root_path, prefix="", is_root=True):
        """自定義目錄樹生成 - 精確模擬 Windows tree /a /f 格式"""
        try:
            if is_root:
                # 根目錄顯示
                tree_output = os.path.basename(root_path) + "\n"
                return tree_output + self._build_tree_recursive(root_path, "")
            else:
                return self._build_tree_recursive(root_path, prefix)
        except Exception as e:
            return "生成目錄樹時發生錯誤: " + str(e) + "\n"
    
    def _build_tree_recursive(self, path, prefix):
        """遞歸建立目錄樹"""
        tree_output = ""
        
        try:
            entries = sorted(os.listdir(path))

            # 智能過濾：只忽略真正的"垃圾"隱藏檔案，保留有用的配置檔案
            system_hidden = {'.DS_Store', '.Thumbs.db', '.directory', '._*'}  # 系統生成的檔案
            
            filtered_entries = []
            for e in entries:
                # 檢查是否在自定義忽略清單中
                if self._should_ignore(e):
                    continue
                
                # 檢查是否為系統隱藏檔案（真正需要隱藏的）
                if any(e.startswith(pattern.replace('*', '')) for pattern in system_hidden if '*' in pattern) or e in system_hidden:
                    continue
                    
                filtered_entries.append(e)
            
            entries = filtered_entries

            # 分離目錄和文件，目錄在前
            dirs = []
            files = []
            for entry in entries:
                entry_path = os.path.join(path, entry)
                if os.path.isdir(entry_path):
                    dirs.append(entry)
                else:
                    files.append(entry)
            
            all_entries = dirs + files
            
            for i, entry in enumerate(all_entries):
                is_last = i == len(all_entries) - 1
                entry_path = os.path.join(path, entry)
                
                # Windows tree 格式的連接符
                if is_last:
                    connector = "+---"
                    new_prefix = prefix + "    "
                else:
                    connector = "+---"
                    new_prefix = prefix + "|   "
                
                tree_output += prefix + connector + entry + "\n"
                
                # 如果是目錄，遞歸處理
                if os.path.isdir(entry_path):
                    try:
                        tree_output += self._build_tree_recursive(entry_path, new_prefix)
                    except PermissionError:
                        tree_output += new_prefix + "[權限不足]\n"
                        
        except PermissionError:
            tree_output += prefix + "[權限不足]\n"
        except Exception as e:
            tree_output += prefix + "錯誤: " + str(e) + "\n"
            
        return tree_output
    
    def _should_ignore(self, folder_name):
        """檢查是否應該忽略此資料夾"""
        return folder_name in getattr(self, 'ignore_folders', set())
    
    def show_tree_output(self, tree_output, original_path):
        """在新的視窗中顯示目錄樹結果"""
        # 創建新的視窗
        new_view = self.window.new_file()
        new_view.set_name("Tree - " + os.path.basename(original_path))
        new_view.set_scratch(True)  # 設置為臨時文件，不需要保存
        
        # 準備標題資訊
        header = "目錄樹 - " + original_path + "\n" + "=" * 50 + "\n"
        
        # 顯示使用的預設組合
        if hasattr(self, 'selected_preset'):
            header += "忽略模式: " + self.selected_preset + "\n"
        
        # 如果有忽略資料夾，顯示忽略清單
        if hasattr(self, 'ignore_folders') and self.ignore_folders:
            # 限制顯示的忽略清單長度，避免過長
            ignore_list = sorted(self.ignore_folders)
            if len(ignore_list) > 10:
                display_list = ignore_list[:10] + ["... 等 " + str(len(ignore_list)) + " 項"]
            else:
                display_list = ignore_list
            header += "忽略的資料夾: " + ", ".join(display_list) + "\n"
            header += "-" * 50 + "\n"
        
        header += "\n"
        content = header + tree_output
        
        new_view.run_command('insert', {
            'characters': content
        })
        
        # 設置語法高亮為純文本
        new_view.set_syntax_file("Packages/Text/Plain text.tmLanguage")


class GenerateCurrentDirTreeCommand(sublime_plugin.WindowCommand):
    """為當前文件所在目錄生成目錄樹的命令"""
    def __init__(self, window):
        super().__init__(window)
        # 從配置文件載入預設忽略清單
        self.default_ignore_folders = get_ignore_list('all_common')
        self.available_presets = get_available_presets()
    
    def run(self):
        view = self.window.active_view()
        if view:
            file_path = view.file_name()
            if file_path:
                self.target_path = os.path.dirname(file_path)
                
                # 建立選項清單（與主命令相同）
                options = []
                
                preset_descriptions = {
                    'web_development': 'Web 開發 (忽略 node_modules, dist, .sass-cache 等)',
                    'python_development': 'Python 開發 (忽略 __pycache__, venv, .pytest_cache 等)',
                    'java_development': 'Java 開發 (忽略 target, bin, .idea 等)',
                    'minimal': '最小忽略清單 (只忽略最常見的資料夾)',
                    'all_common': '完整忽略清單 (忽略所有常見資料夾)'
                }
                
                for preset in self.available_presets:
                    description = preset_descriptions.get(preset, '預設組合: ' + preset)
                    options.append([preset.replace('_', ' ').title(), description])
                
                options.extend([
                    ["自定義忽略清單", "手動輸入要忽略的資料夾名稱"],
                    ["顯示全部", "包含所有檔案和隱藏檔案（僅忽略系統檔案）"]
                ])
                
                self.window.show_quick_panel(options, self.on_ignore_option_selected)
            else:
                sublime.error_message("請先儲存文件或開啟一個已儲存的文件")
        else:
            sublime.error_message("沒有活動的文件")
    
    def on_ignore_option_selected(self, selected_index):
        """處理忽略選項選擇"""
        if selected_index == -1:  # 用戶取消
            return
        
        preset_count = len(self.available_presets)
        
        if selected_index < preset_count:  # 選擇了預設組合
            preset_name = self.available_presets[selected_index]
            self.ignore_folders = get_ignore_list(preset_name)
            self.selected_preset = preset_name
            self.generate_and_show_tree()
        elif selected_index == preset_count:  # 自定義忽略清單
            default_list = ", ".join(sorted(self.default_ignore_folders))
            self.window.show_input_panel(
                "輸入要忽略的資料夾名稱 (用逗號分隔):",
                default_list,
                self.on_custom_ignore_done,
                None,
                None
            )
        else:  # 不忽略任何資料夾
            self.ignore_folders = set()
            self.selected_preset = "無忽略"
            self.generate_and_show_tree()
    
    def on_custom_ignore_done(self, ignore_text):
        """處理自定義忽略清單"""
        self.ignore_folders = set()
        if ignore_text:
            folders_list = [folder.strip() for folder in ignore_text.split(',') if folder.strip()]
            self.ignore_folders = add_custom_ignore(self.ignore_folders, folders_list)
        
        self.selected_preset = "自定義"
        self.generate_and_show_tree()
    
    def generate_and_show_tree(self):
        """生成並顯示目錄樹"""
        # 使用主命令的方法
        tree_cmd = GenerateTreeCommand(self.window)
        tree_cmd.ignore_folders = self.ignore_folders
        tree_cmd.selected_preset = self.selected_preset
        tree_output = tree_cmd.generate_tree(self.target_path)
        tree_cmd.show_tree_output(tree_output, self.target_path)
    
    def is_enabled(self):
        """檢查命令是否可用"""
        view = self.window.active_view()
        return view and view.file_name() is not None