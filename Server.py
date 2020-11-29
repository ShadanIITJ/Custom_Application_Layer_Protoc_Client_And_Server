import socket
sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind(('127.0.0.1',12345))

#####################  DataBase Connections  ####################
import sys
sys.path.append("C:\Shadan\3rd_Year\computer_network\Assignment_2")
from database import *
db = connect()
##################################################################

def client_data_parser(data):
  data = data.split("\r\n")
  method = data[0].split(",")[0]
  content_type = data[-2][-4:]
  f_data = data[-1]
  dic ={}
  if(content_type=="json"):
    temp = f_data.split("&")
    for k in temp:
      kv = k.split("=")
      dic[kv[0].lower()]=kv[1]
  else:
    pass
  #print(method)
  #print(content_type)
  #print(dic)
  ######### use database to return data ##########

  if(method.lower()=='pull'):
    try:
      aa = get_by_email(db,dic["email"])
      if(aa == None):
        return("No Data Available For This Email","OK","text")
      r_data = f"name={aa[1]}&email={aa[0]}&phone={aa[4]}&profession={aa[3]}&address={aa[2]}"
      return(r_data,"OK","json")
    except:
      return("Insufficient data for performing PULL, Provide email","OK","text")
  
  elif(method.lower()=='insert'):
    # data = [email,name,address,profession,phoen]
    try:
      l = [dic['email'],dic['name'],dic['address'],dic['profession'],dic['phone']]
      aa = insert(db,l)
      return(aa,"OK","text")
    except:
      return("Insufficient data, Require Following to execute ,[email, name, address, profession, phone]","OK","text")
  
  elif(method.lower()=='update'):
    # data = [name,address,profession,phoen]
    try:
      l = [dic['name'],dic['address'],dic['profession'],dic['phone']]
      email = dic["email"]
      aa = update(db,email,l)
      if(aa==None):
        message = f'No such entry exist for {email} user insert method to create the table'
        return(message,"OK","text")
      return(aa,"OK","text")
    except:
      return("Insufficient data, Require Following to execute \n[email, name, address, profession, phone] \n Note Email is The primary key","OK","text")

  elif(method.lower()=='delete'):
    # data = email
    try:
      email = dic["email"]
      aa = delete(db,email,True)
      return(aa,"OK","text")
    except:
      return("Insufficient data, Require Email","OK","text")
  else:
    return("Can't recognize Method","OK","text")
      



def return_data_for_client(parsed_data):
  msg=""
  if(parsed_data[1].lower()=='ok'):
    msg = "Sped/1.1 200 OK\r\n"
    if(parsed_data[2].lower()=='json'):
      msg+= "content-type:json\r\n"
    else:
      msg+= "content-type:text\r\n"
    msg+= parsed_data[0]
  elif(parsed_data[1].lower()=='notfound'):
    msg = "Sped/1.1 200 NotFound\r\n"
    msg+= "content-type:text\r\n"
    msg+= parsed_data[0]
  else:
    msg = "Sped/1.1 200 OK\r\n"
    msg+= "content-type:text\r\n"
    msg+= parsed_data[0]
  return msg




while True:
  print("Waiting for connection ...")
  data ,addr = sock.recvfrom(4096)
  print("Coneected to ",addr)
  try:
    parsed_data = client_data_parser(data.decode())
    msg = return_data_for_client(parsed_data)
    sock.sendto(msg.encode(), addr)
  except:
    continue
  