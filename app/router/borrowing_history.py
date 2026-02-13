from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.models.engine import get_db
from app.models.models import Book, BorrowingRecord, Member
from app.schema.schemas import BorrowingRecordCreate, BorrowingRecordResponse, BorrowingRecordUpdate

borrowing_router = APIRouter(prefix="/borrowings", tags=["Borrowing History"])


@borrowing_router.get("/", response_model=list[BorrowingRecordResponse])
def get_borrowing_records(db: Session = Depends(get_db)):
    query = select(BorrowingRecord)
    records = db.exec(query).all()
    return records


@borrowing_router.get("/{borrow_id}", response_model=BorrowingRecordResponse)
def get_borrowing_record_by_id(borrow_id: int, db: Session = Depends(get_db)):
    record = db.get(BorrowingRecord, borrow_id)
    if not record:
        raise HTTPException(status_code=404, detail="Borrowing record not found")
    return record


@borrowing_router.post("/", response_model=BorrowingRecordResponse, status_code=201)
def create_borrowing_record(record: BorrowingRecordCreate, db: Session = Depends(get_db)):
    book = db.get(Book, record.book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    member = db.get(Member, record.member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    if not book.is_available:
        raise HTTPException(status_code=400, detail="Book is not available for borrowing")

    db_record = BorrowingRecord(**record.model_dump())
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record


@borrowing_router.put("/{borrow_id}", response_model=BorrowingRecordResponse)
def update_borrowing_record(borrow_id: int, record: BorrowingRecordUpdate, db: Session = Depends(get_db)):
    db_record = db.get(BorrowingRecord, borrow_id)
    if not db_record:
        raise HTTPException(status_code=404, detail="Borrowing record not found")

    update_data = record.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_record, key, value)

    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record


@borrowing_router.delete("/{borrow_id}", status_code=204)
def delete_borrowing_record(borrow_id: int, db: Session = Depends(get_db)):
    record = db.get(BorrowingRecord, borrow_id)
    if not record:
        raise HTTPException(status_code=404, detail="Borrowing record not found")
    db.delete(record)
    db.commit()
    return None


@borrowing_router.post("/{borrow_id}/return", response_model=BorrowingRecordResponse)
def return_book(borrow_id: int, db: Session = Depends(get_db)):
    db_record = db.get(BorrowingRecord, borrow_id)
    if not db_record:
        raise HTTPException(status_code=404, detail="Borrowing record not found")

    if db_record.return_date:
        raise HTTPException(status_code=400, detail="Book has already been returned")

    db_record.return_date = date.today()
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record
