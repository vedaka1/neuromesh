from dataclasses import dataclass, field


@dataclass
class Response:
    """A class that receives text and escapes all unwanted symbols in it"""

    value: str
    _symbols_to_ignore: str = field(default=r"_*[]()~`>#+-=|{}.!", init=False)

    def __post_init__(self):
        for symbol in self._symbols_to_ignore:
            self.value = self.value.replace(symbol, f"\{symbol}")
        self.value = self.value.replace(r"\*", "*")
        self.value = self.value.replace(r"\`", "`")


@dataclass
class Link:
    """A class that receives text and escapes all unwanted symbols in it"""

    value: str
    _symbols_to_ignore: str = field(default=r"()", init=False)

    def __post_init__(self):
        self.value = self.value.replace(" ", "")
        for symbol in self._symbols_to_ignore:
            self.value = self.value.replace(symbol, f"\{symbol}")
