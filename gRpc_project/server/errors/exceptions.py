class LibraryError(Exception):
    """Base class for all custom exceptions in the library system."""
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class ValidationError(LibraryError):
    """Raised when input validation fails (e.g., missing fields, invalid values)."""
    pass


class NotFoundError(LibraryError):
    """Raised when a requested entity (Book, Member, BorrowRecord) is not found."""
    pass


class AlreadyExistsError(LibraryError):
    """Raised when attempting to create an entity that already exists (e.g., duplicate email)."""
    pass


class BorrowError(LibraryError):
    """Raised when borrowing a book fails (e.g., no available copies)."""
    pass


class ReturnError(LibraryError):
    """Raised when returning a book fails (e.g., no active borrow record)."""
    pass