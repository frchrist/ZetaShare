import socket

def get_host():
	return socket.gethostbyname(socket.gethostname())
def base():
	# { str(i):chr(ord("H")+i) for i in range(0, 11) } | {".":"X"} // expression for python3.9
	out = { str(i):chr(ord("H")+i) for i in range(0, 11) }
	out["."] = "X"
	return  out
def encode_username():
	r = get_host().split(".")[-2:]
	return "".join(list(map(lambda x : base()[x], ".".join(r))))

def _encode_username(host):
	r = host.split(".")[-2:]
	return "".join(list(map(lambda x : base()[x], ".".join(r))))

def decode_username(string):
	reversed_base = {y:x for x,y in base().items()}
	return ".".join(get_host().split(".")[:-2])+"."+"".join(list(map(lambda x : reversed_base[x], string)))

