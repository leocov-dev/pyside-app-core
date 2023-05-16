import inspect
import io
import logging
import os
import sys
import traceback

DEFAULT_FORMATTER = logging.Formatter(
    "[%(levelname)s] %(name)s %(funcName)s #%(lineno)d -> %(message)s"
)


class PACHandler(logging.Handler):
    def emit(self, record):
        try:
            if record.levelno >= 40:
                stream = sys.stderr
            else:
                stream = sys.stdout

            stream.write(f"{self.format(record)}\n")

            self.acquire()
            try:
                stream.flush()
            finally:
                self.release()
        except RecursionError:
            raise
        except Exception:
            self.handleError(record)


__handler = PACHandler()
__handler.setFormatter(DEFAULT_FORMATTER)


def get_handler():
    return __handler


class PACLogger(logging.Logger):
    def __init__(self, name: str, level: int = logging.INFO):
        super(PACLogger, self).__init__(name=name, level=level)
        self.addHandler(get_handler())

    def findCaller(
        self, stack_info: bool = ..., stacklevel: int = ...
    ) -> tuple[str, int, str, str | None]:
        """
        Find the stack frame of the caller so that we can note the source
        file name, line number and function name.
        """
        f = inspect.currentframe()

        rv = "(unknown file)", 0, "(unknown function)", None
        while hasattr(f, "f_code"):
            # work our way up the frame stack to find the first thing that is
            # NOT from core/logging package. This is the real caller (we hope...)
            co = f.f_code
            filename = os.path.normcase(co.co_filename)

            # noinspection PyProtectedMember
            if "core/log" in filename or filename == logging._srcfile:
                f = f.f_back
                continue

            sinfo = None
            if stack_info:
                sio = io.StringIO()
                sio.write("Stack (most recent call last):\n")
                traceback.print_stack(f, file=sio)
                sinfo = sio.getvalue()
                if sinfo[-1] == "\n":
                    sinfo = sinfo[:-1]
                sio.close()

            rv = (co.co_filename, f.f_lineno, co.co_name, sinfo)
            break

        return rv
