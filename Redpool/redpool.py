

import redfish
import requests
from urlparse import urljoin
import sys
from _redfishobject import RedfishObject
from redfish.rest.v1 import ServerDownOrUnreachableError
from _restobject import RestObject

# redpool=redfish.connect("https://10.1.213.164/redfish/v1", "admin", "admin", simulator=False, verify_cert=False)
def ex4_get_power_status(redfishobj, bios_password=None):
	sys.stdout.write("\n Get Power Status\n")
	instances = redfishobj.search_for_type("ComputerSystem.")

	if redfishobj.typepath.defs.isgen9:
		for instance in instances:	
			print("Curret Power Status is:")
			print(resp.dict["PowerState"])
			
	else:
		for instance in instances:
			resp = redfishobj.redfish_get(instance['@odata.id'])
			if resp.status==200:
				print("Curret Power Status is:")
				print(resp.dict["PowerState"])
				

			else:
				sys.stderr.write("ERROR: Unable to find the path for reboot.")
				raise


def get_power_status():
	try:
		REDFISH_OBJ = RedfishObject("https://10.1.213.135", "admin", "admin")
	except ServerDownOrUnreachableError as excp:
		sys.stderr.write("ERROR: server not reachable or doesn't support RedFish.\n")
		sys.exit()
	except Exception as excp:
		raise excp

	ex4_get_power_status(REDFISH_OBJ)
	REDFISH_OBJ.redfish_client.logout()

def ex4_change_power_status(redfishobj, bios_password=None, status=None):
	sys.stdout.write("\n Change Power Status\n")
	instances = redfishobj.search_for_type("ComputerSystem.")

	if redfishobj.typepath.defs.isgen9:
		for instance in instances:
			# resp = redfishobj.redfish_get(instance['@odata.id'])	
			# print("Curret Power Status is:")
			# print(resp.dict["PowerState"])
			# options=resp.dict["Actions"]["#ComputerSystem.Reset"]["ResetType@Redfish.AllowableValues"]
			# print ("You have following options to choose from, for changing the Power Status ")
			# print(options)
			print("Enter one of the ResetType Option")
			res=raw_input()
			body = dict()
			body["Action"] = "Reset"
			body["ResetType"] = res

			response = redfishobj.redfish_post(instance["@odata.id"], body)
			redfishobj.error_handler(response)
	else:
		for instance in instances:
			resp = redfishobj.redfish_get(instance['@odata.id'])
			if resp.status==200:
				options=resp.dict["Actions"]["#ComputerSystem.Reset"]["ResetType@Redfish.AllowableValues"]
				if status==None:
					print("Curret Power Status is:")
					print(resp.dict["PowerState"])
					
					print ("You have following options to choose from, for changing the Power Status ")
					print(options)
					print("Enter one of the above options")
					res=raw_input()
				else:
					res=status
				if res not in options:
					print("You have entered a invalid input, aborting this process!!")
					return
				body = dict()
				body["Action"] = "ComputerSystem.Reset"
				body["ResetType"] = res
				path = resp.dict["Actions"]["#ComputerSystem.Reset"]["target"]

			else:
				sys.stderr.write("ERROR: Unable to find the path for reboot.")
				raise

			response = redfishobj.redfish_post(path, body)
			redfishobj.error_handler(response)	

def change_power_status(value=None):
	# redpool=redfish.connect("https://10.1.213.135/redfish/v1", "admin", "admin", simulator=False, verify_cert=True)
	# print("Curret Power Status is:")
	# print(redpool.Systems.systems_dict['1'].get_parameter('PowerState'))
	# options=redpool.Systems.systems_dict['1'].get_parameters()["Actions"]['#ComputerSystem.Reset']['ResetType@Redfish.AllowableValues']
	# print("You have following option in which you can change the Power Status")
	# print(options)
	# print("Enter the Value to which you want to change Power Status to:")
	# res=raw_input()
	# if res not in options:
	# 	print("You have entered a invalid input, aborting this process!!")
	# 	return

	# action = dict()
 #        # action['Action'] = 'Reset'
 #        action['ResetType'] = res

	# response = requests.post(str(urljoin(redpool.Systems.systems_dict['1'].url, redpool.Systems.systems_dict['1'].data["Actions"]["#ComputerSystem.Reset"]["target"])),
 #            verify=redpool.connection_parameters.verify_cert,
 #            headers=redpool.connection_parameters.headers,
 #            data=action)

	# print (response)
	# redpool.logout()
	# return	response
	try:
		REDFISH_OBJ = RedfishObject("https://10.1.213.135", "admin", "admin")
	except ServerDownOrUnreachableError as excp:
		sys.stderr.write("ERROR: server not reachable or doesn't support RedFish.\n")
		sys.exit()
	except Exception as excp:
		raise excp

	ex4_change_power_status(REDFISH_OBJ, status=value)
	REDFISH_OBJ.redfish_client.logout()


