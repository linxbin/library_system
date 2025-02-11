

import hashlib


class User:
    """用户类"""
    def __init__(self, username, password, role="user"):
        self.username = username
        self.password_hash = self._hash_password(password)
        self.role = role  # user/admin
        self.borrowed_books = []  # 当前借阅
        self.borrow_history = []  # 历史记录

    def _hash_password(self, password):
        """密码哈希处理"""
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self, password):
        """验证密码"""
        return self.password_hash == self._hash_password(password)

    def to_dict(self):
        """序列化用户数据"""
        return {
            "username": self.username,
            "password_hash": self.password_hash,
            "role": self.role,
            "borrowed_books": [
                {
                    "isbn": book["isbn"],
                    "title": book["title"],
                    "borrow_date": book["borrow_date"].isoformat(),
                    "return_date": book["return_date"].isoformat() if book["return_date"] else None
                }
                for book in self.borrowed_books
            ],
            "borrow_history": [
                {
                    "isbn": record["isbn"],
                    "title": record["title"],
                    "borrow_date": record["borrow_date"].isoformat(),
                    "return_date": record["return_date"].isoformat() if record["return_date"] else None
                }
                for record in self.borrow_history
            ]
        }