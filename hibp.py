#hibp.py - Redesigned BreachUtils script.
"""
HIBP API script made in Python3:

 + Check any number of Email addresses for a history of breaches.
 + Check any number of passwords for a history of breaches.
"""
import urllib.request, json, datetime, hashlib, re# Imports relevant modules

# User Agent:
agent = "HIBP-py"

# Breach API URLs: 
e_url = "https://haveibeenpwned.com/api/v2/breachedaccount/"
p_url = "https://api.pwnedpasswords.com/range/"
"""
^^^ This confused me for a while, it only accepts the first five characters of the hash.
    HIBP.py then needs to search for the rest of the SHA-1 hash and concat the five-char prefix to find the original password.

    E.g. "password" is:
        1. Generate SHA-1 hash, which is "5baa61e4c9b93f3f0682250b6cf8331b7ee68fd8" in this case.
        2. Send a GET request to "https://api.pwnedpasswords.com/range/5baa6"
        3. Search for "1e4c9b93f3f0682250b6cf8331b7ee68fd8" in the response.
        4. If it exists, the password was breached - the number after the colon is the number of times it was breached.
"""
def oc(opt, vs):# Opt Check
	v_main = {"1","2","99"}# Set of valid opts during main.
	v_pass = {"1", "2"}# Set of valid opts during password opts.
	if vs == 0:
		print("Something has gone wrong, vs=0 is only for testing.")
	if vs == 1:
		vset = v_main
	if vs == 2:
		vset = v_pass
	oc_ = opt in vset # Checks if the value of opt is present in the present in the relevant set.
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
	[2] Query with a single password.
	
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
		sp()
	if opt == "99":
		print("Quitting...")
		quit()
		
# END of UI main portion
##########################################################################
# START of single email address portion
def se():# Single Email
	e = input("HIBP>Enter an Email address> ")
	print("Querying the HIBP database with %s..."% e)
	r = urllib.request.Request(e_url+e, data=None, headers={'User-Agent' : agent})
	try:
		o = urllib.request.urlopen(r)# urllib throws an exception if a 404 is returned here.
		print("[!] You've been breached!")
		jl = json.loads(o.read().decode('utf-8'))# Decodes JSON response.
		jl_num = 0
		title = []
		date = []
		data = []
		while True:
			try:
				jl_index = jl[jl_num]
				title.append(jl_index["Title"])
				date.append(jl_index["BreachDate"])
				data.append(jl_index["DataClasses"])
				jl_num += 1
			except:
				break
##########################################################
# FILE INPUT START
		d_index = 0
		f_input = ""
		current_dc = data
		for t in title:
			f_input += "[+] "+t+" \n"+"Date breached: "+str(date[d_index])+"\n Data compromised in breach:\n"
			f_data = ""
			for d in data[d_index]:# Cheers for the help, Ian!
				f_data += ("	- %s \n"% d)
			d_index += 1
			f_input += f_data+"\n"
		f_in = """
HIBP.py
 Breach data retrieved from 'HaveIBeenPwned?' at """+str(datetime.datetime.now())+""":
 
Breached sites: 
"""+f_input+"""

		"""
		print(f_in)
		e_splitter = e.split("@")
		email_name = e_splitter[0]# Includes all chars before the "@" symbol in 'e'.
		time_splitter = str(datetime.datetime.now()).split()# Gets rid of unnecessary accuracy of the now() method.
		fname = email_name+"-hibp_report-"+time_splitter[0]+".txt"
		print("Output saved in current directory as "+fname+".")
		f = open(fname, "w")
		f.write(f_in)
# FILE INPUT END
##########################################################################
	except:# If/when 404 response code is thrown.
		print("[+] No breach data found, lucky you!")
# END of single email address portion
##########################################################################
# START of single password portion
def sp():# Single password
	print("""
In order to protect the privacy of user-submitted passwords, the PwnedPasswords
API will allow for search ranges only, this is done by hashing user input using the
SHA-1 algorithm and showing all hashes that match the first 5 characters (prefix).
This script will hash any cleartext input and automatically match the prefix with the
rest of the password's hash.

Of course, in the interest of security, this part of the script should be performed
under a secured environment. Be aware of physical, software-based and network-based 
monitoring technologies that may be in place.

This script will not decrypt or store any hashes or cleartext passwords submitted.

Choose an option:
	[1] Cleartext password
	[2] SHA-1 Hash
	
	""")
	opt = str(input("HIBP>Cleartext or SHA-1 Hash?> "))
	oc(opt, 2)
	if opt == "1":
		p = input("HIBP>Cleartext password> ")# TODO: Make the user input invisible
		p = str(p).encode('utf-8')
		h = hashlib.sha1(p).hexdigest()
		prefix = h[0:5].upper()
		suffix = h[5:]
		r = urllib.request.Request(p_url+prefix, data=None, headers={'User-Agent' : agent})
		try:
			o = urllib.request.urlopen(r).read()# Shouldn't be any 404 here, as custom agent is not required.
			re_compile = re.compile("("+suffix+")\:([0-9])*", flags=re.IGNORECASE)
			result = re.search(re_compile, str(o))
			response = result[0]
			splitter = response.split(":")
			#split_h = splitter[0]
			split_n = splitter[1]
			print("[!] That password has been previously compromised %s times!"% split_n)
		except:
			print("[+] No password hash found, lucky you!")
	if opt == "2":
		h = input("HIBP> SHA-1 hash> ")
		prefix = h[0:5].upper()
		suffix = h[5:]
		r = urllib.request.Request(p_url+prefix, data=None, headers={'User-Agent' : agent})
		try:
			o = urllib.request.urlopen(r).read()
			re_compile = re.compile("("+suffix+")\:([0-9])*", flags=re.IGNORECASE)
			result = re.search(re_compile, str(o))
			response = result[0]
			splitter = response.split(":")
			split_n = splitter[1]
			print("[!] That password has been previously compromised %s times!"% split_n)
		except:
			print("[+] No password hash found, lucky you!")
		


# END of single password portion
##########################################################################


# Point of entry
pb()
mph()
while True:# Perpetual loop of interactive UI.
	i()