def ex3_change_boot_mode(redfishobj, bios_password=None):
    # sys.stdout.write("\nEXAMPLE 3: Change a BIOS setting\n")
    instances = redfishobj.search_for_type("Bios.")
    # print(instances)
    if not len(instances) and redfishobj.typepath.defs.isgen9:
        sys.stderr.write("\nNOTE: This example requires the Redfish schema "\
                 "version TBD in the managed iLO. It will fail against iLOs"\
                 " with the 2.50 firmware or earlier. \n")

    for instance in instances:
    	if str(instance['@odata.id']).find("settings")==-1:
    		continue
    	resp = redfishobj.redfish_get(instance['@odata.id'])
    	if resp.dict["Attributes"]["BootMode"]:
			print("Curret Boot Mode is:")
			print (resp.dict["Attributes"]["BootMode"])
			options=["LegacyBios", "Uefi"]
			print("You have following option in which you can change the Power Status")
			print(options)
			print("Enter the Value to which you want to change Power Status to:")
			
			property_value=raw_input()
				
			if property_value not in options:
					print("You have entered a invalid input, aborting this process!!")
					return
			if redfishobj.typepath.defs.isgen9:
				body = {"BootMode": property_value}
			else:
				body = {"Attributes": {"BootMode": property_value}}

			response = redfishobj.redfish_patch(instance["@odata.id"], body, optionalpassword=bios_password)
			redfishobj.error_handler(response)

def change_boot_mode():
	# redpool=redfish.connect("https://10.1.213.135/redfish/v1", "admin", "admin", simulator=False, verify_cert=False)
	# print("Curret Boot Mode is:")
	# print(redpool.Systems.systems_dict['1'].bios.get_parameters()["Attributes"]["BootMode"])
	# options=["LegacyBios", "Uefi"]
	# print("You have following option in which you can change the Power Status")
	# print(options)
	# print("Enter the Value to which you want to change Power Status to:")
	# res=raw_input()
	# if res not in options:
	# 	print("You have entered a invalid input, aborting this process!!")
	# 	return

	# response=redpool.Systems.systems_dict['1'].bios.set_parameter('Attributes',  {"BootMode":res})
	
	# redpool.logout()
	# return
	try:
		REDFISH_OBJ = RedfishObject("https://10.1.213.135", "admin", "admin")
	except ServerDownOrUnreachableError as excp:
		sys.stderr.write("ERROR: server not reachable or doesn't support RedFish.\n")
		sys.exit()
	except Exception as excp:
		raise excp
	

	ex3_change_boot_mode(REDFISH_OBJ)
	REDFISH_OBJ.redfish_client.logout()

