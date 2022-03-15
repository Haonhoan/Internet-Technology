import socket
import sys 
import select 
import time 


def server():
  try:
    ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("[S]: RS Server socket created")
  except socket.error as err:
    print('socket open error: {}\n'.format(err))
    exit()
  
  server_binding = ('', int(sys.argv[1]))
  ss.bind(server_binding)
  ss.listen(1)
  
  host = socket.gethostname()
  # print("[S]: Server host name is {}".format(host))
  localhost_ip = (socket.gethostbyname(host))
  print("[S]: Server IP address is {}".format(localhost_ip))
      
  while True: 
    # print("\nBEFORE ACCEPT: ")
    csockid, addr = ss.accept()
    print("[S]: RS Got a connection request from a client at {}".format(addr))

    # iterates per each line of query from client 
    while True:
      # print('\n\n----------- BASE LOOP -----------')
      data_from_client = csockid.recv(500).decode('utf-8')
      if not data_from_client:
        # print("*** no more data from client, closing connection")
        csockid.close()
        break
      data_from_client = data_from_client.strip() 
      
      try:
        TS1_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      except socket.error as err:
        print('socket open error: {} \n'.format(err))
        exit()
      TS1_port = int(sys.argv[3])
      TS1_binding = (sys.argv[2], TS1_port)
      TS1_socket.connect(TS1_binding)
      # print('* connected to TS1')
      
      try:
        TS2_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      except socket.error as err:
        print('socket open error: {} \n'.format(err))
        exit()
      TS2_port = int(sys.argv[5])
      TS2_binding = (sys.argv[4], TS2_port)
      TS2_socket.connect(TS2_binding)
      # print('* connected to TS2')
      
      TS1_socket.send(data_from_client.strip().encode('utf-8'))
      # print('* sent data to TS1')
      TS2_socket.send(data_from_client.strip().encode('utf-8'))
      # print('* sent data to TS2')
      
      answer = '' 
      answer_found = False
      inputs = [TS1_socket, TS2_socket]
      start = time.time()
      
      # print('\n')
      while True:
        # print("<SELECT LOOP>")
        if answer_found:
          # print("* found answer -- BREAK NON BLOCK LOOP!")
          break
        if time.time() - start > 5:
          # print("* TIMEOUT -- BREAK NON BLOCK LOOP!")
          break
        readers, writers, exceptional = select.select(inputs, [], [], 1)
        
        for reader in readers:
          # print("--- READER FOR LOOP ---")
          if reader is TS1_socket:
            data = TS1_socket.recv(300).decode('utf-8').strip() 
            if data != '':
              answer = data
              answer_found = True 
            # print('TS1 Socket received: ', data)
         
          elif reader is TS2_socket:
            data = TS2_socket.recv(300).decode('utf-8').strip()
            if data != '':
              answer = data
              answer_found = True 
            # print('TS2 Socket received: ', data)

        
      if not answer_found: 
        # print("*** TIME OUT!")
        time_out_msg = data_from_client.split(' ')[0] + ' - TIMED OUT'
        csockid.send(time_out_msg.encode('utf-8'))
        TS1_socket.close()
        TS2_socket.close()
      else: 
        # print("*** ANSWER FOUND! ==> ", answer)
        answer = answer + " IN"
        csockid.send(answer.encode('utf-8'))
        TS1_socket.close()
        TS2_socket.close()


if __name__ == "__main__":
    server()
