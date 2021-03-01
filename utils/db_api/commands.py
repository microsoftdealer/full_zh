from asyncpg import UniqueViolationError

from utils.db_api.db_gino import db
from utils.db_api.schemas.radiance import RadianceImg, User


async def select_user_by_id(user_id):
    user = await User.query.where(User.id == user_id).gino.all()
    return user


async def new_rad(user_id, year, month, photo_id, state):
    try:
        rad = RadianceImg(owner_id=user_id, year=year, photo_id=photo_id, state=state, month=month)
        await rad.create()

    except UniqueViolationError:
        pass


async def check_this_month(tg_id, month, year):
    rad = await RadianceImg.query.where(RadianceImg.owner_id == tg_id).where(RadianceImg.month == str(month)
                                        ).where(RadianceImg.year == year).gino.first()
    return rad if rad else False


async def delete_rad(id):
    rad = await RadianceImg.query.where(RadianceImg.id == id).gino.first()
    await rad.delete()


async def add_question(topic: str, questions: str, right_answer: str, wrong_answer: str, explanation: str = None):
    try:
        question = Questions(topic=topic, questions=questions,
                             right_answer=right_answer, wrong_answer=wrong_answer,
                             explanation=explanation)
        await question.create()

    except UniqueViolationError:
        pass


async def select_question_by_topic(topics):
    questions = await Questions.query.where(Questions.topic == topics).gino.all()
    return questions


async def select_all_question():
    question = await Questions.query.gino.all()
    return question


async def select_all_users():
    users = await User.query.order_by(User.rating.desc()).gino.all()
    return users


async def select_all_admins():
    users = await User.query.order_by(User.admin_stats.desc()).gino.all()
    return users


async def add_user(user_id: int, name: str, referral: int = 1079453114):
    try:
        user = User(tg_id=user_id, name=name, referral=referral)
        await user.create()

    except UniqueViolationError:
        pass


async def select_user(id: int):
    user = await User.query.where(User.id == id).gino.first()
    return user


async def select_language_by_id(lang: str):
    user = await User.query.where(User.lang == lang).gino.all()
    return user


async def select_questions_id(questions_ids: int):
    user = await User.query.where(User.questions_ids == questions_ids).gino.all()
    return user


async def select_questions(id: int):
    questions = await Questions.query.where(Questions.id == id).gino.first()
    return questions


async def count_users():
    total = await db.func.count(User.id).gino.scalar()
    return total


async def count_questions():
    total = await db.func.count(Questions.id).gino.scalar()
    return total


async def update_rating(id: int, rating: int):
    user = await User.query.where(User.id == id).gino.first()
    await user.update(rating=rating).apply()


async def update_admin_stats(id: int, admin_stats: int):
    user = await User.query.where(User.id == id).gino.first()
    await user.update(admin_stats=admin_stats).apply()


async def update_user_stats(id: int, stats: str):
    user = await User.query.where(User.id == id).gino.first()
    await user.update(stats=stats).apply()


async def update_language(id: int, language: str):
    user = await User.query.where(User.id == id).gino.first()
    await user.update(language=language).apply()
