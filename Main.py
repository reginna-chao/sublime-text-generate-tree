import sublime
import sublime_plugin

class ExampleCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # 在這裡撰寫你的套件功能
        self.view.insert(edit, 0, "Hello, Sublime Text!")

class ExampleEventListener(sublime_plugin.EventListener):
    def on_load(self, view):
        # 當文件載入時觸發
        sublime.message_dialog("文件已載入！")