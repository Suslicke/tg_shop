from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_pagination_keyboard(current_page: int, total_pages: int) -> InlineKeyboardMarkup:
    """
    Generates an inline keyboard markup for pagination and a payment button.

    Parameters:
    - current_page (int): The current page number in the pagination sequence.
    - total_pages (int): The total number of pages available in the pagination sequence.

    Returns:
    - InlineKeyboardMarkup: An object representing the inline keyboard layout with the created buttons.
    """
    buttons = []

    if current_page >= 1:
        buttons.append(InlineKeyboardButton(text="⬅️", callback_data=f"page_{current_page - 1}"))
    else:
        buttons.append(InlineKeyboardButton(text="⬅️", callback_data="noop", disabled=True))

    buttons.append(InlineKeyboardButton(text=f"{current_page}/{total_pages}", callback_data="noop"))

    if current_page < total_pages:
        buttons.append(InlineKeyboardButton(text="➡️", callback_data=f"page_{current_page + 1}"))
    else:
        buttons.append(InlineKeyboardButton(text="➡️", callback_data="noop", disabled=True))

    payment_button = [InlineKeyboardButton(text="💳 Оплатить", callback_data=f"pay_{current_page}")]

    keyboard = InlineKeyboardMarkup(inline_keyboard=[buttons, payment_button])
    return keyboard