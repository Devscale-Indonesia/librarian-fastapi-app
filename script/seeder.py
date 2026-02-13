"""
Database seeder script for populating the library database with realistic data.
Run from project root: python -m script.seeder
"""

import random
import sys
from datetime import date, timedelta
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlmodel import Session, SQLModel

from app.models.engine import engine
from app.models.models import Book, BorrowingRecord, Member

# Real books with actual titles, authors, and ISBNs
BOOKS_DATA = [
    {"title": "To Kill a Mockingbird", "author": "Harper Lee", "isbn": "978-0-06-112008-4"},
    {"title": "1984", "author": "George Orwell", "isbn": "978-0-45-152493-5"},
    {"title": "Pride and Prejudice", "author": "Jane Austen", "isbn": "978-0-14-143951-8"},
    {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "isbn": "978-0-74-327356-5"},
    {"title": "One Hundred Years of Solitude", "author": "Gabriel Garcia Marquez", "isbn": "978-0-06-088328-7"},
    {"title": "The Catcher in the Rye", "author": "J.D. Salinger", "isbn": "978-0-31-676948-0"},
    {"title": "Brave New World", "author": "Aldous Huxley", "isbn": "978-0-06-085052-4"},
    {"title": "The Lord of the Rings", "author": "J.R.R. Tolkien", "isbn": "978-0-54-400341-5"},
    {"title": "Harry Potter and the Sorcerer's Stone", "author": "J.K. Rowling", "isbn": "978-0-59-035342-7"},
    {"title": "The Hobbit", "author": "J.R.R. Tolkien", "isbn": "978-0-54-792822-7"},
    {"title": "Fahrenheit 451", "author": "Ray Bradbury", "isbn": "978-1-45-167331-9"},
    {"title": "Jane Eyre", "author": "Charlotte Bronte", "isbn": "978-0-14-144114-6"},
    {"title": "Wuthering Heights", "author": "Emily Bronte", "isbn": "978-0-14-143955-6"},
    {"title": "The Odyssey", "author": "Homer", "isbn": "978-0-14-026886-7"},
    {"title": "Crime and Punishment", "author": "Fyodor Dostoevsky", "isbn": "978-0-14-310763-5"},
    {"title": "War and Peace", "author": "Leo Tolstoy", "isbn": "978-0-14-044793-4"},
    {"title": "Anna Karenina", "author": "Leo Tolstoy", "isbn": "978-0-14-303500-8"},
    {"title": "The Brothers Karamazov", "author": "Fyodor Dostoevsky", "isbn": "978-0-37-441122-3"},
    {"title": "Moby-Dick", "author": "Herman Melville", "isbn": "978-0-14-243724-7"},
    {"title": "Don Quixote", "author": "Miguel de Cervantes", "isbn": "978-0-06-093434-7"},
]

# Real-sounding member names and emails
MEMBERS_DATA = [
    {"name": "Emma Thompson", "email": "emma.thompson@gmail.com"},
    {"name": "James Wilson", "email": "james.wilson@outlook.com"},
    {"name": "Sofia Rodriguez", "email": "sofia.rodriguez@yahoo.com"},
    {"name": "Michael Chen", "email": "michael.chen@gmail.com"},
    {"name": "Olivia Johnson", "email": "olivia.johnson@hotmail.com"},
    {"name": "William Davis", "email": "william.davis@gmail.com"},
    {"name": "Isabella Martinez", "email": "isabella.martinez@outlook.com"},
    {"name": "Alexander Brown", "email": "alex.brown@yahoo.com"},
    {"name": "Mia Anderson", "email": "mia.anderson@gmail.com"},
    {"name": "Benjamin Taylor", "email": "ben.taylor@hotmail.com"},
    {"name": "Charlotte White", "email": "charlotte.white@gmail.com"},
    {"name": "Daniel Harris", "email": "daniel.harris@outlook.com"},
    {"name": "Amelia Clark", "email": "amelia.clark@yahoo.com"},
    {"name": "Henry Lewis", "email": "henry.lewis@gmail.com"},
    {"name": "Sophia Walker", "email": "sophia.walker@hotmail.com"},
]


def seed_books(session: Session) -> list[Book]:
    """Seed the database with books."""
    books = []
    for book_data in BOOKS_DATA:
        book = Book(**book_data)
        session.add(book)
        books.append(book)
    session.commit()
    for book in books:
        session.refresh(book)
    print(f"Seeded {len(books)} books")
    return books


def seed_members(session: Session) -> list[Member]:
    """Seed the database with members."""
    members = []
    for member_data in MEMBERS_DATA:
        member = Member(**member_data)
        session.add(member)
        members.append(member)
    session.commit()
    for member in members:
        session.refresh(member)
    print(f"Seeded {len(members)} members")
    return members


def seed_borrowing_records(session: Session, books: list[Book], members: list[Member]) -> list[BorrowingRecord]:
    """Seed the database with borrowing records."""
    records = []
    today = date.today()

    # Create some past borrowing records (returned)
    for i in range(10):
        book = random.choice(books)
        member = random.choice(members)
        borrow_date = today - timedelta(days=random.randint(30, 90))
        return_date = borrow_date + timedelta(days=random.randint(7, 21))

        record = BorrowingRecord(
            book_id=book.id,
            member_id=member.id,
            borrow_date=borrow_date,
            return_date=return_date,
        )
        session.add(record)
        records.append(record)

    # Create some current borrowing records (not yet returned)
    for i in range(5):
        book = random.choice(books)
        member = random.choice(members)
        borrow_date = today - timedelta(days=random.randint(1, 14))

        record = BorrowingRecord(
            book_id=book.id,
            member_id=member.id,
            borrow_date=borrow_date,
            return_date=None,
        )
        session.add(record)
        records.append(record)

    session.commit()
    print(f"Seeded {len(records)} borrowing records")
    return records


def main():
    """Main seeder function."""
    print("Creating database tables...")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        print("\nSeeding database with realistic data...\n")

        books = seed_books(session)
        members = seed_members(session)
        seed_borrowing_records(session, books, members)

        print("\nDatabase seeding completed successfully!")


if __name__ == "__main__":
    main()
