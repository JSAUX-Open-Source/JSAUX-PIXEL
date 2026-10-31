# Contributing

Thanks for interest in the JSAUX PIXEL opensource tip.

## Before you start

- Everyday product UX (Decky modes, Studio) needs the **official JSAUX PIXEL release**
  (closed companion). See the
  [installation guide](https://jsaux.com/pages/steam-machine-faceplate-app-installation-guide).
- **Hardware calling in this tip** uses only the optimized open stack:
  `protocols/usb` (`dy_frame` + `UsbSerialTransport`) and `tools/matrix_cli.py`.
  Do not contribute closed companion serial stacks or proprietary transport dumps.
- Replacing the official Decky plugin with this tip is documented in
  [`docs/replace-official-plugin.md`](docs/replace-official-plugin.md).

## What we accept here

| Accept | Do not file here |
|--------|------------------|
| Fixes to protocol docs / `protocols/usb` (codec + transport) | Firmware / PCBA / LED-driver silicon issues |
| `tools/matrix_cli.py` and transport unit tests | Closed companion (`daemon` / Studio) bugs |
| LED API / codec / unit tests | Requests to open closed binaries |
| Plugin Python orchestration (`main.py`, `backend/`) | Hardware RMA / warranty claims |
| Docs / packaging helpers for this tip | |

## Frontend UI (`dist/index.js`)

Matching TSX sources are **not** in this tip. Please **do not** open PRs that
only rewrite `decky-plugin/dist/index.js` by hand. UI rebuild work needs the
source project to be restored first.

## Development checks

```bash
python3 tools/run_device_tests.py
# includes:
#   tests/test_usb_dy_frame.py
#   tests/test_usb_transport.py
#   tests/test_matrix_api.py
#   tests/plugin_ui_test.js
```

Optional hardware smoke (device + `pyserial`):

```bash
pip install '.[serial]'   # or: pip install pyserial
python3 tools/matrix_cli.py list
python3 tools/matrix_cli.py power on
python3 tools/matrix_cli.py brightness 128
python3 tools/matrix_cli.py gif examples/demo.gif
```

Optional CMake policy tests (Linux + Qt6 headers):

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build -j2
ctest --test-dir build --output-on-failure
```

## Pull requests

1. Keep changes focused and documented (one concern per PR).
2. Run `python3 tools/run_device_tests.py` before opening a PR.
3. Do not commit secrets, `auth.json`, closed ELFs, or personal paths.
4. Check that protocol/transport changes stay brand-neutral in docs (VID/PID hex OK).

## Code of conduct

See [`CODE_OF_CONDUCT.md`](./CODE_OF_CONDUCT.md).
