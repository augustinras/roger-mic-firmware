"""Package Roger's signed app with Omi's qualified CV1 bootloader for wired service."""

import argparse
import sys
import zipfile
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("vendor_tools", type=Path)
parser.add_argument("qualified_hex", type=Path)
parser.add_argument("built_zip", type=Path)
parser.add_argument("output", type=Path)
parser.add_argument("version")
args = parser.parse_args()

# The workflow pins the upstream packaging tools and their bootloader policy.
sys.path.insert(0, str(args.vendor_tools.resolve()))
from cv1_bootloader import boot_bytes, read_hex, validate_release_hex, wire_memory, write_hex
from cv1_release import repackage, validate_signed_version

args.output.mkdir(parents=True, exist_ok=True)
ota = args.output / f"Omi_CV1_OTA_v{args.version}.zip"
wired = args.output / f"Omi_CV1_v{args.version}.hex"
repackage(args.built_zip, ota)
with zipfile.ZipFile(ota) as archive:
    validate_signed_version(archive, args.version)
    image = archive.read("omi.signed.bin")
loader = boot_bytes(read_hex(args.qualified_hex))
write_hex(wired, wire_memory(image, loader))
validate_release_hex(wired, image)
