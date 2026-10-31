#!/usr/bin/env python3
"""Command-line host tools for the USB-serial DY connection protocol."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from protocols.usb.transport import (  # noqa: E402
    TransportError,
    UsbSerialTransport,
    iter_ports_as_dicts,
    list_candidate_ports,
    require_pyserial,
)


def _add_port_arg(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--port",
        default="",
        help="Serial device path (default: first allowlisted VID/PID port)",
    )


def cmd_list(_args: argparse.Namespace) -> int:
    require_pyserial()
    ports = list_candidate_ports()
    print(json.dumps(iter_ports_as_dicts(ports), indent=2))
    return 0


def cmd_power(args: argparse.Namespace) -> int:
    enabled = args.state == "on"
    with UsbSerialTransport(port=args.port or None) as bus:
        reply = bus.set_power(enabled)
    print(f"ok power={args.state} status=0x{reply.payload[:1].hex() or '??'}")
    return 0


def cmd_brightness(args: argparse.Namespace) -> int:
    level = max(0, min(255, int(args.level)))
    with UsbSerialTransport(port=args.port or None) as bus:
        reply = bus.set_brightness(level)
    print(f"ok brightness={level} status=0x{reply.payload[:1].hex() or '??'}")
    return 0


def cmd_gif(args: argparse.Namespace) -> int:
    path = Path(args.path)
    data = path.read_bytes()
    with UsbSerialTransport(port=args.port or None) as bus:
        reply = bus.upload_gif(data)
    print(f"ok gif={path} bytes={len(data)} status=0x{reply.payload[:1].hex() or '??'}")
    return 0


def cmd_animation(args: argparse.Namespace) -> int:
    animation_id = max(0, min(255, int(args.animation_id)))
    with UsbSerialTransport(port=args.port or None) as bus:
        reply = bus.play_animation(animation_id)
    print(f"ok animation={animation_id} status=0x{reply.payload[:1].hex() or '??'}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="matrix_cli",
        description=(
            "Optimized host USB-serial DY tools (open tip). "
            "This is the supported hardware calling path in this repository."
        ),
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_list = sub.add_parser("list", help="List allowlisted USB serial ports")
    p_list.set_defaults(func=cmd_list)

    p_power = sub.add_parser("power", help="Set screen power")
    _add_port_arg(p_power)
    p_power.add_argument("state", choices=("on", "off"))
    p_power.set_defaults(func=cmd_power)

    p_bri = sub.add_parser("brightness", help="Set brightness 0-255")
    _add_port_arg(p_bri)
    p_bri.add_argument("level", type=int)
    p_bri.set_defaults(func=cmd_brightness)

    p_anim = sub.add_parser("animation", help="Play built-in animation id 0-255")
    _add_port_arg(p_anim)
    p_anim.add_argument("animation_id", type=int)
    p_anim.set_defaults(func=cmd_animation)

    p_gif = sub.add_parser("gif", help="Upload a GIF file")
    _add_port_arg(p_gif)
    p_gif.add_argument("path")
    p_gif.set_defaults(func=cmd_gif)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args))
    except ImportError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    except (TransportError, OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
