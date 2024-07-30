from pyside_app_core.services.serial_service.types import ChunkedData, Decodable, Encodable, TranscoderInterface


class Message(Encodable):
    """"""

    def encode(self) -> bytes:
        return b""

    def __str__(self) -> str:
        return f"<{self.__class__.__name__}>"


class Result(Decodable):
    """"""

    def __init__(self, data: bytes):
        self._raw_data = data

    @classmethod
    def decode(cls, data: bytes) -> "Result":
        return cls(data)

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return f"<{self.__class__.__name__}>({self._raw_data!r})"


class RawTranscoder(TranscoderInterface):
    SEP = b"\r\n"

    @classmethod
    def process_buffer(cls, buffer: bytearray) -> ChunkedData:
        if cls.SEP in buffer:
            chunks: list[bytearray]
            remainder: bytearray
            *chunks, remainder = buffer.split(cls.SEP)
            return chunks, remainder

        return [], None

    @classmethod
    def encode(cls, data: Encodable) -> bytes:
        return data.encode()

    @classmethod
    def decode(cls, raw: bytearray) -> Result:
        return Result.decode(raw)
