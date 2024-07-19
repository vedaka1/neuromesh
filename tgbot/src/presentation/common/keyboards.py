from aiogram import types


class Keyboards:

    @property
    def image_keyboard(self):
        buttons = [
            [
                types.InlineKeyboardButton(text="Да", callback_data="image_yes"),
                types.InlineKeyboardButton(text="Нет", callback_data="image_no"),
            ]
        ]
        return buttons

    @property
    def send_announcement_keyboard(self):
        buttons = [
            [
                types.InlineKeyboardButton(text="Отправить", callback_data="send_yes"),
                types.InlineKeyboardButton(text="Отменить", callback_data="send_no"),
            ]
        ]
        return buttons


kb = Keyboards()
