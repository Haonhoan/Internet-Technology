import socket
import time


def client():
    try:
        cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[C]: Client socket created")
    except socket.error as err:
        print('socket open error: {} \n'.format(err))
        exit()

    # Define the port on which you want to connect to the server
    port = 50007
    localhost_addr = socket.gethostbyname(socket.gethostname())

    # connect to the server on local machine
    server_binding = (localhost_addr, port)
    cs.connect(server_binding)

    #Part - 5 File Import
    lines = []
    file1 = open("in-proj.txt", 'r')
    lines = file1.readlines()
    lines.insert(0, str(len(lines)))

    for line in lines:
        time.sleep(0.25)
        cs.sendall(line.encode('utf-8'))

    # close the client socket
    print("END")
    cs.close()
    exit()


if __name__ == "__main__":
    client()
