"""可选的 stdio MCP 代理：原样转发消息，将副本写入本地日志。"""

import argparse
import subprocess
import sys
import threading
from datetime import datetime
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--log-file", type=Path, default=Path("mcp_io.log"))
    parser.add_argument("command", nargs=argparse.REMAINDER, help="服务启动命令及参数")
    args = parser.parse_args()
    command = args.command
    if command and command[0] == "--":
        command = command[1:]
    if not command:
        parser.error("需要提供 MCP 服务启动命令。")

    lock = threading.Lock()
    with args.log_file.open("a", encoding="utf-8") as log:
        process = subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=sys.stderr,
            bufsize=0,
        )

        def forward(source, destination, direction):
            try:
                for line in iter(source.readline, b""):
                    destination.write(line)
                    destination.flush()
                    with lock:
                        log.write(
                            f"[{datetime.now().isoformat()}] {direction}: "
                            f"{line.decode('utf-8', errors='replace').rstrip()}\n"
                        )
                        log.flush()
            except (BrokenPipeError, OSError) as exc:
                print(f"MCP 代理转发结束：{exc}", file=sys.stderr)
            finally:
                if direction == "client -> server":
                    destination.close()

        incoming = threading.Thread(
            target=forward,
            args=(sys.stdin.buffer, process.stdin, "client -> server"),
            daemon=True,
        )
        outgoing = threading.Thread(
            target=forward,
            args=(process.stdout, sys.stdout.buffer, "server -> client"),
            daemon=True,
        )
        incoming.start()
        outgoing.start()
        try:
            return_code = process.wait()
            outgoing.join(timeout=2)
            return return_code
        finally:
            if process.poll() is None:
                process.terminate()
                try:
                    process.wait(timeout=2)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait()


if __name__ == "__main__":
    raise SystemExit(main())
