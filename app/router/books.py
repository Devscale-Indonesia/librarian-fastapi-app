from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.models.engine import get_db
from app.models.models import Book
from app.schema.schemas import BookCreate, BookResponse, BookUpdate

books_router = APIRouter(prefix="/books", tags=["Books"])


@books_router.get("/", response_model=list[BookResponse])
def get_books(db: Session = Depends(get_db)):
    query = select(Book)
    books = db.exec(query).all()
    return books


@books_router.get("/{id}", response_model=BookResponse)
def get_book_by_id(id: int, db: Session = Depends(get_db)):
    book = db.get(Book, id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@books_router.post("/", response_model=BookResponse, status_code=201)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    db_book = Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


@books_router.put("/{id}", response_model=BookResponse)
def update_book(id: int, book: BookUpdate, db: Session = Depends(get_db)):
    db_book = db.get(Book, id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")

    update_data = book.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_book, key, value)

    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


@books_router.delete("/{id}", status_code=204)
def delete_book(id: int, db: Session = Depends(get_db)):
    book = db.get(Book, id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()
    return None
