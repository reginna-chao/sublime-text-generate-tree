# DirectoryTreePlugin/ignore_config.py
"""
目錄樹插件的忽略清單配置
"""

# 預設忽略資料夾清單
DEFAULT_IGNORE_FOLDERS = {
    # Node.js / JavaScript
    'node_modules',
    'bower_components',
    'jspm_packages',
    '.npm',
    '.yarn',
    
    # 版本控制系統
    '.git',
    '.svn',
    '.hg',
    '.bzr',
    'CVS',
    
    # Python
    '__pycache__',
    '.pytest_cache',
    '.coverage',
    '.tox',
    '.nox',
    'venv',
    'env',
    '.venv',
    '.env',
    'site-packages',
    'eggs',
    '*.egg-info',
    'build',
    'dist',
    '.pyc',
    
    # IDE 和編輯器
    '.idea',
    '.vscode',
    '.vs',
    '.sublime-project',
    '.sublime-workspace',
    '*.sublime-*',
    '.atom',
    
    # 作業系統
    '.DS_Store',
    'Thumbs.db',
    'Desktop.ini',
    '$RECYCLE.BIN',
    
    # 編譯和建置
    'target',  # Maven/Gradle (Java)
    'bin',
    'obj',
    'out',
    'Release',
    'Debug',
    'x64',
    'x86',
    
    # 快取目錄
    '.cache',
    '.sass-cache',
    '.less-cache',
    'cache',
    'tmp',
    'temp',
    '.tmp',
    '.temp',
    
    # 測試覆蓋率
    'coverage',
    '.nyc_output',
    'htmlcov',
    
    # 日誌
    'logs',
    '*.log',
    'log',
    
    # Ruby
    '.bundle',
    'vendor/bundle',
    
    # PHP
    'vendor',
    
    # Rust
    'target',
    'Cargo.lock',
    
    # Go
    'vendor',
    
    # Docker
    '.dockerignore',
    
    # 其他常見忽略項目
    'backup',
    'backups',
    '.bak',
    '*.bak',
    '*.orig',
    '*.swp',
    '*.swo',
    '*~',
}

# 常用的預設組合
PRESET_COMBINATIONS = {
    'web_development': {
        'node_modules', 'bower_components', '.git', '.sass-cache', 
        'dist', 'build', '.cache', 'coverage'
    },
    
    'python_development': {
        '__pycache__', '.pytest_cache', 'venv', '.venv', 'env', '.env',
        '.git', 'build', 'dist', '*.egg-info', '.coverage'
    },
    
    'java_development': {
        'target', 'bin', '.git', '.idea', '.vscode', 'build'
    },
    
    'minimal': {
        'node_modules', '.git', '__pycache__', 'dist', 'build'
    },
    
    'all_common': DEFAULT_IGNORE_FOLDERS
}

# 檔案擴展名忽略清單（可選）
DEFAULT_IGNORE_EXTENSIONS = {
    '.log',
    '.tmp',
    '.cache',
    '.bak',
    '.orig',
    '.swp',
    '.swo',
    '.pyc',
    '.pyo',
    '.class'
}

def get_ignore_list(preset_name='all_common'):
    """
    根據預設名稱取得忽略清單
    
    Args:
        preset_name (str): 預設組合名稱
        
    Returns:
        set: 忽略資料夾集合
    """
    return PRESET_COMBINATIONS.get(preset_name, DEFAULT_IGNORE_FOLDERS).copy()

def get_available_presets():
    """
    取得所有可用的預設組合
    
    Returns:
        list: 預設組合清單
    """
    return list(PRESET_COMBINATIONS.keys())

def add_custom_ignore(ignore_set, custom_folders):
    """
    添加自定義忽略資料夾
    
    Args:
        ignore_set (set): 現有忽略集合
        custom_folders (list or str): 要添加的資料夾
        
    Returns:
        set: 更新後的忽略集合
    """
    if isinstance(custom_folders, str):
        custom_folders = [custom_folders]
    
    for folder in custom_folders:
        if folder:
            ignore_set.add(folder.strip())
    
    return ignore_set