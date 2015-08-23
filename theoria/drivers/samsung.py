"""
A Samsung LCD Screen driver for Theoria.
"""

from PIL import Image
from cStringIO import StringIO
import time
import struct
import usb.core
from usb.util import *

SAMSUNG_VID = 0x04e8
MASS_STORAGE_PID = 0x2035
MINI_DISPLAY_PID = 0x2036

def create(*args, **kwargs):
    return SamsungDriver(*args, **kwargs)

class SamsungDriver:
    def __init__(self):
        # Look for the frame in storage mode
        dev = usb.core.find(idVendor=SAMSUNG_VID, idProduct=MASS_STORAGE_PID)
        if dev is not None:
            try:
                dev.ctrl_transfer(CTRL_TYPE_STANDARD | CTRL_IN | CTRL_RECIPIENT_DEVICE, 0x06, 0xfe, 0xfe, 254)
            except usb.core.USBError as e:
                pass # Ignore the error from the device disappearing

        # Give the display 3 seconds to come back
        time.sleep(3)

        # Look for the frame in display mode
        ev = usb.core.find(idVendor=SAMSUNG_VID, idProduct=MINI_DISPLAY_PID)
        dev.set_configuration()
        result = dev.ctrl_transfer(CTRL_TYPE_VENDOR | CTRL_IN | CTRL_RECIPIENT_DEVICE, 0x04, 0x00, 0x00, 1)

        self._dev = dev
        self._buffer = Image.new('RGB', (1024, 600))

    def get_buffer(self):
        return self._buffer

    def get_img_data(self):
        out = StringIO()
        self._buffer.save(out, 'JPEG', quality=95)
        imgdata = out.getvalue()
        out.close()
        return imgdata

    def send_buffer(self):
        pic = self.get_img_data()
        rawdata = b"\xa5\x5a\x18\x04" + struct.pack('<I', len(pic)) + b"\x48\x00\x00\x00" + pic
        pad = 16384 - (len(rawdata) % 16384)
        tdata = rawdata + pad * b'\x00'
        tdata = tdata + b'\x00'
        endpoint = 0x02
        self._dev.write(endpoint, tdata)

