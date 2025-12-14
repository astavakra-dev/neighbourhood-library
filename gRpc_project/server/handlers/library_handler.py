import grpc
from proto import library_service_pb2, library_service_pb2_grpc
from server.data.repository import BookRepository, MemberRepository, BorrowRepository
from server.errors.exceptions import (
    ValidationError,
    NotFoundError,
    AlreadyExistsError,
    BorrowError,
    ReturnError,
)

class LibraryHandler(library_service_pb2_grpc.LibraryServiceServicer):
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def AddBook(self, request, context):
        async with self.session_factory() as session:
            repo = BookRepository(session)
            try:
                book = await repo.add_book(request.title, request.author, request.published_year)
                return library_service_pb2.BookResponse(
                    success=True, message="Book added successfully", id=book.id
                )
            except ValidationError as ve:
                context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(ve))
            except Exception as e:
                context.abort(grpc.StatusCode.INTERNAL, str(e))

    async def UpdateBook(self, request, context):
        async with self.session_factory() as session:
            repo = BookRepository(session)
            try:
                book = await repo.update_book(request.id, request.title, request.author, request.published_year)
                return library_service_pb2.BookResponse(
                    success=True, message="Book updated successfully", id=book.id
                )
            except NotFoundError as nf:
                context.abort(grpc.StatusCode.NOT_FOUND, str(nf))
            except ValidationError as ve:
                context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(ve))
            except Exception as e:
                context.abort(grpc.StatusCode.INTERNAL, str(e))

    async def AddMember(self, request, context):
        async with self.session_factory() as session:
            repo = MemberRepository(session)
            try:
                member = await repo.add_member(request.name, request.contact_no, request.email)
                return library_service_pb2.MemberResponse(
                    success=True, message="Member added successfully", id=member.id
                )
            except ValidationError as ve:
                context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(ve))
            except AlreadyExistsError as ae:
                context.abort(grpc.StatusCode.ALREADY_EXISTS, str(ae))
            except Exception as e:
                context.abort(grpc.StatusCode.INTERNAL, str(e))

    async def BorrowBook(self, request, context):
        async with self.session_factory() as session:
            repo = BorrowRepository(session)
            try:
                record = await repo.borrow_book(request.book_id, request.member_id, request.due_date)
                return library_service_pb2.BorrowResponse(
                    record_id=record.record_id, status="Borrowed"
                )
            except NotFoundError as nf:
                context.abort(grpc.StatusCode.NOT_FOUND, str(nf))
            except BorrowError as be:
                context.abort(grpc.StatusCode.FAILED_PRECONDITION, str(be))
            except Exception as e:
                context.abort(grpc.StatusCode.INTERNAL, str(e))

    async def ReturnBook(self, request, context):
        async with self.session_factory() as session:
            repo = BorrowRepository(session)
            try:
                record = await repo.return_book(request.book_id, request.member_id)
                return library_service_pb2.ReturnResponse(
                    success=True, message="Book returned successfully"
                )
            except ReturnError as re:
                context.abort(grpc.StatusCode.FAILED_PRECONDITION, str(re))
            except NotFoundError as nf:
                context.abort(grpc.StatusCode.NOT_FOUND, str(nf))
            except Exception as e:
                context.abort(grpc.StatusCode.INTERNAL, str(e))

    async def ListBorrowedBooks(self, request, context):
        async with self.session_factory() as session:
            repo = BorrowRepository(session)
            try:
                books = await repo.list_borrowed_books(request.member_id)
                return library_service_pb2.BorrowListResponse(
                    books=[
                        library_service_pb2.Book(
                            id=b.id, title=b.title, author=b.author, published_year=b.published_year
                        )
                        for b in books
                    ]
                )
            except NotFoundError as nf:
                context.abort(grpc.StatusCode.NOT_FOUND, str(nf))
            except Exception as e:
                context.abort(grpc.StatusCode.INTERNAL, str(e))