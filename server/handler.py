from socket import *
from strings import *

def handleClientRequest(conn: socket, addrTuple):
    ip, p = addrTuple
    try:
        request = conn.recv(1024).decode()

        filename = request.split()[1]

        print(f"{bcolors.HEADER}[R]{bcolors.ENDC} Trying to GET {bcolors.BOLD}{filename}{bcolors.ENDC}")

        if filename == '/' or filename == '':
            res = open("static/index.html", encoding="utf8")
        else:
            res = open("static/"+filename[1:], encoding="utf8")
        print(f"{bcolors.OKCYAN}[R]{bcolors.ENDC} Sending {bcolors.OKGREEN}OK{bcolors.ENDC} Response back to {bcolors.OKCYAN}{ip}:{p}{bcolors.ENDC}")
        conn.sendall((getHttpOKHeader() + res.read() + "\r\n").encode())
    except IOError:
        res = open("static/404.html", encoding="utf8")
        print(f"{bcolors.OKCYAN}[R]{bcolors.ENDC} Sending {bcolors.WARNING}Not Found{bcolors.ENDC} Response back to {bcolors.OKCYAN}{ip}:{p}{bcolors.ENDC}")
        conn.sendall((getHttpNotFoundHeader() + res.read() + "\r\n").encode())
    except Exception:
        res = open("static/500.html", encoding="utf8")
        print(f"{bcolors.OKCYAN}[R]{bcolors.ENDC} Sending {bcolors.FAIL}Internal Server Error{bcolors.ENDC} Response back to {bcolors.OKCYAN}{ip}:{p}{bcolors.ENDC}")
        conn.sendall((getHttpInternalServerErrorHeader() + res.read() + "\r\n").encode())
    finally:
        conn.close()