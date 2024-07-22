from aiogram import types


class Keyboards:

    def select_model(self,user_id: int, data: dict):
        buttons = [
            [
                types.InlineKeyboardButton(
                    text=model["name"], callback_data=f"selectModel_{user_id}_{model["name"]}"
                )
            ]
            for model in data["models"]
        ]
        return types.InlineKeyboardMarkup(inline_keyboard=buttons)
    
    def all_models(self, data: dict):
        buttons = [
            [
                types.InlineKeyboardButton(
                    text=model["name"], callback_data=f"selectModel_{model["name"]}"
                )
            ]
            for model in data
        ]
        return types.InlineKeyboardMarkup(inline_keyboard=buttons)
    
    def all_subscriptions(self, data: dict):
        buttons = [
            [
                types.InlineKeyboardButton(
                    text=sub["name"], callback_data=f"selectSub_{sub["name"]}"
                )
            ]
            for sub in data
        ]
        return types.InlineKeyboardMarkup(inline_keyboard=buttons)

    @property
    def image_keyboard(self):
        buttons = [
            [
                types.InlineKeyboardButton(text="Да", callback_data="image_yes"),
                types.InlineKeyboardButton(text="Нет", callback_data="image_no"),
            ]
        ]
        return types.InlineKeyboardMarkup(inline_keyboard=buttons)

    @property
    def send_announcement_keyboard(self):
        buttons = [
            [
                types.InlineKeyboardButton(text="Отправить", callback_data="send_yes"),
                types.InlineKeyboardButton(text="Отменить", callback_data="send_no"),
            ]
        ]
        return types.InlineKeyboardMarkup(inline_keyboard=buttons)


kb = Keyboards()
