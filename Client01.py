import socket

ClientSocket = socket.socket()
host = '127.0.0.1'
port = 1233

print('Waiting for connection')
try:
    ClientSocket.connect((host, port))
    print("Connected to Server...")
except socket.error as e:
    print(str(e))

##Response = ClientSocket.recv(1024)
while True:
##    print("1.Send Message\n2.Receive Message")
##    operation = input("Enter the operation you want to perform:")
##    if(operation == "1"):
##        Input = input()
##        ClientSocket.send(str.encode(Input))    
##    elif(operation == "2"):
##        Response = ClientSocket.recv(1024)
##        print(Response.decode('utf-8'))
##    else:
##        print("Enter Valid Operation")
    while True:
        Response = ClientSocket.recv(1024)
        received_message = Response.decode('utf-8')
        if(received_message == "Input"):
##            print("Over")
            break
        else:
##            print("Received :")
            print(received_message)
    Input = input("Enter the Data:")
    ClientSocket.send(str.encode(Input))
ClientSocket.close()
