from sqlalchemy.future import select
from server.models.book import Book
from server.errors.exceptions import NotFoundError

class BookRepository:
    def __init__(self, session):
        self.session = session

    async def add_book(self, title, author, year):
        book = Book(title=title, author=author, published_year=year)
        self.session.add(book)
        await self.session.commit()
        await self.session.refresh(book)
        return book

    async def update_book(self, book_id, title, author, year):
        result = await self.session.execute(select(Book).where(Book.id == book_id))
        book = result.scalar_one_or_none()
        if not book:
            raise NotFoundError("Book not found")
        book.title = title
        book.author = author
        book.published_year = year
        await self.session.commit()
        return book