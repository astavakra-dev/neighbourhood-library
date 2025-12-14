import pytest
from datetime import datetime
from server.data.repository import BookRepository, MemberRepository, BorrowRepository
from server.errors.exceptions import NotFoundError, ReturnError, BorrowError

@pytest.mark.asyncio
async def test_add_book(async_session):
    repo = BookRepository(async_session)
    book = await repo.add_book("Clean Code", "Robert C. Martin", 2008)
    assert book.id is not None
    assert book.title == "Clean Code"
    assert book.available_copies == 1

@pytest.mark.asyncio
async def test_update_book(async_session):
    repo = BookRepository(async_session)
    book = await repo.add_book("Old Title", "Author", 2000)
    updated = await repo.update_book(book.id, "New Title", "Author", 2001)
    assert updated.title == "New Title"
    assert updated.published_year == 2001

    # Non-existent book should raise NotFoundError
    with pytest.raises(NotFoundError):
        await repo.update_book(999, "X", "Y", 2020)

@pytest.mark.asyncio
async def test_add_member(async_session):
    repo = MemberRepository(async_session)
    member = await repo.add_member("Alice", "1234567890", "alice@example.com")
    assert member.id is not None
    assert member.name == "Alice"

@pytest.mark.asyncio
async def test_borrow_book(async_session):
    book_repo = BookRepository(async_session)
    member_repo = MemberRepository(async_session)
    borrow_repo = BorrowRepository(async_session)

    book = await book_repo.add_book("Domain-Driven Design", "Eric Evans", 2003)
    member = await member_repo.add_member("Bob", "9876543210", "bob@example.com")

    record = await borrow_repo.borrow_book(book.id, member.id)
    assert record.record_id is not None
    assert record.book_id == book.id
    assert record.member_id == member.id
    assert isinstance(record.due_date, datetime)

    # Borrow again should fail (no available copies)
    with pytest.raises(BorrowError):
        await borrow_repo.borrow_book(book.id, member.id)

@pytest.mark.asyncio
async def test_return_book(async_session):
    book_repo = BookRepository(async_session)
    member_repo = MemberRepository(async_session)
    borrow_repo = BorrowRepository(async_session)

    book = await book_repo.add_book("Refactoring", "Martin Fowler", 1999)
    member = await member_repo.add_member("Charlie", "1112223333", "charlie@example.com")

    # Borrow first
    record = await borrow_repo.borrow_book(book.id, member.id)
    assert record.return_date is None

    # Return book
    returned = await borrow_repo.return_book(book.id, member.id)
    assert returned.return_date is not None
    assert book.available_copies == 1  # back to full

    # Returning again should fail
    with pytest.raises(ReturnError):
        await borrow_repo.return_book(book.id, member.id)

@pytest.mark.asyncio
async def test_list_borrowed_books(async_session):
    book_repo = BookRepository(async_session)
    member_repo = MemberRepository(async_session)
    borrow_repo = BorrowRepository(async_session)

    book1 = await book_repo.add_book("Patterns of Enterprise Application Architecture", "Martin Fowler", 2002)
    book2 = await book_repo.add_book("The Pragmatic Programmer", "Andrew Hunt", 1999)
    member = await member_repo.add_member("Dana", "4445556666", "dana@example.com")

    # Borrow both books
    await borrow_repo.borrow_book(book1.id, member.id)
    await borrow_repo.borrow_book(book2.id, member.id)

    books = await borrow_repo.list_borrowed_books(member.id)
    titles = [b.title for b in books]
    assert "Patterns of Enterprise Application Architecture" in titles
    assert "The Pragmatic Programmer" in titles

    # Return one book
    await borrow_repo.return_book(book1.id, member.id)

    books_after_return = await borrow_repo.list_borrowed_books(member.id)
    titles_after = [b.title for b in books_after_return]
    assert "The Pragmatic Programmer" in titles_after
    assert "Patterns of Enterprise Application Architecture" not in titles_after