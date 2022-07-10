## @package Multiple Client Server Module Using Multithreading
#  This module consist of Server Code that can handle multiple customers(clients) at the same time for the Shopping Mall based Model.
#  The Customers will be provided with the Interface with which they can select multiple operations and also choose the shop they want to go and by using the current data if any (or will be created) they will be provided with suggestion regarding the next shop they should visit.
#  More details.
import random
import csv
import os
import socket
import threading
import socket
import time
from _thread import *

host = '127.0.0.1'
port = 1233
ThreadCount = 0
    
TOTAL_USERS = 0
user_data = []
MAX_SHOP = 5
CURRENT_SHOP = 0
client_connection = 0

## Class named User consist of all the Methods that are required for the handling of Clients and all the data calculations required for the suggestions that will be provided to the customer.
#
#  More details.
class user():

    ## The constructor.
    def __init__(self,username):
      self.name = username
      self.new_user(username)
      self.start_server(host, port)
      CURRENT_SHOP = 0
      if(os.path.exists("customer.csv")):
          if(os.stat("customer.csv").st_size == 0):
              print("Data Created\n")
              self.create_data()
              
      else:
          file = open("customer.csv","a")
          self.create_data()
          file.close()
          
    ## Run Method handle or provide with the Operation List that can be performed in order to choose the shop customer would like to go next or taking suggestions and also see their current path of shops they visited.
    #  @param self The object pointer.  
    def run(self):
      
      self.send_data("Welcome to shopping Mall\n")
      while 1:
        self.send_data("1. Suggestion\n" + "2. Choose your shop\n" + "3. Print User Data\n"+"4. Exit\n")
        self.send_data("Enter the operation you want to perform\n")
        time.sleep(0.5)
        self.send_data("Input")
        operation = self.receive_data()        
        print("The given operation value is :%s\n"%operation)
        if(operation == "1"):
            self.suggestion()
        elif(operation == "2"):
            self.append_list()
        elif(operation == "3"):
            self.print_list()
        elif(operation == "4"):
          quit()
        else:
          print("Continue\n")
          continue

    ## Create Data generates random data that will be further useful for the suggestion.
    #  @param self The object pointer.     
    def create_data(self):
        name_list = ["Name","shop1","shop2","shop3","shop4","shop5"]
        data_list = ["Nike","addidas","Puma","Skechers","Bata"]
        customer_name = ["Devanshu","Naitik","Vraj","OM","Manthan"]
        file = open("customer.csv","a")
        wrt = csv.writer(file)
        wrt.writerow(name_list)
        for i in range(5):
            final_list = []
            random.shuffle(data_list)
            final_list.append(customer_name[i])
            final_list = final_list + data_list
            print(final_list)
            wrt.writerow(final_list)
        file.close()

    ## New User creates the New User and Save its Name in New User DataBase.
    #  @param self The object pointer.
    #  @param user_name The Name Entered by User
    def new_user(self,user_name):
      user_data.append(user_name)
      print("New User Created\n")

    ## Append List let User to choose the next shop that user want to visit and than once User has visited all the shop once it stores it into the DataBase it also let user know that same shop donot get repeated.
    #  @param self The object pointer.   
    def append_list(self):
        global CURRENT_SHOP
        data_list = ["Nike","addidas","Puma","Skechers","Bata"]
        self.send_data(" 1. Nike\n 2. addidas\n 3. Puma\n 4. Skechers\n 5. Bata\n")
        self.send_data("Enter the shop you want to go\n")
        time.sleep(0.5)
        self.send_data("Input")
        shop = self.receive_data()
        for data in user_data:
            if(data is data_list[int(shop)-1]):
                print("You already visited shop\n")
                return 0
        user_data.append(data_list[int(shop)-1])
        CURRENT_SHOP += 1
        if(len(user_data) == (MAX_SHOP + 1)):
            file = open("customer.csv","a")
            wrt = csv.writer(file)
            wrt.writerow(user_data)
            file.close()
            exit()
            
    ## Suggestion uses the current user data and compares it within the DataBase and it return suggestion list on the basis of patter matching.
    #  @param self The object pointer.
    def suggestion(self):
        sug_list = []
        if(CURRENT_SHOP >= 2):
            file = open('customer.csv', 'r')
            customer_data = csv.reader(file,delimiter=",")
            sug_list = self.data_match(customer_data)
            self.send_data(str(sug_list)+'\n')
        else:
            print("!!!!You are not eligible for the suggestions!!!!\n")

    ## Row Count returns the total number of users present in the DataBase.
    #  @param self The object pointer.
    def row_count(self):
        row_count = 0
        print("Row Count Function\n")
        f = open("customer.csv", "r")
        reader = csv.reader(f, delimiter=",")
        for l in reader:
            row_count += 1
        f.close()
        return row_count

    ## Data Match does pattern matching with the exisiting Data Base in order to find the next shop user should visit.
    #  @param self The object pointer.
    #  @param customer_data The List of the Exisiting Customer Data
    def data_match(self,customer_data):
        print("<======data match====>\n")
        ## A class variable.
        match = 0
        ## A class variable.
        avoid_name = 0
        ## A class variable.
        avoid_heading = 0
        suggestion_list = []
        user_shop = 0
        total_user = self.row_count()
        for list in customer_data:
            print(list)
            avoid_name = 0
            match = 0
            user_shop = 0
            if(avoid_heading != 0):
                #<=======For List for Number of Shops=======>
                for shop in list:
                    if(avoid_name != 0):
                        if(user_shop < (len(user_data)-1)):
                            if(shop == user_data[user_shop+1]):
                                match += 1
                        user_shop +=1
                    avoid_name = 1
                if(match == (len(user_data)-1)):
                    print(list)
                    suggestion_list.append(list)
                    
            print("match:",match)        
            print("avoid heading 1\n")
            avoid_heading = 1
        return suggestion_list

    ## Print_list prints the current list of the shops that user has visited.
    #  @param self The object pointer.       
    def print_list(self):
        print(user_data)
        self.send_data(str(user_data)+'\n')

    ## client_handler informs the client that is now connected and furhter start the run process.
    #  @param self The object pointer.
    #  @param connection The Socket Connection
    def client_handler(self,connection):
        connection.send(str.encode('You are now connected to the replay server... Type BYE to stop\n'))
        self.run()       

    ## accept_connection accepts the connection that is requested by every new client.
    #  @param self The object pointer.
    #  @param ServerSocket The Socket on which request will be initiated
    def accept_connections(self,ServerSocket):
        Client, address = ServerSocket.accept()
        print('Connected to: ' + address[0] + ':' + str(address[1]))
        global client_connection
        client_connection = Client
        start_new_thread(self.client_handler, (Client, ))
        
    ## start_server bind the port on which the communication between server and client will take place.
    #  @param self The object pointer.
    #  @param host The Host ID.
    #  @param port The Port on which communication will take place.
    def start_server(self,host, port):
        ServerSocket = socket.socket()
        try:
            ServerSocket.bind((host, port))
        except socket.error as e:
            print(str(e))
        print(f'Server is listing on the port {port}...')
        ServerSocket.listen()

        while True:
            self.accept_connections(ServerSocket)
            
    ## send_data will send the data on the connected client.
    #  @param self The object pointer.
    #  @param message The data to be sent to client.
    def send_data(self,message):
        global client_connection
        client_connection.send(str.encode(message))

    ## receive_data receives the data that is being send by client.
    #  @param self The object pointer.
    def receive_data(self):
        global client_connection
        data = client_connection.recv(2048)
        message = data.decode('utf-8')
        return message
    ## @var name
    #  a member variable
    
## main fundtion consist of the initialising the user module and taking user name as input.
#  .
def main():
    customer = input("Enter Name of the user:")
    new_user = user(customer)

main()





