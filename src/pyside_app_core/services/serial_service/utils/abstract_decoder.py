from typing import Protocol, Self, TypeVar

T = TypeVar("T")


class CommandInterface(Protocol[T]):
    def encode(self) -> bytearray:
        ...

    @classmethod
    def decode(cls, raw_data: bytes) -> Self:
        ...


class TranscoderInterface(Protocol[T]):
    @classmethod
    def encode_data(cls, command: CommandInterface) -> bytearray:
        pass

    @classmethod
    def decode_data(cls, data: bytearray) -> CommandInterface:
        pass

    @classmethod
    def format_error(cls, error: Exception) -> CommandInterface:
        pass
