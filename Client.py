
import socket
import sys
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(5)# wait for 5 second to receive somethong back from server 13.89.206.2

setting_advanced = True

def can_convert_to_json(data):
    try:
        data = data.split("&")
        for i in data:
            j=i.split("=")
            if(len(j)!=2):
                raise Exception
        
        return True
    except:
        return False

def create_message(inp):
    inp = inp.split(" ")
    msg=None
    if(inp[0].lower()=='pull'):
        if(inp[-2][3:].lower()=='json' and can_convert_to_json(inp[-1][3:])):
            msg="pull,Sped/1.1\r\n"
            msg+="encoding:utf-8\r\ncontent-type:json\r\n"
            data = inp[-1][3:]
            msg+=data
        elif(inp[-2][3:].lower()=='text'):
            msg="pull,Sped/1.1\r\n"
            msg+="id:"+inp[1][4:]+"\r\n"
            msg+="encoding:utf-8\r\ncontent-type:text\r\n"
            data = inp[-1][3:]
            msg+=data
    elif(inp[0].lower()=='insert'):
        if(inp[-2][3:].lower()=='json' and can_convert_to_json(inp[-1][3:])):
            msg="insert,Sped/1.1\r\n"
            msg+="encoding:utf-8\r\ncontent-type:json\r\n"
            data = inp[-1][3:]
            msg+=data
    elif(inp[0].lower()=='update'):
        if(inp[-2][3:].lower()=='json' and can_convert_to_json(inp[-1][3:])):
            msg="update,Sped/1.1\r\n"
            msg+="encoding:utf-8\r\ncontent-type:json\r\n"
            data = inp[-1][3:]
            msg+=data
    elif(inp[0].lower()=='delete'):
        if(inp[-2][3:].lower()=='json' and can_convert_to_json(inp[-1][3:])):
            msg="delete,Sped/1.1\r\n"
            msg+="encoding:utf-8\r\ncontent-type:json\r\n"
            data = inp[-1][3:]
            msg+=data
    else:
        return None
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
        msg="\r\nSped Client, Version 1.1\r\nThese shell commands are defined internally. Type `help' to see this list\r\nType `help name' to find out more about the function `name'\r\nEnter Settings basic\ advanced to switch between settings\r\nEnter Exit to close the Client\r\n"
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
        elif (wrds[1].lower()=="insert"):
            msg="Insert: insert [-f] [-d]\r\n\tThis command enables you to enter data in your database \n\n\tOption/Arguments:\n\t  -f\t\tHelp to decide format of the data , ex=('Json','text')\n\t  -d\t\tassign the data to create query\n\n\tData Format:\n\t Email='abc@xyz.com'&Name='your name'&Address='your Address'&Profession='your profession'&Phone_Number='Your PhoneNo'"
            print(msg)
            return
        elif (wrds[1].lower() == "update"):
            msg = "Update: update [-f] [-d]\r\n\tThis command enables you to update your entries in Database from your email(PK)  \n\n\tOption/Arguments:\n\t  -f\t\tHelp to decide format of the data , ex=('Json','text')\n\t  -d\t\tassign the data to create query\n\n\tData Format:\n\t updated_keys=updates_values&email='abc@xyz.com'"
            print(msg)
            return
        elif (wrds[1].lower() == "delete"):
            msg = "Delete: delete [-f] [-d]\r\n\tThis command helps you to delete record according to your email \n\n\tOption/Arguments:\n\t  -f\t\tHelp to decide format of the data , ex=('Json','text')\n\t  -d\t\tassign the data to create query\n\n\tData Format:\n\t email='abc@xyz.coms'"
            print(msg)
            return
        else:
            return genrate_help("help")


def basic_settings(send_messge,recv_message):
    print("\nmessage being sent is :--- \n")
    print(send_messge)
    print("\nReceived Message is :---\n")
    print(recv_message)
    print("\n")

def Activate_Connection():
    # input formate / pull -f='json' -d='key:value';
    
    print("Sped Client> ",end="")
    inp = input("")
    
    if(len(inp)==0):
        return Activate_Connection()
    
    if(inp[0:4].lower()=='exit'):
        sys.exit()
    if (inp[0:4].lower()=='help'):
        genrate_help(inp.rstrip())
        Activate_Connection()
    if(inp[0:8].lower()=="settings"):
        temp = inp.split(" ")
        if(len(temp)==1):
            global setting_advanced
            if(setting_advanced):
                print("Advanced Mode")
            else:
                print("Basic Mode")
            Activate_Connection()
        if(temp[-1].lower()=="basic"):
            setting_advanced = False
        elif(temp[-1].lower()=="advanced"):
            setting_advanced=True
        else:
            print("No Such Setting Exist! ")
        Activate_Connection()

    messgae_for_server = create_message(inp)
    if(messgae_for_server==None):
        print("Received input cant be converted into the SPED Protocols| Try our Help command to Know more")
        return Activate_Connection()
    #print("message being sent is :-- ")
    #print(messgae_for_server)
    data=None
    addr=None

    try:
        sock.sendto(messgae_for_server.encode('utf-8'),('127.0.0.1',12345))
        data,addr=sock.recvfrom(4096)
    except socket.timeout or ConnectionResetError:
        print("Server is not responding...................")
        print("Try again! or Exit")
        return Activate_Connection()
    
    if(setting_advanced):
        p_message=decode_message(data.decode())
        #print("messgae received from serve is :-- ")
        print("\n")
        print(p_message)
        print("\n")
    else:
        basic_settings(messgae_for_server,data.decode())
    Activate_Connection()


if(__name__=="__main__"):
    print("\r\nWelcome TO SPED Client\r\nEnter help to know more\r\n")
    Activate_Connection()
