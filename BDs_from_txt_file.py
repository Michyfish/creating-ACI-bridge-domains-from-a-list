from credentials_to_myACI import *
from acitoolkit.acitoolkit import *

#Begin the session
session = Session(URL, LOGIN, PASSWORD)
session.login()

#This script creates BDs from a list

#Variables
tn_name = 'Greenfish'
vrf_name = 'VRF1'

#Creating tenant and VRF
tenant = Tenant(tn_name)
vrf = Context(vrf_name, tenant)

#First, creating a dictionary from the list
dictionary = {}
y = raw_input("What file is your list of bridge domains?")	

with open(y) as f:
	for line in f:
		key, value = line.strip("\n").split(":",1)
		dictionary[key] = value

#Create each BD and subnet
for key in dictionary:
   
    bd_name = key
    bridge_domain = BridgeDomain(bd_name, tenant)
    bridge_domain.add_context(vrf)
    subnet_name = "Subnet for " + key
    subnet = Subnet(subnet_name, bridge_domain)
    subnet.set_scope("public")
    subnet.set_addr(dictionary[key]) 

#Committing the config to APIC and reporting the results
resp = session.push_to_apic(tenant.get_url(), data=tenant.get_json())

if resp.ok:
    print("\n{}: {}\n\n{} is ready for use".format(resp.status_code, resp.reason, tenant.name))
 
else:
    print("\n{}: {}\n\n{} was not created!\n\n Error: {}".format(resp.status_code, resp.reason, subnet.name, resp.content))  
