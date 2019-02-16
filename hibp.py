#hibp.py - Redesigned BreachUtils script.
"""
HIBP API script made in Python3:

 + Check any number of Email addresses for a history of breaches.
 + Check any number of passwords for a history of breaches.
"""
import urllib.request, json# Imports relevant modules
#from io import StringIO

# User Agent:
agent = "HIBP-py"

# Breach API URLs: 
e_url = "https://haveibeenpwned.com/api/v2/breachedaccount/"# See "https://haveibeenpwned.com/API/v2#UserAgent", TODO: Figure out how to get around it.
p_url = "https://api.pwnedpasswords.com/range/"
"""
^^^ This confused me for a while, it only accepts the first five characters of the hash.
    BreachUtils then needs to search for the rest of the SHA-1 hash and concat the five-char prefix to find the original password.

    E.g. "password" is:
        1. Generate SHA-1 hash, which is "5baa61e4c9b93f3f0682250b6cf8331b7ee68fd8" in this case.
        2. Send a GET request to "https://api.pwnedpasswords.com/range/5baa6"
        3. Search for "1e4c9b93f3f0682250b6cf8331b7ee68fd8" in the response.
        4. If it exists, the password was breached - the number after the colon is the number of times it was breached.
"""

# POTENTIALLY UNUSED
#psbdmp_domain_url = "https://psbdmp.ws/api/search/domain/"
#psbdmp_email_url = "https://psbdmp.ws/api/search/email/"
#psbdmp_string_url = "https://psbdmp.ws/api/search/"

def oc(opt, vs):# Opt Check
	v_main = {"1","2","3","4","98","99"}# Set of valid opts during main.
	if vs == 0:
		print("Something has gone wrong, vs=0 is only for testing.")
	if vs == 1:
		vset = v_main
	oc_ = opt in v_main # Checks if the value of opt is present in the present in the relevant set.
	if oc_ == True:
		pass
	else:
		print("[X] Invalid option")
	
def pb():# Print Banner
	print("""
 _   _ _________________                   
| | | |_   _| ___ \ ___ \                  
| |_| | | | | |_/ / |_/ /      _ __  _   _ 
|  _  | | | | ___ \  __/      | '_ \| | | | Simple script to check for password
| | | |_| |_| |_/ / |      _  | |_) | |_| | and Email address data breaches.
\_| |_/\___/\____/\_|     (_) | .__/ \__, | Written in Python 3
                              | |     __/ | kieran-walker-0@github.com
                              |_|    |___/ 

	""")
def mph():# Main Print Help
	print("""
	Choose an option:
	[1] Query with a single Email address.
	[2] Query with a list of Email addresses.
	[3] Query with a single password.
	[4] Query with a list of passwords.
	
	[98] Test connection to the HIBP servers.
	[99] Quit.
	""")
	
##########################################################################
# START of UI main portion
def i():# Interactive interface
	global opt# Allows oc() to check validity of opt.
	opt = str(input("HIBP> "))
	oc(opt, 1)
	if opt == "1":
		se()
	if opt == "2":
		print("This is the option for a list of Email addresses")
	if opt == "3":
		print("This is the option for the password")
	if opt == "4":
		print("This is the option for a list of passwords")
	if opt == "98":
		print("This is the option to test connection to the HIBP server(s)")
	if opt == "99":
		print("Quitting...")
		quit()
		
# END of UI main portion
##########################################################################
# START of single email address portion
def se():# Single Email
	pb()
	e = input("HIBP>Enter an Email address> ")
	print("Querying the HIBP database with %s..."% e)
	r = urllib.request.Request(e_url+e, data=None, headers={'User-Agent' : agent})
	o = urllib.request.urlopen(r)
	jl = json.loads(o.read().decode('utf-8'))# Loads and decodes JSON response.
	
# END of single email address portion
##########################################################################


# Point of entry
pb()
mph()
while True:# Perpetual loop of interactive UI.
	i()
