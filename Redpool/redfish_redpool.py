

import redfish
import requests
from urlparse import urljoin
import sys
from _redfishobject import RedfishObject
from redfish.rest.v1 import ServerDownOrUnreachableError
from _restobject import RestObject
import tortilla
import redfish.main
import redfish.config
import redfish.standard
import redfish.mapping
import redfish.types




def get_power_status():
	redpool=redfish.main.connect("https://10.1.213.135/redfish/v1", "admin", "admin", simulator=False, verify_cert=False)
	print("Curret Power Status is:")
	for key, value in redpool.Systems.systems_dict.iteritems():
		print(value.get_parameter('PowerState'))
	redpool.logout()

	# try:
	# 	REDFISH_OBJ = RedfishObject("https://10.1.213.135", "admin", "admin")
	# except ServerDownOrUnreachableError as excp:
	# 	sys.stderr.write("ERROR: server not reachable or doesn't support RedFish.\n")
	# 	sys.exit()
	# except Exception as excp:
	# 	raise excp

	# ex4_get_power_status(REDFISH_OBJ)
	# REDFISH_OBJ.redfish_client.logout()

	

def change_power_status(value=None):
	redpool=redfish.main.connect("https://10.1.213.135/redfish/v1", "admin", "admin", simulator=False, verify_cert=False)
	for key, value in redpool.Systems.systems_dict.iteritems():
		print("Curret Power Status is:")
		print(value.get_parameter('PowerState'))
		options=value.get_parameters()["Actions"]['#ComputerSystem.Reset']['ResetType@Redfish.AllowableValues']
		print("You have following option in which you can change the Power Status")
		print(options)
		print("Enter the Value to which you want to change Power Status to:")
		res=raw_input()
		if res not in options:
			print("You have entered a invalid input, aborting this process!!")
			return
		target=value.get_parameters()["Actions"]['#ComputerSystem.Reset']["target"]
		url=urljoin(value.url, target)
		action = dict()
		# action['Action'	] = 'Reset'
		action['ResetType'] = res
		api_url = tortilla.wrap(url, debug=True)
		
		response = api_url.post(
		verify=value.connection_parameters.verify_cert,
		headers=value.connection_parameters.headers,
		data=action)
		# response = value.api_url.post(
  #           verify=value.connection_parameters.verify_cert,
  #           headers=value.connection_parameters.headers,
  #           data=action)

		print(response)

	redpool.logout()
	# return	response
	# try:
	# 	REDFISH_OBJ = RedfishObject("https://10.1.213.135", "admin", "admin")
	# except ServerDownOrUnreachableError as excp:
	# 	sys.stderr.write("ERROR: server not reachable or doesn't support RedFish.\n")
	# 	sys.exit()
	# except Exception as excp:
	# 	raise excp

	# ex4_change_power_status(REDFISH_OBJ, status=value)
	# REDFISH_OBJ.redfish_client.logout()




def change_boot_mode():
	redpool=redfish.main.connect("https://10.1.213.135/redfish/v1", "admin", "admin", simulator=False, verify_cert=False)
	for key, value in redpool.Systems.systems_dict.iteritems():
		print("Curret Boot Mode is:")
		print(value.bios.get_parameters()["Attributes"]["BootMode"])
		options=["LegacyBios", "Uefi"]
		print("You have following option in which you can change the Power Status")
		print(options)
		print("Enter the Value to which you want to change Power Status to:")
		res=raw_input()
		if res not in options:
			print("You have entered a invalid input, aborting this process!!")
			return

		response=value.bios.set_parameter('Attributes',  {"BootMode":res})
		print(response)
	redpool.logout()
	return
	# try:
	# 	REDFISH_OBJ = RedfishObject("https://10.1.213.135", "admin", "admin")
	# except ServerDownOrUnreachableError as excp:
	# 	sys.stderr.write("ERROR: server not reachable or doesn't support RedFish.\n")
	# 	sys.exit()
	# except Exception as excp:
	# 	raise excp
	

	# ex3_change_boot_mode(REDFISH_OBJ)
	# REDFISH_OBJ.redfish_client.logout()



def change_boot_order():
	redpool=redfish.main.connect("https://10.1.213.135/redfish/v1", "admin", "admin", simulator=False, verify_cert=False)
	for key, value in redpool.Systems.systems_dict.iteritems():
		print("Curret Boot Source is:")
		print(value.get_parameter('Boot')["BootSourceOverrideTarget"])
		options=value.get_parameter('Boot')['BootSourceOverrideTarget@Redfish.AllowableValues']
		print("You have following option in which you can change the Power Status")
		print(options)
		print("Enter the Value to which you want to change Power Status to:")
		res=raw_input()
		if res not in options:
			print("You have entered a invalid input, aborting this process!!")
			return

		response=value.set_boot_source_override(res, "Continuous")
		print(response)
	
	redpool.logout()
	return
	# try:
	# 	REDFISH_OBJ = RedfishObject("https://10.1.213.135", "admin", "admin")
	# except ServerDownOrUnreachableError as excp:
	# 	sys.stderr.write("ERROR: server not reachable or doesn't support RedFish.\n")
	# 	sys.exit()
	# except Exception as excp:
	# 	raise excp

	# ex7_change_boot_order(REDFISH_OBJ)
	# REDFISH_OBJ.redfish_client.logout()




