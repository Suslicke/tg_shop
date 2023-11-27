from aiogram import Router, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from sqlalchemy import func, select

from bot.db.models import ProductModel, UserModel
from bot.keyboards import get_pagination_keyboard
from bot.db.database import async_sessionmaker

router = Router(name="commands-router")


@router.message(CommandStart())
async def cmd_start(message: types.Message):
    """
    Handle the /start command

    Parameters:
    - message (types.Message): The message object from the Telegram API, containing the user's message and other metadata.

    Process:
    1. Extract user data from the message object.
    2. Check if the user already exists in the database.
    3. If not, create a new user entry and save it to the database.
    4. Send a welcome message to the user.

    :param message: Telegram message with "/start" text
    """
    user_data = {
        "telegram_id": message.from_user.id,
        "name": message.from_user.full_name,
        "username": message.from_user.username
    }

    async with async_sessionmaker() as session:
        existing_user = await session.execute(
            select(UserModel).filter_by(telegram_id=user_data["telegram_id"])
        )
        existing_user = existing_user.scalar_one_or_none()

        if not existing_user:
            new_user = UserModel(**user_data)
            session.add(new_user)
            await session.commit()

    await message.answer(
        "Добрый день, это магазин.\n"
        "Можете выбрать товары, после нажать кнопку заказать\n\n"
        "Вы можете использовать /browse для просмотра товаров"
    )


@router.message(Command('browse'))
async def cmd_browse(message: Message):
    """
    Handle the 'browse' command

    Parameters:
    - message (types.Message): The message object from the Telegram API, containing the user's message and other metadata.

    Process:
    1. Retrieve the total count of products from the database.
    2. Check if there are any products available.
    3. If products are available, display the first product with its details.
    4. Provide a response message and a photo of the product with a pagination keyboard for navigation.


    :param message:
    :return:
    """
    async with async_sessionmaker() as session:
        total_product_query = select(func.count()).select_from(ProductModel)
        total_product_result = await session.execute(total_product_query)
        total_products = total_product_result.scalar()

        if total_products == 0:
            await message.answer("На данный момент продуктов нет.")
            return

        index = 1

        model = await session.get(ProductModel, index)

        response_message = (
            f"Наименование: {model.name}\n"
            f"Цена: {model.price}\n"
            f"Описание: {model.description}\n"
        )

        await message.answer_photo(photo=str(model.photo_url), caption=response_message, reply_markup=get_pagination_keyboard(index, total_products))
