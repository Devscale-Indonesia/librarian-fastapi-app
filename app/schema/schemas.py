from datetime import date

from pydantic import BaseModel


class BookCreate(BaseModel):
    title: str
    author: str
    isbn: str


class BookUpdate(BaseModel):
    title: str | None = None
    author: str | None = None
    isbn: str | None = None


class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    is_available: bool

    class Config:
        from_attributes = True


class MemberCreate(BaseModel):
    name: str
    email: str


class MemberUpdate(BaseModel):
    name: str | None = None
    email: str | None = None


class MemberResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True


class BorrowingRecordCreate(BaseModel):
    borrow_date: date
    book_id: int
    member_id: int


class BorrowingRecordUpdate(BaseModel):
    return_date: date | None = None


class BorrowingRecordResponse(BaseModel):
    borrow_id: int
    borrow_date: date
    return_date: date | None
    book_id: int
    member_id: int

    class Config:
        from_attributes = True
