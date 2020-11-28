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



def Activate_Connection():
    # input formate / pull -f='json' -d='key:value';
    
    print("Sped Client>",end="")
    inp = input("")
    
    if(len(inp)==0):
        return Activate_Connection()
    
    if(inp[0:4].lower()=='exit'):
        sys.exit()
    
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


