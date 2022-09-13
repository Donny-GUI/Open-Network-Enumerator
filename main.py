import os
import socket



def get_ip():
	return socket.gethostbyname(socket.gethostname())

def get_dns_server():
	ip = get_ip()
	nets = ip.split('.')
	nets.remove(nets[-1])
	nets.append('1/24')
	dns_server = '.'.join(nets)
	return dns_server
	
def enumerate_addresses():
	mynet = get_dns_server()
	print("mapping all ips in network - this will take time")
	os.system(f'nmap {mynet}')

def dump_arp():
	os.system('arp -a > temp.txt')

def get_network_devices():
	dump_arp()
	devices = []
	with open('temp.txt', 'r', encoding='utf-8') as rfile:
		lines = rfile.readlines()
		for line in lines:
			x = str(line)
			y = x.split(' ')
			if y[3] == '(incomplete)':
				pass
			else:
				devices.append(x)
		rfile.close()
	for index, x in enumerate(devices):
		if x.startswith(' ? '):
			print(f"\033[1;32m[ {index} ]--[ ? ]---------------------------------------------------\033[0m")
			print(x[1:])
		else:
			t = x.split('(')
			print(f"\033[1;32m[ {index} ]--[ {t[0]} ]\033[0m")
			values = t[1].split(')')
			print(f" ip address : \033[44m{values[0].strip()}\033[0m")
			macs = values[1].rsplit('on')
			print(f"mac address : \033[46m{macs[0][3:].strip()}\033[0m")
			xinfo = macs[1].split(']')
			gh = xinfo[0]
			interface = gh[0:4]
			print(f"interface id: \033[45m{interface.strip()}\033[0m")
			scope = gh[4:]
			scope2 = scope.split('[')
			print(f"      scope : \033[43m{scope2[0].strip()}\033[0m")
			print(f"  interface : \033[42m{scope2[1].strip()}\033[0m")


if __name__ == '__main__':
	try:
		enumerate_addresses()
	except: 
		print("Nmap not installed")

	get_network_devices()