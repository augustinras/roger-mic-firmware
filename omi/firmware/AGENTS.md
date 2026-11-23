# Firmware (Omi CV1) — Agent Guide

Component guide for `omi/firmware/`. General engineering rules: root `AGENTS.md`.

## Release Workflow

Firmware releases are manual via `.github/workflows/firmware_release.yml`:

1. Bump `CONFIG_BT_DIS_FW_REV_STR` in `omi/firmware/omi/omi.conf` first.
2. `gh workflow run firmware_release.yml -f publish=publish -f changelog="..." -f minimum_app_version_code=...` (omit `publish` for a build-only QA run).
3. The workflow builds via Docker (NCS 2.9.0 sysbuild + MCUboot), names the OTA asset `Omi_CV1_OTA_v<ver>.zip` (the "ota" substring is required), and publishes a `Omi_CV1_v<ver>` GitHub Release with the `KEY_VALUE` body that `backend/routers/firmware.py` serves.

Build logic lives in `omi/firmware/scripts/ci/`.

On this Roger branch, build without the publish input for individual CV1
installations. Check the downloaded OTA ZIP with
`python3 omi/firmware/scripts/ci/check-roger-name.py <ota.zip>`.
The name-only variant advertises the complete name `Roger`. It uses the
stock CV1 3.0.21 application source and retains its original LED behavior.
Only the Bluetooth name and release version settings differ from stock. The Roger build stamps the same release version in the signed
app header and device information. Its OTA ZIP updates the application.
For a wired service fixture, use the staged HEX that passes Omi's bootloader
policy and exact signed-app check. The raw merged build output is unsuitable
for that purpose. Omi documents the stock 3.0.21 Bluetooth update failure in
the [CV1 recovery guide](https://github.com/BasedHardware/omi/blob/bf8b408e153de69a8644949846a295a070102088/omi/firmware/docs/cv1-manufacturing-and-field-recovery.md#fielded-stock-3021-units).

## Formatting

C/C++ files: `clang-format -i <files>` (the repo pre-commit hook covers this).
