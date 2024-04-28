import atexit
import ctypes as cts
import os
import sys
from ctypes import wintypes as wts
from typing import Optional

__IS_WIN = sys.platform[:3].lower() == "win"
__DLL_NAME = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "zdoc.{:s}".format("dll" if __IS_WIN else "so"),
)

if __IS_WIN:
    __DLL = cts.CDLL(__DLL_NAME)

    __MessageBoxXY = __DLL.MessageBoxXY
    __MessageBoxXY.argtypes = (
        wts.HWND,
        wts.LPCWSTR,
        wts.LPCWSTR,
        wts.UINT,
        cts.c_int,
        cts.c_int,
    )
    __MessageBoxXY.restype = cts.c_int

    def MessageBox(
        title: str,
        text: str,
        x: Optional[int] = None,
        y: Optional[int] = None,
        style: int = 0,
        hwnd: Optional[wts.HWND] = None,
    ):
        return __MessageBoxXY(
            hwnd,
            text,
            title,
            style,
            x if x is not None else 0x80000000,
            y if y is not None else 0x80000000,
        )

    __clearHooks = __DLL.clearHooks
    __clearHooks.argtypes = ()
    __clearHooks.restype = cts.c_int
    atexit.register(__clearHooks)
    del __clearHooks

    __all__ = ("MessageBox",)
else:  # Nix
    __DLL = None
    __all__ = ()


del __DLL
del __DLL_NAME
del __IS_WIN


if __name__ == "__main__":
    print("This script is not meant to be run directly.\n")
    sys.exit(-1)
