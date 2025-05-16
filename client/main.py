import os
import signal
from pygments import highlight
from pygments.lexers import HtmlLexer
from pygments.formatters import TerminalFormatter
from socket import *
from threading import *
import sys


if __name__ == '__main__':
    clientSocket = socket(AF_INET, SOCK_STREAM)

    server_host = sys.argv[1]
    server_port = sys.argv[2]
    filename = sys.argv[3]

    print(f"Connecting to {server_host}:{server_port} ...")
    clientSocket.connect((server_host, int(server_port)))

    print(f"Fetching file {filename} ...")
    clientSocket.send(f"GET /{filename} HTTP/1.1".encode())

    segment_chunks = []

    try:
        print(f"Waiting for response...")
        while True:
            html = clientSocket.recv(8192).decode()
            if not html:
                break
            segment_chunks.append(html)
    finally:
        html_content = "".join(segment_chunks)
        print(highlight(html_content, HtmlLexer(), TerminalFormatter()))
        # fallback
        # print("".join(segment_chunks))
        print(f"Closing Connection...")
        clientSocket.close()
