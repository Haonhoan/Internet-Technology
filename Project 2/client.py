import socket
import sys 

def client():
  try:
    cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("[C]: Client socket created")
  except socket.error as err:
    print('socket open error: {} \n'.format(err))
    exit()

  # Define the port on which you want to connect to the server
  port = int(sys.argv[2])
  host_addr = sys.argv[1]
  
  # connect to the server on local machine
  server_binding = (host_addr, port)
  cs.connect(server_binding)
  
  # read lines from file 
  file = open('PROJ2-HNS.txt', 'r')
  lines = file.readlines()
  lines = [line.strip() for line in lines]
  file.close()
  
  # print('lines: ', lines)
  print('\n')
  for line in lines:
    # raw_input('@Enter to Proceed: ')
    # print('\n* LINE to send: ', line)
    cs.send(line)
    # print('* sent line to RS')
    data_from_rs = cs.recv(300).decode('utf-8')
    data_from_rs = data_from_rs.strip() + "\n"
    # print('* received answer from RS: ', data_from_rs)
    file = open('RESOLVED.txt', 'a')
    file.write(data_from_rs)
    file.close()
    # print("END of LOOP")
  
  
  # close the client socket
  cs.close()
  exit()

if __name__ == "__main__":
  client()