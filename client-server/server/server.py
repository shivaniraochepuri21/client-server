import socket     
import sys
import hashlib
import shutil
import os 
import time

SEPARATOR = "*"

# send 4096 bytes each time step
BUFFER_SIZE = 1024 
		
def TCP(c):
	#socket_accept()
	#Receive the filename + character string from the client
	received_tcp = c.recv(BUFFER_SIZE).decode()
	filename, filesize = received_tcp.split(SEPARATOR)
	#F = filen[:3]
	#filename = filename[4:]
	#print("this is flag", F)
	print("this is the filename",filename)

	#Remove absolute path if there is
	filename = os.path.basename(filename)
	filesize = os.path.getsize(os.path.join('shared') + '/' + filename)
	filesize = int(filesize)		
	#start sending the file
	#progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True)
	try:
		with open(os.path.join('shared') + '/' + filename, "rb+") as f:
			while True:
				# read the bytes from the file
				bytes_read = f.read(BUFFER_SIZE)
				if not bytes_read:
					# file transmitting is done
					break
				# we use sendall to assure transimission in busy networks
				c.sendall(bytes_read)
				# update the progress bar
				#progress.update(len(bytes_read))	
	
	except IOError:
		print("file not found")
	except TypeError:
		print("file not found")			
	
	c.close()	

def bind_udp_socket():
	try:
		print("Binding the UDP port " + str(udp_port) + " UDP")
		sock.bind((udp_host,udp_port))         
		
	except sock.error as m:
		print("Binding error: " + str(m) + "\n" + "Retrying...")
		bind_udp_socket()
	except OSError:
		sys.exit()	

def UDP():
	
	bind_udp_socket(sock)
	print("UDP socket is binded to port: ", udp_port)

	received, add = sock.recvfrom(BUFFER_SIZE).decode()
	filen, fs = received.split(SEPARATOR)
	F = filen[:3]
	filename = filename[4:]
	print(F)
	print(filename)
	filename = os.path.basename(filename)
	filesize = int(filesize)
	print(filesize)

	if(F == "UDP"):	
		#start sending the file
		progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True)
		with open(os.path.join('shared') + '/' + filename, "rb") as f:
			for _ in progress:
				# read the bytes from the file
				bytes_read = f.read(BUFFER_SIZE)
				if not bytes_read:
					# file transmitting is done
					break
				# we use sendall to assure transimission in busy networks
				sock.sendto(bytes_read, add)
				# update the progress bar
				progress.update(len(bytes_read))


def create_udpsocket():	
	global sock
	sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	global udp_host
	global udp_port
	udp_host = '127.0.0.1'
	udp_port = 10001
	print("UDP Socket is Created")
	print("UDP socket is binded to port: ", udp_port)

def create_tcpsocket():
	try:
		global host 
		global port 
		global s
		host = '127.0.0.1'
		port = 10050    
		s = socket.socket()
		#s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)          
		print("TCP Socket created")
	except socket.error as msg:
		print("TCP Socket creation error: " + str(msg))	

def bind_socket():		
	try:
		#print("Binding the port" + str(port))
		s.bind((host,port))         
		print("TCP socket is binded to port: ", port)
	except socket.error as msg:
		print("TCP Binding error: " + str(msg) + "\n" + "pls reconnect")
		#bind_socket()
		sys.exit(0)
	except OSError:
		#print("")	
		sys.exit(0)
def socket_accept():
	
	# put the socket into listening mode 
	s.listen(5)      
	print("TCP Socket is listening")            
	print(f"TCP [*] Listening as {host}:{port}")

	while (1): 
		#Establish connection with client.
		global c
		c, addr = s.accept()      
		print('Got TCP connection from', addr)
		#pass
		TCP(c)
		UDP()
def main():
	create_tcpsocket()
	bind_socket()
	socket_accept()
	create_udpsocket()
	s.close()
main()