def ex7_change_boot_order(redfishobj, bios_password=None):
	sys.stdout.write("\nEXAMPLE 7: Change Boot Order (UEFI)\n")
	instances = redfishobj.search_for_type("ServerBootSettings.")
	if not len(instances) and redfishobj.typepath.defs.isgen9:
		sys.stderr.write("\nNOTE: This example requires the Redfish schema version TBD in the managed iLO. It will fail against iLOs with the 2.50 firmware or earlier. \n")

	for instance in instances:
		if str(instance['@odata.id']).find("settings")==-1:
			continue
		response = redfishobj.redfish_get(instance["@odata.id"])
		bootorder = response.dict["PersistentBootConfigOrder"]
		print("\nCurrent persistent boot order is this:")
		print(bootorder,"\n")
		#TODO: Need to change the persistent boot order here
		# print("Please enter the new Persistent Boot Order List")
		# res=[]
		# n=len(bootorder)
		# for i in xrange(n):
		# 	if i==0:
		# 		print("Please enter the first device:")
		# 	else:
		# 		print("Please enter the next device:")	

		# 	res2=raw_input()
		# 	if res2 not in bootorder:
		# 		print("Invalid input!!")
		# 		return
		# 	res.append(res2)	
		res=bootorder[0]
		bootorder[0]=bootorder[1]
		bootorder[1]=res

		body = dict()
		body["PersistentBootConfigOrder"] = bootorder

		response = redfishobj.redfish_patch(instance["@odata.id"], body, optionalpassword=bios_password)            
		redfishobj.error_handler(response)

def change_boot_order():
	# redpool=redfish.connect("https://10.1.213.135/redfish/v1", "admin", "admin", simulator=False, verify_cert=False)
	# print("Curret Boot Source is:")
	# print(redpool.Systems.systems_dict['1'].get_parameter('Boot')["BootSourceOverrideTarget"])
	# options=redpool.Systems.systems_dict['1'].get_parameter('Boot')['BootSourceOverrideTarget@Redfish.AllowableValues']
	# print("You have following option in which you can change the Power Status")
	# print(options)
	# print("Enter the Value to which you want to change Power Status to:")
	# res=raw_input()
	# if res not in options:
	# 	print("You have entered a invalid input, aborting this process!!")
	# 	return

	# response=redpool.Systems.systems_dict['1'].set_boot_source_override(res, "Continuous")
	
	# redpool.logout()
	# return
	try:
		REDFISH_OBJ = RedfishObject("https://10.1.213.135", "admin", "admin")
	except ServerDownOrUnreachableError as excp:
		sys.stderr.write("ERROR: server not reachable or doesn't support RedFish.\n")
		sys.exit()
	except Exception as excp:
		raise excp

	ex7_change_boot_order(REDFISH_OBJ)
	REDFISH_OBJ.redfish_client.logout()


def ex17_virtual_media_status(redfishobj):
	# sys.stdout.write("\nEXAMPLE 17: Mount iLO Virtual Media DVD ISO from URL\n")
	instances = redfishobj.search_for_type("Manager.")

	for instance in instances:
		# print("****",instance["@odata.id"],"*****")
		rsp = redfishobj.redfish_get(instance["@odata.id"])
		# print("!!!!",rsp.dict["VirtualMedia"]["@odata.id"],"!!!!!")
		rsp = redfishobj.redfish_get(rsp.dict["VirtualMedia"]["@odata.id"])
		# print("@@@@",rsp.dict["Members"],"@@@@@")
		for vmlink in rsp.dict["Members"]:
			response = redfishobj.redfish_get(vmlink["@odata.id"])
			# print(response.dict)
			print("\n********************\n")
			print("Status of Virtual Media:")
			print("\n")
			for key, value in response.dict.iteritems():
				print(str(key)+" : "+ str(value))
			# print("@@@@",response.dict["MediaTypes"],"@@@@@")
			# if response.status == 200 and "DVD" in response.dict["MediaTypes"]:
			# 	body = {"Image": iso_url}

			# 	# TODO need to check for redfish support
			# 	if (iso_url is not None and boot_on_next_server_reset is not None):
			# 		if redfishobj.typepath.defs.isgen9:
			# 			body["Oem"] = {"Hp": {"BootOnNextServerReset": \
   #                                                  boot_on_next_server_reset}}
			# 		else:
			# 			body["Oem"] = {"Hpe": {"BootOnNextServerReset":boot_on_next_server_reset}}

			# 		response = redfishobj.redfish_patch(vmlink["@odata.id"], body)
			# 		redfishobj.error_handler(response)
			# elif response.status != 200:
			# 	redfishobj.error_handler(response)

