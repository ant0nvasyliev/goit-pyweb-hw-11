from datetime import date, timedelta

from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from src.entity.models import Contact

from src.schemas.contact import ContactSchema, ContactUpdate


async def get_contacts(limit: int, offset: int, db: AsyncSession):
    stmt = select(Contact).offset(offset).limit(limit)
    contacts = await db.execute(stmt)
    return contacts.scalars().all()


async def get_contact_by_id(contact_id: int, db: AsyncSession):
    stmt = select(Contact).filter_by(id=contact_id)
    contact = await db.execute(stmt)
    return contact.scalar_one_or_none()


async def create_contact(body: ContactSchema, db: AsyncSession):
    contact = Contact(**body.model_dump(exclude_unset=True))
    db.add(contact)
    await db.commit()
    await db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactUpdate, db: AsyncSession):
    stmt = select(Contact).filter_by(id=contact_id)
    result = await db.execute(stmt)
    contact = result.scalar_one_or_none()
    if not contact:
        return None
    for key, value in body.model_dump(exclude_unset=True).items():
        setattr(contact, key, value)
    await db.commit()
    await db.refresh(contact)
    return contact


async def delete_contact(contact_id: int, db: AsyncSession):
    stmt = select(Contact).filter_by(id=contact_id)
    result = await db.execute(stmt)
    contact = result.scalar_one_or_none()
    if not contact:
        return None
    await db.delete(contact)
    await db.commit()
    return contact


async def search_contacts(query: str, db: AsyncSession):
    stmt = select(Contact).where(
        or_(
            Contact.first_name.ilike(f"%{query}%"),
            Contact.second_name.ilike(f"%{query}%"),
            Contact.email.ilike(f"%{query}%"),
        )
    )
    contacts = await db.execute(stmt)
    return contacts.scalars().all()


async def get_upcoming_birthdays(db: AsyncSession):
    today = date.today()
    next_week = today + timedelta(days=7)
    stmt = select(Contact).where(
        Contact.birth_date.between(today, next_week)
    )
    contacts = await db.execute(stmt)
    return contacts.scalars().all()
