from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
import threading
import re
import datetime,time
import json

lock = threading.RLock()
thread_dict={}


def process_client(client,addr):
	print "CLIENT JUST IN FUNCTION START"
	send_addr=(client,addr)
	print client.getsockname()
	global lock
	global thread_dict
	data_buf=""
	print client
	while True:
		data = client.recv(50)
		#print "Client sent: " + data
		data_buf+=data
		if not data: break
	   
	print "DATA BUFFER"
	print data_buf
	print client


	url_dict=process_request_data(data_buf)
	print "URL DICT"
	print url_dict
	if url_dict['type']=="sleep":
		print "REQUEST TYPE : SLEEP"
		print "CLIENT ADDRESS"
		print client
		print "Acquiring lock for Thread in Sleep " 
		
		lock.acquire()
		if thread_dict.has_key(url_dict['args']['connid']):
			
			lock.release()
			return
		else:
			thread_dict[url_dict['args']['connid']]={}
			thread_dict[url_dict['args']['connid']]['threadID']=threading.current_thread()
			thread_dict[url_dict['args']['connid']]['starttime']=datetime.datetime.now()
			timeout=int(url_dict['args']["timeout"])
			lock.release()
		
		
			print "THREAD DICT"
			print thread_dict
			print "Sleeping for %s milliseconds" %str(timeout)
        #client.send()
			import time
			time.sleep(timeout)

			print " Terminating "
			print url_dict['args']['connid']
			
			print "Releasing lock for Thread in Sleep %s" %str(thread_dict[url_dict['args']['connid']])
			lock.acquire()
			del thread_dict[url_dict['args']['connid']]
			
			lock.release()
			print "Sending back data HELLO"
			print client
			print dir(client)
			print send_addr[0]
			print client.getsockname()
			client.sendall("Hey")
			#socket.sendto("hello",send_addr)
			print "DATA HELLO SENT TO CLIENT"
	elif url_dict['type']=="server-status":
		print "REQUEST TYPE : SERVER STATUS"
		now=datetime.datetime.now()
		print "ThreadID, Remaining Sleep Time"
		print "Acquiring lock for Thread in Server Status " 
		
		lock.acquire()
		print thread_dict
		for elem in thread_dict:
			print elem,now-thread_dict[elem]['starttime']
		print "Releasing lock for Thread in Server Status " 
		lock.release()
			#print k,now-v['starttime']
		#client.close()
	elif url_dict['type']=="kill":
		lock.acquire()
		tid=thread_dict[url_dict['args']['connid']]
		print "Stopping the thread"
		print tid
		
		del thread_dict[url_dict['args']['connid']]
		lock.release()
		print "Thread Stopped and entry deleted"
		#client.close()
		pass    
    	
	print url_dict
	print "Thread Terminated"
	client.close()



def process_request_data(data):
	cmd_type=None
	arg_dict={}
	pattern =re.compile("GET (.*) HTTP/1.1")
	m=re.search(pattern,data)
	if m!=None:
		url_data=m.group(1)
		print "URL DATA:" 
		print url_data
		if '?' in url_data:
			pattern=re.compile("^/(.*)[?](.*)")
			m2=re.search(pattern,url_data)
			if m2!=None:
				cmd_type=m2.group(1)
				arg_list=m2.group(2).split("&")
				for elem in arg_list:
					l1=elem.split('=')
					arg_dict[l1[0]]=l1[1]
		else:
			pattern=re.compile("^/(.*)")
			m2=re.search(pattern,url_data)
			if m2!=None:
					cmd_type=m2.group(1)

	return {'type':cmd_type,'args':arg_dict}

			

mySocket = socket(AF_INET, SOCK_STREAM)
mySocket.bind(("127.0.0.1", 5050))

print "Echo server listening on port 5050\n"
mySocket.listen(5)
class MyThread(Thread):
	pass
try:
	
    while True:
        (client_sock, addr) = mySocket.accept()
        #print "Got incoming connection from: " + `addr`
        print "Got Incomiing connection"
        
        #process_client(client)
        print "Starting thread with Client"
        print client_sock
        Thread(target=process_client, args=(client_sock,addr)).start()

        
except:
    print "ENTERING EXCEPTION"
    mySocket.close()
    client.close()