from server.data.repository import BookRepository, MemberRepository, BorrowRepository
from server.errors.exceptions import ValidationError

class LibraryService:
    def __init__(self, session):
        self.book_repo = BookRepository(session)
        self.member_repo = MemberRepository(session)
        self.borrow_repo = BorrowRepository(session)

    async def add_book(self, title, author, year):
        if not title.strip():
            raise ValidationError("Title is required")
        if not author.strip():
            raise ValidationError("Author is required")
        if year < 0:
            raise ValidationError("Year must be positive")
        return await self.book_repo.add_book(title, author, year)

    async def update_book(self, book_id, title, author, year):
        return await self.book_repo.update_book(book_id, title, author, year)

    async def add_member(self, name, contact_no, email):
        if not name.strip():
            raise ValidationError("Name is required")
        if not contact_no.strip():
            raise ValidationError("Contact number is required")
        if not email.strip():
            raise ValidationError("Email is required")
        return await self.member_repo.add_member(name, contact_no, email)

    async def borrow_book(self, book_id, member_id, due_date):
        return await self.borrow_repo.borrow_book(book_id, member_id, due_date)

    async def return_book(self, book_id, member_id):
        return await self.borrow_repo.return_book(book_id, member_id)

    async def list_borrowed_books(self, member_id):
        return await self.borrow_repo.list_borrowed_books(member_id)