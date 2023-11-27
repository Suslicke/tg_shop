from aiogram import Router, types
from aiogram.types import CallbackQuery, LabeledPrice, PreCheckoutQuery
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from bot.keyboards import get_pagination_keyboard
from bot.db.database import async_sessionmaker
from bot.db.models import ProductModel
from bot.config_reader import config


router = Router(name="callbacks-router")


@router.callback_query(lambda c: c.data.startswith('page_'))
async def query_page(callback_query: CallbackQuery):
    """
    Handles a page query in a paginated view of products.

    Parameters:
    - callback_query (CallbackQuery): The callback query from the telegram bot, containing data about the user's action.
    """
    current_page = int(callback_query.data.split('_')[1])  # извлекаем номер страницы из callback_data
    async with async_sessionmaker() as session:
        total_product_query = select(func.count()).select_from(ProductModel)
        total_product_result = await session.execute(total_product_query)
        total_products = total_product_result.scalar()

        model = await session.get(ProductModel, current_page)  # Индексация начинается с 1

        response_message = (
            f"Наименование: {model.name}\n"
            f"Цена: {model.price}\n"
        )
        media = types.InputMediaPhoto(media=model.photo_url)

        await callback_query.message.edit_media(
            media=media,
        )
        await callback_query.message.edit_caption(caption=response_message, reply_markup=get_pagination_keyboard(current_page, total_products))


@router.callback_query(lambda c: c.data.startswith('pay_'))
async def query_pay(callback_query: CallbackQuery, session: AsyncSession):
    """
   Create a payment request for a selected product.

    Parameters:
    - callback_query (CallbackQuery): The callback query from the telegram bot, containing data about the user's action.
    - session (AsyncSession): The database session for querying product details.
    """
    model_index = int(callback_query.data.split('_')[1])
    model = await session.get(ProductModel, model_index)

    # Тестовая цена и описание
    prices = [LabeledPrice(label=f"Товар {model.name}", amount=model.price * 100)]

    # Отправка инвойса
    await callback_query.bot.send_invoice(
        chat_id=callback_query.from_user.id,
        title=f"Товар {model.name}",
        description=f'{model.description}',
        provider_token=config.payment_token,
        currency="RUB",
        prices=prices,
        start_parameter="create_invoice",
        payload="some_invoice_payload"
    )

@router.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    """
    Handles the pre-checkout process for a payment.

    Parameters:
    - pre_checkout_query (PreCheckoutQuery): The pre-checkout query containing details of the checkout process.
    """
    await pre_checkout_query.message.answer_pre_checkout_query(pre_checkout_query.id, ok=True)