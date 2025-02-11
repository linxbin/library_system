"""
main.py - 程序入口
"""
import traceback
from core.system import LibrarySystem, Book
from core.menu import MenuManager

def main():
    system = LibrarySystem()

    if "admin" not in system.users:
        system.register_user("admin", "admin123", "admin")

    menu = MenuManager(system)
    menu.start()
    
    while True:
        # 显示菜单
        option_map = menu.show_current_menu()
        
        # 获取用户输入
        choice = input("请输入选项: ").strip()
        action = option_map.get(choice, "invalid")

        current_menu = menu.current_menu_name
        # 登录状态检查
        if current_menu != "root" and not system.current_user:
            current_menu = "root"
            continue
            
        # 处理业务逻辑
        try:  
            if action == "login":
                username = input("用户名: ")
                password = input("密码: ")
                if system.login(username, password):
                    menu.menu_stack.append("user_main")
                
            elif action == "register":
                username = input("新用户名: ")
                password = input("密码: ")
                system.register_user(username, password)
                system.save_data()

            elif action == "exit":
                print("谢谢使用！")
                break

            elif action == "logout":
                system.logout()
                menu.menu_stack = ["root"]        

            elif action == "user_mgmt":
                menu.menu_stack.append("user_management")
            
            elif action == "admin_menu":
                menu.menu_stack.append("admin_main")

            elif action == "back":
                if len(menu.menu_stack) > 1:
                    menu.menu_stack.pop()

            # 用户管理子菜单处理
            elif current_menu == "user_management":
                if action == "list_users":
                    for user in system.users.values():
                        print(f"{user.username} ({user.role})")
                        
                elif action == "reset_pw":
                    username = input("要重置的用户名: ")
                    if username in system.users:
                        new_pass = input("输入新密码: ")
                        system.users[username].password_hash = \
                            system.users[username]._hash_password(new_pass)
                        print("密码已重置")
                        system.save_data()
            
            # 管理员主菜单处理
            elif current_menu == "admin_main":
                if action == "add_book":
                    isbn = input("ISBN: ")
                    title = input("书名: ")
                    author = input("作者: ")
                    total_copies = int(input("总数量: "))
                    new_book = Book(isbn, title, author, total_copies)
                    system.add_book(new_book)
                    system.save_data()

            # 普通用户菜单处理
            elif current_menu == "user_main":
                if action == "search":
                    keyword = input("输入搜索关键词: ")
                    results = system.search_book(keyword)
                    for book in results:
                        print(f"[{book.isbn}] {book.title} - {book.author}")
                        
                elif action == "borrow":
                    isbn = input("输入ISBN: ")
                    system.borrow_book(isbn)
                    system.save_data()
                    
                elif action == "return":
                    isbn = input("输入ISBN: ")
                    system.return_book(isbn)
                    system.save_data()
                    
                elif action == "my_books":
                    print("\n当前借阅：")
                    for book in system.current_user.borrowed_books:
                        print(f"- {book['title']} (ISBN: {book['isbn']})")
                    print("\n历史记录：")
                    for record in system.current_user.borrow_history:
                        print(f"- {record['title']} 于 {record['return_date']} 归还")

        except Exception as e:
            print(f"操作失败: {str(e)}")
            traceback.print_exc()

         # 管理员特殊菜单衔接
        if system.current_user and system.current_user.role == "admin":
            if current_menu == "user_main" and "admin_main" not in menu.menu_stack:
                menu.menu_stack.insert(-1, "admin_main")

if __name__ == "__main__":
    main()