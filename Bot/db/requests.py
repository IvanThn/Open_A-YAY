from sqlalchemy import select

from Bot.db.ORM import User, Sign, async_session


async def insert_user(user_id: int, user_name: str = 'пользователь') -> None:
    async with async_session() as session:
        user_in_db = await session.scalar(select(User).where(User.id == user_id))
        if not user_in_db:
            user = User(
                id=user_id,
                name=user_name,
            )
            session.add(user)
            await session.commit()


async def select_signs(signs_id: list[int]) -> list[Sign]:
    async with async_session() as session:
        signs_id = set(map(lambda x: '.'.join(x.split('.')[:3]), signs_id))
        signs = []
        for sign_id in signs_id:
            sign = await session.scalar(select(Sign).where(Sign.id == sign_id))
            if sign:
                signs.append(sign)
            else:
                sign = await session.scalar(select(Sign).where(Sign.id == '.'.join(sign_id.split('.')[:-1])))
                if sign:
                    signs.append(sign)
        return signs


async def select_user(user_id: int) -> User:
    async with async_session() as session:
        return await session.scalar(select(User).where(User.id == user_id))


async def transfer_db(sign_id, sign_name, sign_about):
    async with async_session() as session:
        sign_in_db = await session.scalar(select(Sign).where(Sign.id == sign_id))
        if not sign_in_db:
            session.add(Sign(id=sign_id, name=sign_name, about=sign_about))
            await session.commit()
