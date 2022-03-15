import socket
from termios import CSIZE
import time


def server():
    try:
        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[S]: Server socket created")
    except socket.error as err:
        print('socket open error: {}\n'.format(err))
        exit()

    server_binding = ('', 50007)
    ss.bind(server_binding)
    ss.listen(1)
    host = socket.gethostname()
    print("[S]: Server host name is {}".format(host))
    localhost_ip = (socket.gethostbyname(host))
    print("[S]: Server IP address is {}".format(localhost_ip))
    csockid, addr = ss.accept()
    print("[S]: Got a connection request from a client at {}".format(addr))

    data_from_client = csockid.recv(1024)
    data_from_client = data_from_client.decode('utf-8')

    count = int(data_from_client)

    reversed_lines = []
    for x in range(0, count):
        data_from_client = csockid.recv(1024)
        data_from_client = data_from_client.decode('utf-8')

        reversed_string = data_from_client[::-1]
        reversed_lines.append(reversed_string)

    #reversed_lines.append('')

    file2 = open("out-proj.txt", "w")
    file2.writelines(reversed_lines)

    # Close the server socket
    print("END")
    ss.close()
    exit()


if __name__ == "__main__":
    server()
