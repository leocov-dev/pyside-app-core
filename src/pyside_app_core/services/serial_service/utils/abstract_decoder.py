from typing import Protocol, Self, TypeVar

T = TypeVar("T")


class CommandInterface(Protocol):
    def encode(self) -> bytearray:
        ...

    @classmethod
    def decode(cls, raw_data: bytes):
        ...


class TranscoderInterface(Protocol):
    @classmethod
    def encode_data(cls, command: CommandInterface) -> bytearray:
        pass

    @classmethod
    def decode_data(cls, data: bytearray) -> CommandInterface:
        pass

    @classmethod
    def format_error(cls, error: Exception) -> CommandInterface:
        pass