def check_virtual_media_status():
	# redpool=redfish.main.connect("https://10.1.213.135/redfish/v1", "admin", "admin", simulator=False, verify_cert=False)
	# url=redpool.Managers.managers_dict['1'].get_link_url('VirtualMedia')
	# # print url
	# cp=redpool.connection_parameters
	# vm=redfish.types.BaseCollection(url,cp)
	# vm1=redfish.types.Base(vm.links[0],cp)
	# vm2=redfish.types.Base(vm.links[1],cp)
	# print("\n********************\n")
	# print("Status of first Virtual Media:")
	# print("\n")
	# for key, value in vm1.get_parameters().iteritems():
	# 	print(str(key)+" : "+ str(value))


	# print("\n********************\n")
	# print("Status of second Virtual Media:")
	# print("\n")
	# for key, value in vm2.get_parameters().iteritems():
	# 	print(str(key)+" : "+ str(value))	
	# print("\n********************\n")
	# redpool.logout()
	# return
	try:
		REDFISH_OBJ = RedfishObject("https://10.1.213.135", "admin", "admin")
	except ServerDownOrUnreachableError as excp:
		sys.stderr.write("ERROR: server not reachable or doesn't support RedFish.\n")
		sys.exit()
	except Exception as excp:
		raise excp

	ex17_virtual_media_status(REDFISH_OBJ)
	REDFISH_OBJ.redfish_client.logout()	

def ex17_mount_virtual_media_iso(redfishobj, iso_url, boot_on_next_server_reset):
	# sys.stdout.write("\nEXAMPLE 17: Mount iLO Virtual Media DVD ISO from URL\n")
	instances = redfishobj.search_for_type("Manager.")

	for instance in instances:
		# print("****",instance["@odata.id"],"*****")
		rsp = redfishobj.redfish_get(instance["@odata.id"])
		# print("!!!!",rsp.dict["VirtualMedia"]["@odata.id"],"!!!!!")
		rsp = redfishobj.redfish_get(rsp.dict["VirtualMedia"]["@odata.id"])
		# print("@@@@",rsp.dict["Members"],"@@@@@")
		for vmlink in rsp.dict["Members"]:
			response = redfishobj.redfish_get(vmlink["@odata.id"])
			# print("@@@@",response.dict["MediaTypes"],"@@@@@")
			if response.status == 200 and "DVD" in response.dict["MediaTypes"]:
				body = {"Image": iso_url}

				# TODO need to check for redfish support
				if (iso_url is not None and boot_on_next_server_reset is not None):
					if redfishobj.typepath.defs.isgen9:
						body["Oem"] = {"Hp": {"BootOnNextServerReset": \
                                                    boot_on_next_server_reset}}
					else:
						body["Oem"] = {"Hpe": {"BootOnNextServerReset":boot_on_next_server_reset}}

					response = redfishobj.redfish_patch(vmlink["@odata.id"], body)
					redfishobj.error_handler(response)
			elif response.status != 200:
				redfishobj.error_handler(response)

def attaching_virtual_media():
	# redpool=redfish.main.connect("https://10.1.213.135/redfish/v1", "admin", "admin", simulator=False, verify_cert=False)
	# url=redpool.Managers.managers_dict['1'].get_link_url('VirtualMedia')
	# # print url
	# cp=redpool.connection_parameters
	# vm=redfish.types.BaseCollection(url,cp)
	# vm1=redfish.types.Base(vm.links[0],cp)
	# vm2=redfish.types.Base(vm.links[1],cp)
	# print("\n********************\n")
	# print("Status of first Virtual Media:")
	# print("\n")
	# for key, value in vm1.get_parameters().iteritems():
	# 	print(str(key)+" : "+ str(value))


	# print("\n********************\n")
	# print("Status of second Virtual Media:")
	# print("\n")
	# for key, value in vm2.get_parameters().iteritems():
	# 	print(str(key)+" : "+ str(value))	
	# print("\n********************\n\n")
	# print ("Enter the path of the iso:")
	# iso=raw_input()
	# print("Enter:\n 0 : Adding iso to Virtual Media 1\n 1: Adding iso to Virtual Media 2")
	# option=input()
	# if option==0:
	# 	vm1.set_parameter("Image",iso)
	# elif option==1:
	# 	vm2.set_parameter("Image", iso)
	# else:
	# 	print("Invalid Input!!")

	# return	
	try:
		print("\nPlease ensure that there is no inserted Virtual Media already!!\n\n")
		REDFISH_OBJ = RedfishObject("https://10.1.213.135", "admin", "admin")
	except ServerDownOrUnreachableError as excp:
		sys.stderr.write("ERROR: server not reachable or doesn't support RedFish.\n")
		sys.exit()
	except Exception as excp:
		raise excp
	# change_power_status(value="ForceOff")
	ex17_mount_virtual_media_iso(REDFISH_OBJ, "http://10.4.64.11:8080/Users/subrat/centaur-x86_64-v3.0.2.isos", True)
	REDFISH_OBJ.redfish_client.logout()


