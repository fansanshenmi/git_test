from abc import ABC, abstractmethod
import json


# =========================
# 书籍类
# =========================
class Book:

    def __init__(self, book_id, title, author, total_num):
        self.title = title
        self.book_id = book_id
        self.author = author
        self.total_num = total_num

        # 当前可借数量
        self.__available_num = total_num

    # 借书
    def borrow_book(self):

        if self.__available_num > 0:
            self.__available_num -= 1
            return True

        else:
            return False

    # 还书
    def return_book(self):

        self.__available_num += 1
        return True

    # 获取当前可借数量
    def get_available_num(self):

        return self.__available_num

print("GIT练习")
print("test")
# =========================
# 会员抽象类
# =========================
class Member(ABC):

    def __init__(self, member_id, name, password):

        self.member_id = member_id
        self.name = name

        # 私有密码
        self.__password = password

        # 已借阅图书
        self.borrowed_books = []

    # 借书
    def borrow_book(self, book):

        # 判断会员借阅数量是否超过限制
        if len(self.borrowed_books) >= self.max_borrow_num():

            print("借阅数量超过限制")
            return False

        # 判断图书是否还有库存
        if book.borrow_book():

            self.borrowed_books.append(book)

            print(f"{self.name}借阅了《{book.title}》")

            return True

        else:

            print(f"《{book.title}》不可借阅")

            return False

    # 还书
    def return_book(self, book):

        # 判断当前会员是否借过这本书
        if book in self.borrowed_books:

            book.return_book()

            self.borrowed_books.remove(book)

            print(f"{self.name}归还了《{book.title}》")

            return True

        else:

            print(f"{self.name}没有借阅《{book.title}》")

            return False

    # 获取当前会员已经借阅的图书
    def get_borrowed_books(self):

        return self.borrowed_books

    # 获取密码
    def get_password(self):

        return self.__password

    # 借阅数量限制
    # 在子类中实现
    @abstractmethod
    def max_borrow_num(self):

        pass


# =========================
# 普通会员类
# =========================
class NormalMember(Member):

    # 普通会员最多借3本
    def max_borrow_num(self):

        return 3


# =========================
# VIP会员类
# =========================
class VIPMember(Member):

    def __init__(
        self,
        member_id,
        name,
        password,
        VIP_level
    ):

        # 调用父类构造方法
        super().__init__(
            member_id,
            name,
            password
        )

        # VIP等级
        self.VIP_level = VIP_level

    # VIP最多借 6 + VIP等级 本
    def max_borrow_num(self):

        return 6 + self.VIP_level


# =========================
# 图书馆管理系统
# =========================
class Library:

    def __init__(self):

        # 存储所有图书
        self.books = {}

        # 存储所有会员
        self.members = {}

        # 当前登录会员
        self.current_member: Member | None = None

        # 加载会员数据
        self.load_members_data()

        # 加载图书数据
        self.load_books_data()

    # =========================
    # 加载会员数据
    # =========================
    def load_members_data(self):

        # 从JSON文件加载会员数据
        with open(
            "resource/json_data/member.json",
            "r",
            encoding="utf-8"
        ) as f:

            members_data = json.load(f)

            # 遍历会员数据
            for member in members_data:

                # 普通会员
                if member["member_type"] == "normal":

                    normal_member = NormalMember(
                        member["member_id"],
                        member["name"],
                        member["password"]
                    )

                    # 添加到会员字典
                    self.members[
                        member["member_id"]
                    ] = normal_member

                # VIP会员
                elif member["member_type"] == "vip":

                    vip_member = VIPMember(
                        member["member_id"],
                        member["name"],
                        member["password"],
                        member["VIP_level"]
                    )

                    # 添加到会员字典
                    self.members[
                        member["member_id"]
                    ] = vip_member

        print("会员数据加载完成")

    # =========================
    # 加载书籍数据
    # =========================
    def load_books_data(self):

        # 从JSON文件加载图书数据
        with open(
            "resource/json_data/book.json",
            "r",
            encoding="utf-8"
        ) as f:

            books_data = json.load(f)

            # 遍历图书数据
            for book_data in books_data:

                book = Book(
                    book_data["book_id"],
                    book_data["title"],
                    book_data["author"],
                    book_data["total_num"]
                )

                # 将书籍添加到字典
                self.books[
                    book_data["book_id"]
                ] = book

        print("书籍数据加载完成")
    def login(self):
        while True:
            print("【登录】")
            member_id = input("请输入会员ID :")
            password = input("请输入密码：")
            if member_id not in self.members:
                print("会员不存在")
                continue
            else:
                member = self.members[member_id]
            if member.get_password() != password:
                print("密码错误")
                continue
            else:
                self.current_member = member
                print(f"欢迎{member.name}登录")
                return True
    def borrow_book(self):
            #展示当前图书馆的列表
        for book in self.books.values():
            print(f"书籍ID:{book.book_id} 书名:{book.title} 作者:{book.author} 总数:{book.total_num} 剩余:{book.get_available_num()}")

        book_id = input("请输入书籍ID：")
        if book_id not in self.books:
            print("书籍不存在")
            return False
        self.current_member.borrow_book(self.books[book_id])
    def return_book(self):
        #展示当前会员借阅列表
        borrow_books = self.current_member.get_borrowed_books()
        print("【当前借阅列表】")
        for book in borrow_books:
            print(f"书籍ID:{book.book_id} 书名:{book.title} 作者:{book.author}")
        book_id = input("请输入书籍ID：")
        if book_id not in self.books:
            print("书籍不存在")
            return False
        self.current_member.return_book(self.books[book_id])
    def view_borrowed_books(self):
        borrow_books = self.current_member.get_borrowed_books()
        if len(borrow_books) == 0:
            print("当前没有借阅书籍")
            return False
        print("【当前借阅列表】")
        for book in borrow_books:
            print(f"书籍ID:{book.book_id} 书名:{book.title} 作者:{book.author}")
        return True

    def run(self):
        if self.login():
            while True:
                print("【图书馆管理系统】")
                print("1.借阅图书")
                print("2.归还图书")
                print("3.查看借阅图书")
                print("4.退出")
                choice = input("请输入操作编号：")
                if choice == "1":
                    self.borrow_book()
                elif choice == "2":
                    self.return_book()
                elif choice == "3":
                    self.view_borrowed_books()
                elif choice == "4":
                    print("退出系统")
                    break
                else:
                    print("输入错误")
                    continue
            
# =========================
# 程序入口
# =========================
if __name__ == "__main__":

    # 创建图书馆系统
    library = Library()

    library.run()