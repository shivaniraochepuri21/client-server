# Import socket module 
import socket  
import sys 
import os
import subprocess  
import hashlib   
import shutil         
import time  
import threading
import tqdm
from datetime import datetime
import operator

global s
# Create a socket object 

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)          
#s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# Define the port on which you want to connect 
global host
global port
port = 10050               
  
# connect to the server on local computer 
host = '127.0.0.1'
s.connect((host, port)) 
print(f"[+] Connected to {host}:{port}")

SEPARATOR = "*"
BUFFER_SIZE = 1024 # send 4096 bytes each time step
#cs.send("SEND " + FILE)
def Cache_update():
	#considering the maximum number of files in cache as a limit to
	#cache_memory which is set to 2
	for filename in os.listdir(os.path.join('cache')):
		os.unlink(os.path.join('cache') + '/' + filename)

	cache_memory = 2
	timestamps = []
	#downloaded_files list is the list of files in the downloaded folder of the client
	downloaded_files = os.listdir(os.path.join('shared'))
	
	for i in os.listdir(os.path.join('shared')):
		timestamps.append(os.path.getmtime(os.path.join('shared') + "/" + i)) 
	
	#sorting and updating based on timestamps taken in seconds
	#Recently downloaded file has the highest timestamp
	sorted_files = [x for _,x in sorted(zip(timestamps,downloaded_files))]
	#print(sorted_files)
	sorted_files = sorted_files[::-1]
	s_files = sorted_files[0:2]
	
	#files that are to be kept in the cache
	print("Cache is going to be updated with the following files")
	print(s_files)

	#two files are kept/copied in cache folder 
	dest_folder = os.path.join('cache')
	
	for i in range(len(s_files)):
		shutil.copy(os.path.join('shared') + "/" + s_files[i], dest_folder)
	return

def Cache_verify(filename,flag='TCP'):
	files_in_cache = os.listdir(os.path.join('cache'))
	dest_path = os.path.join('shared')
	if(filename in files_in_cache):
		print("The file " + filename + " is in Cache")
		shutil.copy( os.path.join('cache') + "/" + filename, dest_path)
	elif flag == "TCP":
		TCP(filename)
	else:
		UDP(filename)

	Cache_update()
	return

def Cache_show():
	for i in os.listdir(os.path.join('cache')):
		size = os.stat(os.path.join('cache') + "/" +str(i)).st_size	
		print("The file_name is: " + i, end = " ")
		print("The file size in bytes: ", size)
	return 

def get_filesize_server(filename):
	#s.send(f"{filename}".encode()) 
	#ll = os.listdir(os.path.join('shared'))
	#print(ll)
	try:
		a = os.getcwd().split("/")
		del a[len(a) - 1]
		#a.append('/')
		a.append('server')
		#a.append('/')
		a.append('shared')
		b = ("/").join(a)
		print(b)
		f = b + "/" + filename
		#fz = os.stat(f).st_size
		#fz = os.path.dirname('/server/shared').getsize(filename)
		print(f)
		fz = os.path.getsize(f)
		print("The size of the file in bytes, " + filename + ": ", fz)
		return fz
	except IOError:
		print("file not found")

def UDP(filename):

	global sock
	global udp_port
	global udp_host
	global MAX

	sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) 
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
	udp_host = '127.0.0.1'		# Host IP
	udp_port = 10000			        # specified port to connect
	sock.connect((udp_host, udp_port))
	#sock.sendto(msg.encode(),(udp_host,udp_port))
	
	filesize = get_filesize_server(filename)
	#filesize = int(filesize)
	#filen = "UDP" + filename
	sock.sendto(f"{filename}{SEPARATOR}{filesize}".encode(), (udp_host, udp_port))
	
	# start receiving the file from the socket
	# and writing to the file stream
	
	#progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True)
	with open(filename, "wb+") as f:
		#for _ in progress:
		while True:
			#read 1024 bytes from the socket (receive)
			#bytes_read, add = sock.recvfrom(BUFFER_SIZE)
			bytes_read = None
			if not bytes_read:    
				# nothing is received file transmitting is done
				break

			# write to the file the bytes we just received
			f.write(bytes_read)

			# update the progress bar
			#progress.update(len(bytes_read))
			f.close()
	
	msg = "File downloading with UDP: " + " " + str(filename)
	print(msg)
	
	sock.close()
	print("UDP Download Complete")
	os.remove(os.getcwd() + '/' + filename)
	print_md5_timestamp(filename)

def print_md5_timestamp(filename):
	x,y = FileHash_verify(os.path.join('shared') + '/' + filename)
	st = 'scp -r ../server/shared/' + str(filename) + ' ../client/shared/' + str(filename)
	subprocess.check_output(st,shell=True)
	print("Hash: ", x)
	print("Lastmodified time: ",y)

def TCP(filename):
	filesize = get_filesize_server(filename)
	msg = "File downloading with TCP: " + filename
	print(msg)
	#filen = 'TCP' + filename
	s.send(f"{filename}{SEPARATOR}{filesize}".encode())
	#print(filename)
	try:
		progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True)
		with open(os.getcwd() + '/shared/' + filename, "wb+") as f:
			#for _ in progress:
			while True:
				# read 1024 bytes from the socket (receive)
				bytes_read = s.recv(BUFFER_SIZE)
				if not bytes_read:    
			    	# nothing is received file transmitting is done
					break

				# write to the file the bytes we just received
				f.write(bytes_read)

				#update the progress bar
				progress.update(len(bytes_read))
				f.close()
			
		print("TCP Download Complete")
		print_md5_timestamp(filename)
		shutil.move(os.getcwd() + '/' + filename, os.path.join('shared') + '/' + filename)
	except TypeError:
		print("file not found")

