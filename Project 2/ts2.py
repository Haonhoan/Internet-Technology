import socket
import sys 


def server():
  # read file and pouplate dns_record_list
  dns_record_list = []
  file = open('PROJ2-DNSTS2.txt', 'r')
  lines = file.readlines()
  for line in lines:
    dns_record_list.append(line.strip())
  
  try:
    ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("[S]: TS2 Server socket created")
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
    print("[S]: TS2 Got a connection request from a client at {}".format(addr))

    data_from_rs = csockid.recv(500).decode('utf-8')
    data_from_rs = data_from_rs.strip()
    # print("* data_from_rs: ", data_from_rs)
    
    for record in dns_record_list:
      arr = record.strip().split(' ')
      domain_name = arr[0];
      # print('@each domain_name: ', domain_name)
      
      record_not_found = True 
      if domain_name.lower() == data_from_rs.lower():
        # print('* record found! ==> ', record)
        record_not_found = False
        csockid.send(record.strip().encode('utf-8'))
    
    # if record_not_found: 
    #   print('* record NOT found!')
    
    csockid.close()       


if __name__ == "__main__":
  server()