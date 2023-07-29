*********************************************************************************************************************************
											COMMUNICATION NETWORKS PROJECT 2
																			Shivani Chepuri 2018122004
																			Gowri Lekshmy 20171053


*********************************************************************************************************************************
FUNCTIONALITIES

An implementation of File Sharing with the following functionalities

1.IndexGet longlist 	- Displays longlist/all the shared files

2.IndexGet shortlist 	- Displays list of files between 2 timestamps of shared files

3.FileHash verify 		- Verifies if a given file has been changed on the other side based on md5 checksum hash.

4.FileHash checkall 	- Verifies if all files have been changed on the other side based on md5 checksum hash.

5.FileDownload TCP/UDP 	- Downloads a given file from the shared folder of the server to the shared
			  			  folder of the client using either TCP or UDP protocol(specified in the command line)

6.Caching verify 		- This is a client side check/folder. Verfies if a given file is present in the cache folder.
			  			  If the file is present in the cache folder, the required file is fetched from the cache 
			  			  folder to the shared folder. If not, downloads the file from the server.
			  			  Then, Updates the cache based on the recently downloaded files (timestamp).
			  			  This Cache folder is limited to having 2 files (Cache Memory).

7.Caching show 			- Prints all elements in cache with their sizes 

8.Quit 					- Quits the program


*********************************************************************************************************************************
DIRECTORY STRUCTURE

CN_Project2
├── client
│   ├── cache
│   │   ├── a.txt
│   │   ├── b.txt
│   │   └── c.txt
│   ├── client.py
│   ├── history.txt : contains history of requests
│   └── shared : contains shared files
│       ├── 2.txt
│       ├── folder1
│       │   ├── 3.txt
│       │   └── 4.txt
│       ├── new.txt
│       ├── paper.pdf
│       └── solutionmanual.pdf
└── server
    ├── server.py
    └── shared : contains shared files
        ├── 2.txt
        ├── a.txt
        ├── folder1
        │   ├── 3.txt
        │   └── 4.txt
        ├── paper.pdf
        └── solutionmanual.pdf


*********************************************************************************************************************************        
REQUIREMENTS

sockets
hashlib
shutil
subprocess
sys
os
tqdm  

pip install tqdm 

*********************************************************************************************************************************
RUNNING THE CODE

Run the Server side first, so that it can accept connections/requests from the client.
Then Run the Client side.

On Server Side:
cd CN_Project2/server/
	- python3 server.py

On Client Side:	
cd CN_Project2/client/
	- python3 client.py

	- On Displaying list of functionalities
	- Use the following command structure for the corresponding functionalities:

		Function                  Command  
		
		1.IndexGet Longlist 	- IndexGet Longlist

		2.IndexGet Shortlist 	- IndexGet Shortlist <begintimestamp> <endtimestamp> 
					  			  (Eg.2011-12-22 12:00:00 2020-12-25 12:00:00) 

		3.FileHash Verify 		- FileHash Verify <filename>

		4.FileHash Checkall 	- FileHash Checkall

		5.FileDownload TCP/UDP 	- FileDownload <filename> <TCP/UDP>

		6.Cache Verify 			- Cache Verify <filename>

		7.Cache Show 			- Cache Show

		8.Quit 					- Quit		

Note - Do not give the entire path to the file as filename, give only its name, including the extension

*********************************************************************************************************************************
BONUS IMPLEMENTATION:

IndexGet Longlist   - Returns longlist only for *.txt files which have "Programmer" word in it  
IndexGet Shortlist  - Returns shortlist only for *.txt and *.pdf files created between the two timestamps specified by user 

*********************************************************************************************************************************
