from sqlalchemy.future import select
from datetime import datetime, timedelta

from server.models.book import Book
from server.models.member import Member
from server.models.borrow_record import BorrowRecord
from server.errors.exceptions import NotFoundError, ValidationError, BorrowError, ReturnError, AlreadyExistsError


class BookRepository:
    def __init__(self, session):
        self.session = session

    async def add_book(self, title, author, year):
        if not title or not author or year <= 0:
            raise ValidationError("Invalid book details provided")

        book = Book(title=title, author=author, published_year=year,
                    total_copies=1, available_copies=1)
        self.session.add(book)
        await self.session.commit()
        await self.session.refresh(book)
        return book

    async def update_book(self, book_id, title, author, year):
        result = await self.session.execute(select(Book).where(Book.id == book_id))
        book = result.scalar_one_or_none()
        if not book:
            raise NotFoundError(f"Book with id {book_id} not found")

        if not title or not author or year <= 0:
            raise ValidationError("Invalid book details provided")

        book.title = title
        book.author = author
        book.published_year = year
        await self.session.commit()
        return book

    async def get_book(self, book_id):
        result = await self.session.execute(select(Book).where(Book.id == book_id))
        book = result.scalar_one_or_none()
        if not book:
            raise NotFoundError(f"Book with id {book_id} not found")
        return book


class MemberRepository:
    def __init__(self, session):
        self.session = session

    async def add_member(self, name, contact_no, email):
        if not name or not contact_no or not email:
            raise ValidationError("Invalid member details provided")

        # Check for duplicates
        existing = await self.session.execute(select(Member).where(Member.email == email))
        if existing.scalar_one_or_none():
            raise AlreadyExistsError(f"Member with email {email} already exists")

        member = Member(name=name, contact_no=contact_no, email=email)
        self.session.add(member)
        await self.session.commit()
        await self.session.refresh(member)
        return member

    async def get_member(self, member_id):
        result = await self.session.execute(select(Member).where(Member.id == member_id))
        member = result.scalar_one_or_none()
        if not member:
            raise NotFoundError(f"Member with id {member_id} not found")
        return member


class BorrowRepository:
    def __init__(self, session):
        self.session = session

    async def borrow_book(self, book_id, member_id, due_date=None):
        # Fetch book
        result = await self.session.execute(select(Book).where(Book.id == book_id))
        book = result.scalar_one_or_none()
        if not book:
            raise NotFoundError(f"Book with id {book_id} not found")

        if book.available_copies <= 0:
            raise BorrowError("No available copies to borrow")

        # Default due date
        if not due_date:
            due_date = datetime.now() + timedelta(days=14)

        record = BorrowRecord(book_id=book_id, member_id=member_id, due_date=due_date)
        self.session.add(record)

        # Update available copies
        book.available_copies -= 1

        await self.session.commit()
        await self.session.refresh(record)
        return record

    async def return_book(self, book_id, member_id):
        result = await self.session.execute(
            select(BorrowRecord).where(
                BorrowRecord.book_id == book_id,
                BorrowRecord.member_id == member_id,
                BorrowRecord.return_date.is_(None)
            )
        )
        record = result.scalar_one_or_none()
        if not record:
            raise ReturnError("No active borrow record found")

        record.return_date = datetime.now()

        # Update available copies
        book_result = await self.session.execute(select(Book).where(Book.id == book_id))
        book = book_result.scalar_one_or_none()
        if book:
            book.available_copies = min(book.available_copies + 1, book.total_copies)

        await self.session.commit()
        return record

    async def list_borrowed_books(self, member_id):
        result = await self.session.execute(
            select(Book).join(BorrowRecord).where(
                BorrowRecord.member_id == member_id,
                BorrowRecord.return_date.is_(None)
            )
        )
        books = result.scalars().all()
        if not books:
            raise NotFoundError(f"No borrowed books found for member {member_id}")
        return books