def ex17_eject_virtual_media(redfishobj):
	# sys.stdout.write("\nEXAMPLE 17: Mount iLO Virtual Media DVD ISO from URL\n")
	instances = redfishobj.search_for_type("Manager.")

	for instance in instances:
		# print("****",instance["@odata.id"],"*****")
		rsp = redfishobj.redfish_get(instance["@odata.id"])
		# print("!!!!",rsp.dict["VirtualMedia"]["@odata.id"],"!!!!!")
		rsp = redfishobj.redfish_get(rsp.dict["VirtualMedia"]["@odata.id"])
		# print("@@@@",rsp.dict["Members"],"@@@@@")
		for vmlink in rsp.dict["Members"]:
			response = redfishobj.redfish_get(vmlink["@odata.id"])
			# print("@@@@",response.dict["MediaTypes"],"@@@@@")
			if response.status == 200 and "DVD" in response.dict["MediaTypes"]:
				# body = {"Image": iso_url}
				body=dict()
				# TODO need to check for redfish support
				
				# if redfishobj.typepath.defs.isgen9:
				# 	body["Oem"] = {"Hp": {"Actions":"#HpeiLOVirtualMedia.EjectVirtualMedia"}}
				# else:
				# 	body["Oem"] = {"Hpe": {"Actions":"EjectVirtualMedia", "EjectVirtualMedia": True  }}
				url=response.dict["Oem"]["Hpe"]["Actions"]["#HpeiLOVirtualMedia.EjectVirtualMedia"]["target"]
				# print("******",vmlink["@odata.id"])
				response = redfishobj.redfish_post(url, body)
				redfishobj.error_handler(response)
			elif response.status != 200:
				redfishobj.error_handler(response)


def eject_virtual_media():
	try:
		REDFISH_OBJ = RedfishObject("https://10.1.213.135", "admin", "admin")
	except ServerDownOrUnreachableError as excp:
		sys.stderr.write("ERROR: server not reachable or doesn't support RedFish.\n")
		sys.exit()
	except Exception as excp:
		raise excp

	ex17_eject_virtual_media(REDFISH_OBJ)
	REDFISH_OBJ.redfish_client.logout()


print ("\n\n*********Welcome to Redpool*********\n")
while(True):
	print("\n")
	print("Enter 1 for Getting Power Status")
	print("Enter 2 for Changing the Power Status")
	print("Enter 3 for Changing the Boot Mode")
	print("Enter 4 for Changing the Boot Order")
	print("Enter 5 for Checking the Virtual Media Status")
	print("Enter 6 for Attaching Virtual Media")
	print("Enter 7 for Ejecting Vitual Media")
	print("Enter 0 to End the Program")
	print("\n")
	print("Enter one of the above options according to your need: ")

	res=input()
	if res==1:
		get_power_status()
	elif res==2:
		change_power_status()
	elif res==3:
		change_boot_mode()
	elif res==4:
		change_boot_order()
	elif res==5:
		check_virtual_media_status()
	elif res==6:
		attaching_virtual_media()
	elif res==7:
		eject_virtual_media()
	elif res==0:
		print("********Exiting********")
		quit()
	else:
		print("Its an invalid response. Please try again!!")


# redpool.logout()		

# def connect(url, userid, password, simulator=False, verify_cert=False):
# 	redpool =redfish.main.connect(url, userid, password, simulator=False, verify_cert=False)

# 	return redpool







# a=connect("https://10.1.213.164/redfish/v1", "admin", "admin", simulator=False, verify_cert=False)

# print(get_power_status(a))