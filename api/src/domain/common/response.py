from dataclasses import dataclass, field

from domain.common.value import ValueObject


@dataclass
class Response(ValueObject[str]):
    value: str
    _symbols_to_ignore: str = field(default=r"_*[]()~`>#+-=|{}.!", init=False)

    def __post_init__(self):
        for symbol in self._symbols_to_ignore:
            self.value = self.value.replace(symbol, f"\{symbol}")
        self.value = self.value.replace(r"\`\`\`", "```")
        self.value = self.value.replace(r"\*\*", "**")


@dataclass
class ModelResponse(ValueObject[str]):
    value: str
