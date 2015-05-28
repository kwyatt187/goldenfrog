To setup the environment run 'source bin/activate'

********** Problem 1 ***************

The code for problem one is reversestring.py and reversestring_test.py. Run in the following manner:

solus@veritas:~/goldenfrog$ python reversestring.py 'Hello World'                                               
dlrOw OllEh

********** Problem 2 ***************

The code for problem 2 is vpnlist.py and vpnlist_test.py. The app listens on port 5000 after 
running the following: python vpnlist.py

The api uses the following syntax.

For listing the VPNs by distance: localhost:5000/?lat=&lt;lat&gt;&lng=&lt;lng&gt;

Example: localhost:5000/?lat=10&lng=20

For adding new VPNs or updating an existing one with the same name: localhost:5000/addvpn?name=&lt;name&gt;&lng=&lt;lng&gt;&lat=&lt;lat&gt;

Example: localhost:5000/addvpn?name=testvpn0&lng=10&lat=20

For deleting VPNs: localhost:5000/delvpn?name=&lt;name&gt;

Example: localhost:5000/delvpn?name=testvpn0

An error is returned if you don't enter all the necessary data.
