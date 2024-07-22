from aiogram.fsm.state import State, StatesGroup


class CreateModel(StatesGroup):
    name = State()


class CreateSubscription(StatesGroup):
    name = State()


class AddModelToSubscription(StatesGroup):
    subscription_name = State()
    model_name = State()
    default_requests = State()
