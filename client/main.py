# remove unused imports
# import os
# import signal
# from threading import *

# import pygments for syntax highlighting
from pygments import highlight
from pygments.lexers import HtmlLexer
from pygments.formatters import TerminalFormatter

# import socket for connecting to the server
from socket import *

# import sys for command line arguments
import sys

# check if the script is run as the main module
if __name__ == '__main__':
    # Socket type, SOCK_STREAM for TCP
    clientSocket = socket(AF_INET, SOCK_STREAM)

    # 3 params needed for this script to run, mainly server host, port and filename
    server_host = sys.argv[1]
    server_port = sys.argv[2]
    filename = sys.argv[3]

    # connect to the server
    print(f"Connecting to {server_host}:{server_port} ...")
    clientSocket.connect((server_host, int(server_port)))

    # send the GET request to the server
    print(f"Fetching file {filename} ...")
    clientSocket.send(f"GET /{filename} HTTP/1.1".encode())

    # initialize a list to store the received HTML segments 
    segment_chunks = []

    try:
        print(f"Waiting for response...")
        while True:
            # receive data from the server in chunks, exactly 8192 bytes at a time
            html = clientSocket.recv(8192).decode()
            # if the html is finished, break the loop 
            if not html:
                break
            # append the received HTML segment to the list
            segment_chunks.append(html)
    finally:
        # join all the received HTML segments into a single string
        html_content = "".join(segment_chunks)
        # print the received HTML content with syntax highlighting
        print(highlight(html_content, HtmlLexer(), TerminalFormatter()))

        # fallback
        # print("".join(segment_chunks))

        # print a message indicating the end of the response & close the connection
        print(f"Closing Connection...")
        clientSocket.close()
