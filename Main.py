# DirectoryTreePlugin/Main.py
import sublime
import sublime_plugin
import os
import subprocess
import sys

class GenerateTreeCommand(sublime_plugin.WindowCommand):
    def run(self):
        # 顯示輸入對話框讓用戶輸入資料夾路徑
        self.window.show_input_panel(
            "輸入資料夾路徑:",
            "",
            self.on_done,
            None,
            None
        )
    
    def on_done(self, path):
        """處理用戶輸入的路徑"""
        if not path:
            return
        
        # 檢查路徑是否存在
        if not os.path.exists(path):
            sublime.error_message("路徑不存在: " + path)
            return
        
        if not os.path.isdir(path):
            sublime.error_message("不是資料夾: " + path)
            return
        
        # 生成目錄樹
        tree_output = self.generate_tree(path)
        
        # 在新的視窗中顯示結果
        self.show_tree_output(tree_output, path)
    
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
            # 過濾隱藏文件
            entries = [e for e in entries if not e.startswith('.')]
            
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
    
    def show_tree_output(self, tree_output, original_path):
        """在新的視窗中顯示目錄樹結果"""
        # 創建新的視窗
        new_view = self.window.new_file()
        new_view.set_name("Tree - " + os.path.basename(original_path))
        new_view.set_scratch(True)  # 設置為臨時文件，不需要保存
        
        # 插入目錄樹內容
        header = "目錄樹 - " + original_path + "\n" + "=" * 50 + "\n\n"
        content = header + tree_output
        
        new_view.run_command('insert', {
            'characters': content
        })
        
        # 設置語法高亮為純文本
        new_view.set_syntax_file("Packages/Text/Plain text.tmLanguage")


class GenerateCurrentDirTreeCommand(sublime_plugin.WindowCommand):
    """為當前文件所在目錄生成目錄樹的命令"""
    def run(self):
        view = self.window.active_view()
        if view:
            file_path = view.file_name()
            if file_path:
                dir_path = os.path.dirname(file_path)
                # 直接使用當前文件所在目錄
                tree_cmd = GenerateTreeCommand(self.window)
                tree_output = tree_cmd.generate_tree(dir_path)
                tree_cmd.show_tree_output(tree_output, dir_path)
            else:
                sublime.error_message("請先儲存文件或開啟一個已儲存的文件")
        else:
            sublime.error_message("沒有活動的文件")
    
    def is_enabled(self):
        """檢查命令是否可用"""
        view = self.window.active_view()
        return view and view.file_name() is not None