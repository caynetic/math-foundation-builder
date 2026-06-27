"""Start the local web app and open it in the default browser."""

from __future__ import annotations

import socket
import threading
import time
import urllib.request
import webbrowser

from werkzeug.serving import make_server

from web.app import create_app


def find_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


class ServerThread(threading.Thread):
    def __init__(self, host: str, port: int):
        super().__init__(daemon=True)
        self.host = host
        self.port = port
        self.app = create_app()
        self.server = make_server(host, port, self.app)

    def run(self) -> None:
        self.server.serve_forever()

    def shutdown(self) -> None:
        self.server.shutdown()


def wait_for_health(url: str, timeout_seconds: float = 10.0) -> None:
    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(f"{url}/health", timeout=0.5) as response:
                if response.status == 200:
                    return
        except OSError:
            time.sleep(0.1)
    raise RuntimeError(f"Local server did not become ready: {url}")


def main() -> None:
    host = "127.0.0.1"
    port = find_free_port()
    url = f"http://{host}:{port}"
    server = ServerThread(host, port)
    server.start()
    wait_for_health(url)
    webbrowser.open(url)

    try:
        print(f"Math Foundation Builder is running at {url}")
        print("Press Ctrl-C to stop the local server.")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        server.shutdown()


if __name__ == "__main__":
    main()
