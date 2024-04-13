from dataclasses import dataclass

from domain.common.value import ValueObject


@dataclass
class Response(ValueObject):
    value: str
    symbols_to_ignore: str = r"_*[]()~`>#+-=|{}.!"

    def __post_init__(self):
        for symbol in self.symbols_to_ignore:
            self.value = self.value.replace(symbol, f"\{symbol}")
        self.value = self.value.replace(r"\`\`\`", "```")
        self.value = self.value.replace(r"\*\*", "**")

    def as_generic_type(self):
        return str(self.value)
