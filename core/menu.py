"""
core/menu.py - 菜单系统模块
"""
from typing import Dict, List, Callable, Any

class MenuManager:
    """菜单管理系统"""
    
    def __init__(self, system: Any):
        self.system = system
        self.menu_stack: List[str] = []
        self.menu_config = self._load_menu_config()
        
    def _load_menu_config(self) -> Dict:
        """加载菜单配置"""
        return {
            "root": {
                "title": "\n=== 图书馆管理系统 ===",
                "options": [
                    ("1", "用户登录", "login"),
                    ("2", "用户注册", "register"),
                    ("3", "退出系统", "exit")
                ]
            },
            "user_main": {
                "title": lambda: f"\n=== 欢迎，{self.system.current_user.username} ===",
                "options": lambda: [
                    ("1", "图书搜索", "search"),
                    ("2", "借阅图书", "borrow"),
                    ("3", "归还图书", "return"),
                    ("4", "我的借阅", "my_books"),
                    *self._admin_options(),
                    ("0", "退出登录", "logout")
                ]
            },
            "admin_main": {
                "title": "\n=== 管理员面板 ===",
                "options": [
                    ("1", "添加图书", "add_book"),
                    ("2", "用户管理", "user_mgmt"),
                    ("0", "返回主菜单", "back")
                ]
            },
            "user_management": {
                "title": "\n=== 用户管理 ===",
                "options": [
                    ("1", "查看所有用户", "list_users"),
                    ("2", "重置用户密码", "reset_pw"),
                    ("0", "返回上级", "back")
                ]
            }
        }
    
    def _admin_options(self) -> List:
        """生成管理员专属选项"""
        if self.system.current_user and self.system.current_user.role == "admin":
            return [("5", "管理员功能", "admin_menu")]
        return []
    
    def show_current_menu(self) -> Dict:
        """显示当前菜单并返回选项映射"""
        current_menu = self.menu_stack[-1]
        config = self.menu_config[current_menu]
        
        # 动态生成标题
        title = config["title"]
        if callable(title):
            print(title())
        else:
            print(title)
            
        # 动态生成选项
        options = config["options"]
        if callable(options):
            options = options()
            
        # 打印选项并生成映射
        option_map = {}
        for i, (num, text, action) in enumerate(options, 1):
            print(f"{num}. {text}")
            option_map[str(num)] = action

        option_map["0"] = options[-1][2]  # 最后一项为0键
        return option_map

    @property
    def current_menu_name(self) -> str:
        """获取当前菜单名称"""
        return self.menu_stack[-1] if self.menu_stack else "root"
    
    def start(self):
        """初始化菜单"""
        if not self.menu_stack:
            self.menu_stack.append("root")