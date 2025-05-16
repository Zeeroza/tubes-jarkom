from socket import *
from strings import *

def handleClientRequest(conn: socket, addrTuple):
    ip, p = addrTuple
    try:
        request = conn.recv(1024).decode()

        filename = request.split()[1]

        print(f"{bcolors.HEADER}[R]{bcolors.ENDC} Trying to GET {bcolors.BOLD}{filename}{bcolors.ENDC}")

        if filename.endswith('/') or filename == '':
            res = open("static"+filename+"/index.html", encoding="utf8")
        elif filename.endswith('.jpg') or filename.endswith('.png') or filename.endswith('.svg'):
            res = open("static/"+filename[1:], 'rb')
            conn.sendall((getHttpOKHeader()).encode() + res.read())
            return
        else:
            res = open("static/"+filename[1:], encoding="utf8")
        print(f"{bcolors.OKCYAN}[R]{bcolors.ENDC} Sending {bcolors.OKGREEN}OK{bcolors.ENDC} Response back to {bcolors.OKCYAN}{ip}:{p}{bcolors.ENDC}")
        conn.sendall((getHttpOKHeader() + res.read() + "\r\n").encode())
    except IOError:
        res = open("static/404.html", encoding="utf8")
        print(f"{bcolors.OKCYAN}[R]{bcolors.ENDC} Sending {bcolors.WARNING}Not Found{bcolors.ENDC} Response back to {bcolors.OKCYAN}{ip}:{p}{bcolors.ENDC}")
        conn.sendall((getHttpNotFoundHeader() + res.read() + "\r\n").encode())
    except Exception as e:
        res = open("static/500.html", encoding="utf8")
        print(f"{bcolors.OKCYAN}[R]{bcolors.ENDC} Sending {bcolors.FAIL}Internal Server Error{bcolors.ENDC} Response back to {bcolors.OKCYAN}{ip}:{p}{bcolors.ENDC}")
        print(f"{bcolors.FAIL}[ERROR]{bcolors.ENDC} : {e}")
        conn.sendall((getHttpInternalServerErrorHeader() + res.read() + "\r\n").encode())
    finally:
        conn.close()