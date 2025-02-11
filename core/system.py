"""
core/system.py - 系统核心逻辑
"""
import json
from datetime import datetime, timedelta
import os
from typing import Dict, Any

from core.book import Book
from core.user import User

class LibrarySystem:
    """系统主类"""
    def __init__(self):
        self.books = {}  # ISBN: Book对象
        self.users = {}  # 用户名: User对象
        self.current_user = None  # 当前登录用户
        self.load_data()

    def add_book(self, isbn, title, author, total_copies):
        """添加新书"""
        if isbn in self.books:
            print("错误：ISBN已存在！")
            return False
        new_book = Book(isbn, title, author, total_copies)
        self.books[isbn] = new_book
        print("图书添加成功！")
        return True

    def search_book(self, keyword):
        """搜索图书（支持ISBN/标题/作者）"""
        results = []
        for isbn, book in self.books.items():
            if (keyword.lower() in book.title.lower() or
                keyword.lower() in book.author.lower() or
                keyword == isbn):
                results.append(book)
        return results
    
    def delete_book(self, isbn):
        """删除图书"""
        if isbn not in self.books:
            print("错误：图书不存在！")
            return False
        del self.books[isbn]
        print("图书删除成功！")
        return True

    def edit_book(self, old_isbn, new_isbn=None, title=None, author=None, total_copies=None):
        """修改图书"""
        if old_isbn not in self.books:
            print("错误：图书不存在！")
            return False
        book = self.books[old_isbn]
        if new_isbn and new_isbn != old_isbn:
            if new_isbn in self.books:
                print("错误：新的 ISBN 已存在！")
                return False
            self.books[new_isbn] = book
            del self.books[old_isbn]
            book.isbn = new_isbn
        if title:
            book.title = title
        if author:
            book.author = author
        if total_copies is not None:
            book.total_copies = total_copies
            book.available_copies = total_copies - len([r for r in book.borrow_records if not r["return_date"]])
        print("图书修改成功！")
        return True

    def list_books(self):
        """查看全部图书"""
        if not self.books:
            print("当前没有图书。")
            return
        for isbn, book in self.books.items():
            print(f"ISBN: {isbn}, 书名: {book.title}, 作者: {book.author}, 总数量: {book.total_copies}, 可借数量: {book.available_copies}")

    def borrow_book(self, isbn):
        """借阅图书（关联用户）"""
        if not self.current_user:
            print("请先登录！")
            return False

        book = self.books.get(isbn)
        if not book:
            print("错误：图书不存在！")
            return False
        
        if book.available_copies <= 0:
            print("错误：该书已全部借出！")
            return False

        borrow_date = datetime.now()
        return_date = borrow_date + timedelta(days=30)
        
        # 添加借阅记录到图书
        book.borrow_records.append({
            "user": self.current_user.username,
            "borrow_date": borrow_date,
            "return_date": None
        })
        book.available_copies -= 1
        
        # 添加记录到用户
        self.current_user.borrowed_books.append({
            "isbn": isbn,
            "title": book.title,
            "borrow_date": borrow_date,
            "return_date": None
        })
        
        print(f"借阅成功！应归还日期：{return_date.strftime('%Y-%m-%d')}")
        return True

    def return_book(self, isbn):
        """归还图书（关联用户）"""
        if not self.current_user:
            print("请先登录！")
            return False

        book = self.books.get(isbn)
        if not book:
            print("错误：图书不存在！")
            return False

        # 更新图书记录
        for record in book.borrow_records:
            if record["user"] == self.current_user.username and not record["return_date"]:
                record["return_date"] = datetime.now()
                book.available_copies += 1
                
                # 计算逾期
                delta = datetime.now() - record["borrow_date"]
                if delta.days > 30:
                    overdue_days = delta.days - 30
                    print(f"逾期{overdue_days}天，需缴纳罚金{overdue_days * 0.5}元")
                
                # 更新用户记录
                for user_record in self.current_user.borrowed_books:
                    if user_record["isbn"] == isbn and not user_record["return_date"]:
                        user_record["return_date"] = datetime.now()
                        self.current_user.borrow_history.append(user_record.copy())
                        self.current_user.borrowed_books.remove(user_record)
                        break
                return True
        
        print("错误：未找到借阅记录！")
        return False
    

    # 新增用户管理方法：
    def register_user(self, username, password, role="user"):
        """用户注册"""
        if username in self.users:
            print("用户名已存在！")
            return False
            
        if len(password) < 6:
            print("密码至少需要6位！")
            return False
            
        self.users[username] = User(username, password, role)
        print("注册成功！")
        return True

    def login(self, username, password):
        """用户登录"""
        user = self.users.get(username)
        if not user:
            print("用户不存在！")
            return False
            
        if user.verify_password(password):
            self.current_user = user
            print(f"欢迎回来，{username}！")
            return True
        else:
            print("密码错误！")
            return False
        
    def logout(self):
        """退出登录"""
        self.current_user = None
        print("已退出登录")

    def save_data(self):
        try:
            # 保存图书数据
            with open(os.path.join("data","library_data.json"), "w") as f:
                book_data = {isbn: book.to_dict() for isbn, book in self.books.items()}
                json.dump(book_data, f, indent=2)
            
            # 保存用户数据
            with open(os.path.join("data","user_data.json"), "w") as f:
                user_data = {user.username: user.to_dict() for user in self.users.values()}
                json.dump(user_data, f, indent=2)
        except IOError as e:
            print(f"保存数据失败：{str(e)}")

    def load_data(self):
        """从文件加载数据"""
        try:

            # 加载图书数据
            with open(os.path.join("data","library_data.json"), "r") as f:
                data = json.load(f)
                for isbn, book_data in data.items():
                    book = Book(
                        isbn=book_data["isbn"],
                        title=book_data["title"],
                        author=book_data["author"],
                        total_copies=book_data["total_copies"]
                    )
                    book.available_copies = book_data["available_copies"]
                    book.borrow_records = [
                        {
                            "user": r["user"],
                            "borrow_date": datetime.fromisoformat(r["borrow_date"]),
                            "return_date": datetime.fromisoformat(r["return_date"]) if r["return_date"] else None
                        }
                        for r in book_data["borrow_records"]
                    ]
                    self.books[isbn] = book

            # 加载用户数据
            with open(os.path.join("data","user_data.json"), "r") as f:
                user_data = json.load(f)
                for username, data in user_data.items():
                    user = User(
                        username=data["username"],
                        password="",  # 密码不加载
                        role=data["role"]
                    )
                    user.password_hash = data["password_hash"]
                    user.borrowed_books = data["borrowed_books"]
                    user.borrow_history = data["borrow_history"]
                    self.users[username] = user
        except FileNotFoundError:
            print("初始化新数据库...")
        except Exception as e:
            print(f"加载数据失败：{str(e)}")