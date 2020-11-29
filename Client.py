import socket
import sys
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# sys.path.append('C:/Shadan/3rd_Year/computer_network/Assignment_2')
# import Server
# input will be Pull -f=json -d=name=gaurav&phone=1234567890

def create_message(inp):
    inp = inp.split(" ")
    msg=""
    if(inp[0].lower()=='pull'):
        msg="pull,Sped/1.1\r\n"
        if(inp[1][3:].lower()=='json'):
            msg+="encoding:utf-8\r\ncontent-type:json\r\n"
            data = inp[2][3:]
            msg+=data
    elif(inp[0].lower()=='insert'):
        msg="insert,Sped/1.1\r\n"
        if(inp[1][3:].lower()=='json'):
            msg+="encoding:utf-8\r\ncontent-type:json\r\n"
            data = inp[2][3:]
            msg+=data
    elif(inp[0].lower()=='update'):
        msg="update,Sped/1.1\r\n"
        if(inp[1][3:].lower()=='json'):
            msg+="encoding:utf-8\r\ncontent-type:json\r\n"
            data = inp[2][3:]
            msg+=data
    elif (inp[0].lower() == 'delete'):
        msg = "delete,Sped/1.1\r\n"
        if (inp[1][3:].lower() == 'json'):
            msg += "encoding:utf-8\r\ncontent-type:json\r\n"
            data = inp[2][3:]
            msg += data
    
    return msg

#m = create_message("Pull -f=json -d=name=gaurav&phone=1234567890")
#print(m)
#
#aa = Server.return_data_for_client(Server.client_data_parser(m))
#print(aa)


def decode_message(rec):
    rec=rec.split("\r\n")
    if(rec[0][-2:].lower()=='ok'):
        msg=""
        if(rec[1][-4:].lower()=='json'):
            dic ={}
            temp = rec[-1].split("&")
            for k in temp:
                kv = k.split("=")
                dic[kv[0]]=kv[1]

            msg=dic
        else:
            msg = rec[-1]
        return  msg
    elif(rec[0][-8:].lower()=='notfound'):
        return rec[-1]


#print(decode_message("Sped/1.1 200 NotFound\r\ncontent-type:text\r\nname=Gaurav&email=hello@gm&home=some_val&profeson=Faculty&contact=75654446780"))
#print(decode_message(aa))



def genrate_help(inp):
    if len(inp)==4:
        msg="Sped Client, Version 1.1\r\nThese shell commands are defined internally. Type `help' to see this list\r\nType `help name' to find out more about the function `name'\r\n"
        print(msg)
        msg ="function [Argument] ....\r\npull [-f] [-d] \t '-f'=format '-d'=data >\r\ninsert [-f] [-d]" \
             "\t '-f'=format '-d'=data\r\nupdate [-f] [-d]" \
             "\t '-f'=format '-d'=data\r\nexit  .............\n"
        print(msg)
        return
    if len(inp)>4:
        wrds=inp.split(' ')
        if (wrds[1].lower()=="pull"):
            msg="Pull: pull [-f] [-d]\r\n\tThis command help you to retrieve data from your depending upon email id of the user\n\n\tOption/Arguments:\n\t  -f\t\tHelp to decide format of the data , ex=('Json','text')\n\t  -d\t\tassign the data to create query\n\n\tData Format:\n\t 'email'='abc@xyz.com'"
            print(msg)
            return
        if (wrds[1].lower()=="insert"):
            msg="Insert: insert [-f] [-d]\r\n\tThis command enables you to enter data in your database \n\n\tOption/Arguments:\n\t  -f\t\tHelp to decide format of the data , ex=('Json','text')\n\t  -d\t\tassign the data to create query\n\n\tData Format:\n\t Email='abc@xyz.com'&Name='your name'&Address='your Address'&Profession='your profession'&Phone_Number='Your PhoneNo'"
            print(msg)
            return
        if (wrds[1].lower() == "update"):
            msg = "Update: update [-f] [-d]\r\n\tThis command enables you to update your entries in Database from your email(PK)  \n\n\tOption/Arguments:\n\t  -f\t\tHelp to decide format of the data , ex=('Json','text')\n\t  -d\t\tassign the data to create query\n\n\tData Format:\n\t key='new value'&email='abc@xyz.com'"
            print(msg)
            return
        if (wrds[1].lower() == "delete"):
            msg = "Delete: delete [-f] [-d]\r\n\tThis command helps you to delete record according to your email \n\n\tOption/Arguments:\n\t  -f\t\tHelp to decide format of the data , ex=('Json','text')\n\t  -d\t\tassign the data to create query\n\n\tData Format:\n\t email='abc@xyz.coms'"
            print(msg)
            return
        if (wrds[1].lower() == "exit"):
            msg = "Exit: \r\n\tCloses your system \n"
            print(msg)
            return


def Activate_Connection():
    # input formate / pull -f='json' -d='key:value';
    
    print("Sped Client>",end="")
    inp = input("")
    
    if(len(inp)==0):
        return Activate_Connection()
    
    if(inp[0:4].lower()=='exit'):
        sys.exit()

    if (inp[0:4].lower()=='help'):
        genrate_help(inp.rstrip())
        Activate_Connection()
    
    messgae_for_server = create_message(inp)
    print("message being sent is :-- ")
    print(messgae_for_server)

    sock.sendto(messgae_for_server.encode('utf-8'),('127.0.0.1',12345))
    data,addr=sock.recvfrom(4096)
    
    p_message=decode_message(data.decode())
    print("messgae received from serve is :-- ")
    print(p_message)
    Activate_Connection()
    





Activate_Connection()


