class Text:
    @property
    def start(self):
        text = str(
            "Данный бот может отправлять последние новости с сайта dvinanews.ru\n\n"
            + "/news - для получения последних новостей\n"
            + "/newsletter - для подписки на рассылку новостей\n"
            + "/info - информация для администратора\n"
            + "/request_access - запросить права администратора"
        )
        return text

    @property
    def info(self):
        text = str(
            "Администратор может создавать подписки и модели, управлять содержанием подписок\n\n"
            + "/models - Список доступных моделей нейросетей\n"
            + "/subscriptions - Список доступных подписок\n"
            + "/create_model <name> - Создать модель нейросети\n"
            + "/create_sub <name> - Создать подписку\n"
            + "/add_model_to_sub <sub_name> <mdoel_name> <default_requests> - Добавить модель в подписку\n"
        )
        return text

    @property
    def permission_denied(self):
        text = str("\U00002757 Недостаточно прав\n\n")
        return text

    def request_access(self, user_id: int, username: str):
        text = "Пользователь запросил права администратора\n\n*ID:* {0}\n*username:* {1}".format(
            user_id, username
        )
        return text


text = Text()