def IndexGetlonglist():
	print('Displaying long list for all shared files')
	print(os.system('ls -lR ./shared'))
	print('**********************************')
	print("BONUS")
	print(".txt files with Programmer in it ")
	print(subprocess.check_output('find ./shared -type f -name "*.txt" | while read f;do if grep -qF "Programmer" "$f";then ls -l "$f";fi;done',shell=True))

def IndexGetshortlist(par1,par2):

	print("Displaying files created within timestamps " + str(par1) +" "+"& " + str(par2))
	cmd = 'find ./shared -type f -newerBt '+ '"'+str(par1) +'"'+' \\! -newerBt '+'"'+ str(par2)+'"' + '|while read f;do ls -l "$f";done'
	print(os.system(cmd))
	print('**********************************')
	print("BONUS")
	print("Displaying .txt and .pdf files created within timestamps " + str(par1) +" "+"& " + str(par2))
	cmd = 'find ./shared -type f \\( -iname \\*.pdf -o -iname \\*.txt \\) -newerBt '+ '"'+str(par1) +'"'+' \\! -newerBt '+'"'+ str(par2)+'"' + '|while read f;do ls -l "$f";done'
	print(subprocess.check_output(cmd,shell=True))			

def FileHash_verify(filename):
	
	md5_hash = hashlib.md5()
	# Read and update hash in chunks of 4K
	with open(os.getcwd() + '/' + filename,"rb") as f:
		for byte_block in iter(lambda: f.read(4096),b""):
			md5_hash.update(byte_block)
		checksum = md5_hash.hexdigest()
	cmd = 'date -r ' + str(filename)	
	mod_date = str(subprocess.check_output(cmd, shell=True))

	return checksum,mod_date

def FileHash_checkall():
	print("Filename, checksum and lastmodified timestamp of all the files in the shared directory")
	for root,dirs,files in os.walk('./shared/'):
		for file in sorted(files):
			fpath = os.path.join(root,file)
			print(fpath)
			checksum,mod = FileHash_verify(fpath)
			checksum_s,mod_s = FileHash_verify('../server/' + fpath[2:])
			print("Filename : " + str(file))
			print("Checksum : {}".format(checksum_s))
			print("Last modified timestamp : {}".format(mod_s))
			if checksum != checksum_s:
				print("File has changed!")
			else:	
				print("File has not changed!")


def send_command():
	
	while True:
		print('#############################################')
		print("Enter flag out of the following options:")
		print("1.IndexGet longlist. Use command: 'IndexGet Longlist'")
		print("2.IndexGet shortlist. Use command: 'IndexGet Shortlist <start_timestamp> <end_timestamp>'")
		print("Please Enter times in the format 2011-12-22 12:00:00 2020-12-25 12:00:00")
		print("\n")
		print("3.FileHash verify. Use Command: 'FileHash Verify <file_name>'")
		print("4.FileHash checkall. Use Command: 'FileHash Checkall'")
		print("5.FileDownload. Use  Command: 'FileDownload <file_name> <TCP or UDP>'")
		print("6.Cache verify. Use Command: 'Cache Verify <file_name>'")
		print("7.Cache Show. Use Command: 'Cache Show'")
		print("8.Quit. Use Command: 'Quit'")

		#Take the input command
		cmd = input()
		with open('history.txt','a') as the_file:
			the_file.write(cmd + '\n')
		if cmd == 'quit':
			print("BYE")
			s.close()
			sys.exit()
		if cmd[:8] == 'IndexGet': 
			if cmd.split(' ')[1] == 'Longlist':
				IndexGetlonglist()
			if cmd.split(' ')[1] == 'Shortlist':
				#Time should be entered in the format 2011-12-22 12:00:00 2020-12-25 12:00:00
				par1 = str(cmd.split(' ')[2] +' '+ cmd.split(' ')[3])
				par2 = str(cmd.split(' ')[4] +' '+ cmd.split(' ')[5])	
				IndexGetshortlist(par1,par2)		
			

		if cmd[:8] == 'FileHash':
			if cmd.split(' ')[1] == 'Verify':
				print("Checksum of the file on client side:")
				filename = cmd[16:]
				checksum,mod_date = FileHash_verify(filename)
				print(checksum)
				print("Last modified timestamp of the file on client side " + str(filename))
				print(mod_date)

				print("Checksum of the file on server side:")
				filename_s = '../server/' + filename[2:]
				checksum_s,mod_date_s = FileHash_verify(filename_s)
				print(checksum_s)
				print("Last modified timestamp of the file on server side " + str(filename_s))
				print(mod_date_s)

				if checksum != checksum_s:
					print("File has changed!")
				else:	
					print("File has not changed!")

			if cmd.split(' ')[1] == 'Checkall':	
				FileHash_checkall()

		if cmd[:12] == 'FileDownload':
			filename = cmd.split(' ')[1]
			if cmd.split(' ')[2] == 'TCP':
				TCP(filename)
			if cmd.split(' ')[2] == 'UDP':	
				UDP(filename)
		if cmd[:10] == 'Cache Show':
			Cache_show()
		if cmd[:12] == 'Cache Verify':	
			filename = cmd.split(' ')[2]
			Cache_verify(filename,flag="TCP")


f = open("history.txt", "w")
send_command()

# close the connection 
s.close()    