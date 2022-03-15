import socket
import signal
import sys
import random

# Read a command line argument for the port where the server
# must run.
port = 8080
if len(sys.argv) > 1:
    port = int(sys.argv[1])
else:
    print("Using default port 8080")

# Start a listening server socket on the port
sock = socket.socket()
sock.bind(('', port))
sock.listen(2)

### Contents of pages we will serve.
# Login form
login_form = """
   <form action = "http://localhost:%d" method = "post">
   Name: <input type = "text" name = "username">  <br/>
   Password: <input type = "text" name = "password" /> <br/>
   <input type = "submit" value = "Submit" />
   </form>
""" % port
# Default: Login page.
login_page = "<h1>Please login</h1>" + login_form
# Error page for bad credentials
bad_creds_page = "<h1>Bad user/pass! Try again</h1>" + login_form
# Successful logout
logout_page = "<h1>Logged out successfully</h1>" + login_form
# A part of the page that will be displayed after successful
# login or the presentation of a valid cookie
success_page = """
   <h1>Welcome!</h1>
   <form action="http://localhost:%d" method = "post">
   <input type = "hidden" name = "action" value = "logout" />
   <input type = "submit" value = "Click here to logout" />
   </form>
   <br/><br/>
   <h1>Your secret data is here:</h1>
""" % port

#### Helper functions
# Printing.
def print_value(tag, value):
    print "Here is the", tag
    print "\"\"\""
    print value
    print "\"\"\""
    print

# Signal handler for graceful exit
def sigint_handler(sig, frame):
    print('Finishing up by closing listening socket...')
    sock.close()
    sys.exit(0)
# Register the signal handler
signal.signal(signal.SIGINT, sigint_handler)


# TODO: put your application logic here!
# Read login credentials for all the users
# Read secret data of all the users
def handle_cookie(headers, cookie_dict):
  username = '' 
  header_lines = headers.split("\r\n")
  header_lines = [i.strip() for i in header_lines]
  validCookieFound = False
  validToken = ''
  cookieExists = False
  for index, line in enumerate(header_lines):
    if index == 0: continue
    header_field = line.split(":")
    header_key = header_field[0].strip()
    header_value = header_field[1].strip()
    if header_value[-1] == ";":
      header_value = header_value[0:-1]
    
    if header_key == "Cookie":
      cookieExists = True
      token_value = header_value.split('=')[1]
      if token_value in cookie_dict:
        print "\n * Valid Cookie Found! \n"
        validCookieFound = True
        validToken = token_value
        username = cookie_dict[token_value]
    else:
      username = '' 
  return username, validCookieFound, validToken, cookieExists

def handle_body(body):
  user_credentials = {
    "username": '',
    "password": ''
  }
  isLogout = False
  if body == "":
    return user_credentials, isLogout
  
  body_fields = body.split("&")
  for field in body_fields:
    field_key = field.split("=")[0] 
    field_value = field.split("=")[1]
    if field_key == "username":
      user_credentials["username"] = field_value
    elif field_key == "password":
      user_credentials["password"] = field_value
    elif field_key == "action" and field_value == "logout":
      isLogout = True
  return user_credentials, isLogout


password_dict = {}
secret_dict = {}
cookie_dict = {}

file = open("passwords.txt", "r")
password_lines = file.readlines()
password_lines = [line.strip() for line in password_lines if len(line.strip()) != 0]
for line in password_lines: 
  arr = line.strip().split(" ")
  password_dict[arr[0]] = arr[1]
file.close()

file = open("secrets.txt", "r")
secret_lines = file.readlines()
secret_lines = [line.strip() for line in secret_lines if len(line.strip()) != 0]
for line in secret_lines:
  arr = line.strip().split(" ")
  secret_dict[arr[0]] = arr[1]
file.close()

# print "password_dict: ", password_dict
# print "secret_dict: ", secret_dict



### Loop to accept incoming HTTP connections and respond.
while True:
    client, addr = sock.accept()
    req = client.recv(1024)
    
    print("\n\n----------------- LOOP --------------------------------------------------------------------")

    # Let's pick the headers and entity body apart
    header_body = req.split('\r\n\r\n')
    headers = header_body[0]
    body = '' if len(header_body) == 1 else header_body[1]
    print_value('headers', headers)
    print_value('entity body', body)

    # TODO: Put your application logic here!
    # Parse headers and body and perform various actions
    SUCCESS = "SUCCESS"
    BAD_CRED = "BAD_CRED"
    LOGIN = "LOGIN"
    LOGOUT = "LOGOUT"
    status_code = None
    
    validCookieFound = False 
    isLogout = False
    username = ''
    password = ''
    
    username, validCookieFound, validToken, cookieExists = handle_cookie(headers=headers, cookie_dict=cookie_dict)
    print "cookieExists: ", cookieExists
    
    user_credentials, isLogout = handle_body(body=body)
    if username == "":
      username = user_credentials["username"]
    password = user_credentials["password"] 
    
    html_content_to_send = bad_creds_page
    status_code = BAD_CRED
    
    if isLogout:
      html_content_to_send = logout_page
      status_code = LOGOUT
    elif len(username) == 0 and len(password) == 0:
      if cookieExists and not validCookieFound:
        html_content_to_send = bad_creds_page
        status_code = BAD_CRED
      elif not cookieExists:
        html_content_to_send = login_page
        status_code = LOGIN
    elif (username in password_dict and password_dict[username] == password):
      if cookieExists:
        if not validCookieFound:
          html_content_to_send = bad_creds_page
          status_code = BAD_CRED
        elif validCookieFound: 
          html_content_to_send = success_page + secret_dict[username]
          status_code = SUCCESS
      elif not cookieExists:
        html_content_to_send = success_page + secret_dict[username]
        status_code = SUCCESS
    elif validCookieFound:
      html_content_to_send = success_page + secret_dict[username]
      status_code = SUCCESS
    
    
    print "\n* status_code: " + status_code + "\n"
      
    # html_content_to_send = login_page
    # html_content_to_send = success_page + <secret>
    # html_content_to_send = bad_creds_page
    # html_content_to_send = logout_page
    
    # (2) `headers_to_send` => add any additional headers
    headers_to_send = ''
    
    if status_code == SUCCESS and not validCookieFound:
      rand_val = random.getrandbits(64)
      cookie_dict[str(rand_val)] = username
      headers_to_send = "Set-Cookie: token=" + str(rand_val) + "\r\n"
    
    if status_code == LOGOUT:
      cookie_dict.pop(validToken, None)
      headers_to_send = "Set-Cookie: token=; expires=Thu, 01 Jan 1970 00:00:00 GMT\r\n"
    
    print "cookie_dict: ", cookie_dict

    # Construct and send the final response
    response  = 'HTTP/1.1 200 OK\r\n'
    response += headers_to_send
    response += 'Content-Type: text/html\r\n\r\n'
    response += html_content_to_send
    print_value('response', response)    
    client.send(response)
    client.close()
    
    print "Served one request/connection!"
    print

# We will never actually get here.
# Close the listening socket
sock.close()
