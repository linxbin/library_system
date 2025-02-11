class Book:
    """图书类"""
    def __init__(self, isbn, title, author, total_copies):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.total_copies = total_copies
        self.available_copies = total_copies
        self.borrow_records = []

    def to_dict(self):
        """将对象转换为字典（用于JSON序列化）"""
        return {
            "isbn": self.isbn,
            "title": self.title,
            "author": self.author,
            "total_copies": self.total_copies,
            "available_copies": self.available_copies,
            "borrow_records": [
                {
                    "user": record["user"],
                    "borrow_date": record["borrow_date"].isoformat(),
                    "return_date": record["return_date"].isoformat() if record["return_date"] else None
                }
                for record in self.borrow_records
            ]
        }
