import os
import signal
from handler import *
from strings import bcolors
from socket import *
from threading import *
import sys


SERVER_ADDRESS = gethostbyname(gethostname())
SERVER_PORT = 8000
MAX_BACKLOG = 5

serverSocket = socket(AF_INET, SOCK_STREAM)

serverSocket.bind((SERVER_ADDRESS, SERVER_PORT))
serverSocket.listen(MAX_BACKLOG)
serverSocket.settimeout(1.0)

if __name__ == "__main__":
    print(f"{bcolors.OKBLUE}[*]{bcolors.ENDC} Servers Are UP! {bcolors.OKCYAN}({SERVER_ADDRESS}:{SERVER_PORT}){bcolors.ENDC}")
    try:
        while True:
            try:
                conn, addrTuple = serverSocket.accept()
                ip, a = addrTuple
                print(f"{bcolors.OKGREEN}[V]{bcolors.ENDC} Connection established with {bcolors.OKCYAN}{ip}:{a}{bcolors.ENDC}")
                threader = Thread(target=handleClientRequest, args=(conn, addrTuple))
                threader.daemon = True
                threader.start()
            except timeout:
                continue
    except Exception as e:
        print(f"{bcolors.FAIL}[X] Error: {e} {bcolors.ENDC}")
    except KeyboardInterrupt:
        print(f"{bcolors.WARNING}[-]{bcolors.ENDC} Server interrupted")
        pass
    finally:
        serverSocket.close()
        sys.exit()