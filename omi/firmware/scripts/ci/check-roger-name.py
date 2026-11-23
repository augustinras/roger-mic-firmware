"""Check the complete Bluetooth name in a built CV1 update."""

import json
import struct
import sys
import uuid
import zipfile


def check_advertisement(package):
    with zipfile.ZipFile(package) as archive:
        files = json.loads(archive.read("manifest.json"))["files"]
        app = next(entry for entry in files if entry["image_index"] == "0")
        image = archive.read(app["file"])

    wake_characteristic = uuid.UUID("19b10014-e8f2-537e-4f6c-d104768a1214")
    if wake_characteristic.bytes[::-1] in image:
        raise ValueError("The name-only build contains the custom wake-light characteristic")

    # The signed image starts one MCUboot header before the app's load address.
    header_size = struct.unpack_from("<H", image, 8)[0]
    image_base = app["load_address"] - header_size
    name = b"Roger"
    # The CV1 advertises flags, a 128-bit service, then its complete local name.
    # Zephyr bt_data entries on nRF5340 carry a type, byte count and data pointer.
    for offset in range(16, len(image) - 7, 4):
        if image[offset - 16 : offset - 14] != b"\x01\x01":
            continue
        if image[offset - 8 : offset - 6] != b"\x07\x10":
            continue
        kind, size, address = struct.unpack_from("<BB2xI", image, offset)
        if kind == 9 and size == len(name) and address >= image_base:
            start = address - image_base
            if image[start : start + size] == name:
                return
    raise ValueError("The CV1 advertisement does not contain the complete name Roger")


if __name__ == "__main__":
    check_advertisement(sys.argv[1])
    print("Verified complete Bluetooth name Roger")
