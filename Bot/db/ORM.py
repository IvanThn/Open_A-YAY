import os

from dotenv import load_dotenv
from sqlalchemy import BigInteger
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column

load_dotenv()
engine = create_async_engine(url=os.getenv('SQLALCHEMY_URL'))

async_session = async_sessionmaker(engine, expire_on_commit=False)


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column()

    def __repr__(self):
        return f'ID: {self.id} NAME: {self.name}'


class Sign(Base):
    __tablename__ = 'signs'

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    about: Mapped[str] = mapped_column(nullable=True)

    def __repr__(self):
        return f'{self.id} - {self.name}: {self.about}'


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
