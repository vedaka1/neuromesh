class Text:
    @property
    def start(self):
        text = str(
            "This bot can provide access to neural networks by subscription\n\n"
            + "/select_model - Select neural network\n"
            + "/account - Your account\n"
            + "/subscriptions - Available subscriptions"
            + "/imagine <prompt> - Generate image from prompt"
        )
        return text

    @property
    def info(self):
        text = str(
            "Администратор может создавать подписки и модели, управлять содержанием подписок\n\n"
            + "/models - Список доступных моделей нейросетей\n"
            + "/subscriptions - Список доступных подписок\n"
            + "/create_model - Создать модель нейросети\n"
            + "/create_sub - Создать подписку\n"
            + "/add_model_to_sub - Добавить модель нейросети в подписку\n"
        )
        return text

    @property
    def permission_denied(self):
        text = str("\U00002757 Access denied\n\n")
        return text

    def request_access(self, user_id: int, username: str):
        text = "Пользователь запросил права администратора\n\n*ID:* {0}\n*username:* {1}".format(
            user_id, username
        )
        return text


text = Text()