def check_virtual_media_status():
	redpool=redfish.main.connect("https://10.1.213.135/redfish/v1", "admin", "admin", simulator=False, verify_cert=False)
	for key, value in redpool.Managers.managers_dict.iteritems():
		url=value.get_link_url('VirtualMedia')
		# print url
		cp=redpool.connection_parameters
		vm_list=redfish.types.BaseCollection(url,cp)
		for item in vm_list.get_parameter("Members"):
			for idx,value in item.iteritems():
				url2= urljoin(url,value)	
				vm=redfish.types.Base(url2,cp)
				# vm2=redfish.types.Base(vm.links[1],cp)
				print("\n********************\n")
				print("Status of Virtual Media:")
				print("\n")
				for key, value in vm.get_parameters().iteritems():
					print(str(key)+" : "+ str(value))


				print("\n********************\n")
		# print("Status of second Virtual Media:")
		# print("\n")
		# for key, value in vm2.get_parameters().iteritems():
		# 	print(str(key)+" : "+ str(value))	
		# print("\n********************\n")
	redpool.logout()
	return
	# try:
	# 	REDFISH_OBJ = RedfishObject("https://10.1.213.135", "admin", "admin")
	# except ServerDownOrUnreachableError as excp:
	# 	sys.stderr.write("ERROR: server not reachable or doesn't support RedFish.\n")
	# 	sys.exit()
	# except Exception as excp:
	# 	raise excp

	# ex17_virtual_media_status(REDFISH_OBJ)
	# REDFISH_OBJ.redfish_client.logout()	



def attaching_virtual_media():
	redpool=redfish.main.connect("https://10.1.213.135/redfish/v1", "admin", "admin", simulator=False, verify_cert=False)
	for key, value in redpool.Managers.managers_dict.iteritems():
		url=value.get_link_url('VirtualMedia')
		# print url
		cp=redpool.connection_parameters
		vm_list=redfish.types.BaseCollection(url,cp)
		for item in vm_list.get_parameter("Members"):
			for idx,value in item.iteritems():
				url2= urljoin(url,value)
				vm=redfish.types.Base(url2,cp)
				if "CD" in vm.get_parameter("MediaTypes"):
					body = {"Image": "http://10.4.64.11:8080/Users/subrat/centaur-x86_64-v3.0.2.isos"}
					body["Oem"] = {"Hp": {"BootOnNextServerReset": True}}
					response=vm.set_parameter("Image", "http://10.4.64.11:8080/Users/subrat/centaur-x86_64-v3.0.2.isos")
					print(response)
					# action = dict()
			        # action[parameter_name] = value
			        # config.logger.debug(action)

			        # Perform the POST action
			        # config.logger.debug(self.api_url)
					# api_url = tortilla.wrap(url2, debug=True)
					# response = api_url.patch(
					#     verify=redpool.connection_parameters.verify_cert,
					#     headers=redpool.connection_parameters.headers,
					    # data=body)
					# response=vm.set_parameter("Oem", {"Hp": {"BootOnNextServerReset": True}})
					# print(response)

	redpool.logout()
	return
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

		
	# try:
	# 	print("\nPlease ensure that there is no inserted Virtual Media already!!\n\n")
	# 	REDFISH_OBJ = RedfishObject("https://10.1.213.135", "admin", "admin")
	# except ServerDownOrUnreachableError as excp:
	# 	sys.stderr.write("ERROR: server not reachable or doesn't support RedFish.\n")
	# 	sys.exit()
	# except Exception as excp:
	# 	raise excp
	# change_power_status(value="ForceOff")
	# ex17_mount_virtual_media_iso(REDFISH_OBJ, "http://10.0.0.100/test.iso", True)
	# REDFISH_OBJ.redfish_client.logout()





def eject_virtual_media():
	global TORTILLADEBUG
	redpool=redfish.main.connect("https://10.1.213.135/redfish/v1", "admin", "admin", simulator=False, verify_cert=False)
	for key, value in redpool.Managers.managers_dict.iteritems():
		url=value.get_link_url('VirtualMedia')
		# print url
		cp=redpool.connection_parameters
		vm_list=redfish.types.BaseCollection(url,cp)
		for item in vm_list.get_parameter("Members"):
			for idx,value in item.iteritems():
				url2= urljoin(url,value)
				vm=redfish.types.Base(url2,cp)
				if "CD" in vm.get_parameter("MediaTypes"):
					url2=vm.get_parameters()["Oem"]["Hpe"]["Actions"]["#HpeiLOVirtualMedia.EjectVirtualMedia"]["target"]
					url2= urljoin(url, url2)
					body=dict()

					api_url = tortilla.wrap(url2, debug=True)
					response = api_url.post(
					verify=vm.connection_parameters.verify_cert,
					headers=vm.connection_parameters.headers,
					data=body)
					print(response)
	redpool.logout()
	return
	# try:
	# 	REDFISH_OBJ = RedfishObject("https://10.1.213.135", "admin", "admin")
	# except ServerDownOrUnreachableError as excp:
	# 	sys.stderr.write("ERROR: server not reachable or doesn't support RedFish.\n")
	# 	sys.exit()
	# except Exception as excp:
	# 	raise excp

	# ex17_eject_virtual_media(REDFISH_OBJ)
	# REDFISH_OBJ.redfish_client.logout()


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