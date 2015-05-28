********** Problem 1 ***************
The code for problem one is reversestring.py and reversestring_test.py. Run in the following manner:

solus@veritas:~/goldenfrog$ python reversestring.py 'Hello World'                                               
dlrOw OllEh

********** Problem 2 ***************
The code for problem 2 is vpnlist.py and vpnlist_test.py. The app listens on port 5000 after 
running the following: python vpnlist.py

The api uses the following syntax.
For listing the VPNs by distance: localhost:5000/?lat=<lat>&lng=<lng>
For adding new VPNs or updating an existing one with the same name: localhost:5000/addvpn?name=<name>&lng=<lng>&lat=<lat>
For deleting VPNs localhost:5000/delvpn?name=<name>

An error is returned if you don't enter all the necessary data.
