from credentials_to_myACI import *
from acitoolkit.acitoolkit import *

#Begin the session
session = Session(URL, LOGIN, PASSWORD)
session.login()

#Name objects
tn_name = 'Greenfish'
vrf_name = 'VRF1'
BD_name = 'BD-1'
subnet_name = 'Subnet-1'
subnet_addr = '172.30.1.1/24'
app_profile = "App-1"
epg_name =  "EPG-1"


#Create tenant and VRF
tenant = Tenant(tn_name)
vrf = Context(vrf_name, tenant)

#Create BD 
bridge_domain = BridgeDomain(BD_name, tenant)
bridge_domain.add_context(vrf)

#Create subnet for BD with public scope
subnet = Subnet(subnet_name, bridge_domain)
subnet.set_scope("public")
subnet.set_addr(subnet_addr)

#Create an application profile with an EPG
app_profile = AppProfile(app_profile, tenant)
epg = EPG(epg_name, app_profile)
epg.add_bd(bridge_domain)

#Committing the config to APIC and reporting the results
resp = session.push_to_apic(tenant.get_url(), data=tenant.get_json())

if resp.ok:
    print("\n{}: {}\n\n{} is ready for use".format(resp.status_code, resp.reason, tenant.name))
 
else:
    print("\n{}: {}\n\n{} was not created!\n\n Error: {}".format(resp.status_code, resp.reason, subnet.name, resp.content))


