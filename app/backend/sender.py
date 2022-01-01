"""
Client that sends the file (uploads)
"""
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'tools'))
import socket
# import tqdm

from address import _encode_username
from constant import INVALID_PORT_MSG, CONNECTION_FAILED, READY_MSG, B_BACKGROUND
from storage import format_file_name
SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 1024 * 4 #4K



def send_file(host, port,filename , state, progressBar, guiObj):
    current_socket = socket.socket()
    if port == "" or not port.isdigit():
        state.config(text=INVALID_PORT_MSG, bg="red")
        return
    try:
        state.config(text=f"[+] connexion à {_encode_username(host)}", bg="green")
        current_socket.connect((host, int(port)))
        state.config(text="[+] Connecté.")
    except Exception as e:
        print(e)
        state.config(text=CONNECTION_FAILED, bg="red")
        current_socket.close()
    # get the file size
    filesize = os.path.getsize(filename)
    # create the client socket
   

    # send the filename and filesize
    current_socket.send(f"{filename}{SEPARATOR}{filesize}".encode())

    # start sending the file
    # progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    state.config(text="[+] Trensfert de fichier encours")
    progressBar['value'] = 0
    progressBar.config(max=filesize)
    with open(filename, "rb") as f:
        progressBar.pack(fill="x", pady=2)
        while True:
            # read the bytes from the file
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                # file transmitting is done
                break
            # we use sendall to assure transimission in 
            # busy networks
            current_socket.sendall(bytes_read)
            # update the progress bar
            progressBar["value"] += BUFFER_SIZE
            current_porcentage = (int(progressBar["value"]) / int(filesize)) * 100
            state.config(text=f"[+] Trensfert de fichier {format_file_name(filename)} {int(current_porcentage)} %")
            guiObj.update_idletasks()
            # progress.update(len(bytes_read))

    # close the socket
    current_socket.close()
    state.config(text=READY_MSG, bg=B_BACKGROUND)
    progressBar.pack_forget()





if __name__ == "__main__":
    pass
    # import argparse
    # parser = argparse.ArgumentParser(description="Simple File Sender")
    # parser.add_argument("file", help="File name to send")
    # parser.add_argument("host", help="The host/IP address of the receiver")
    # parser.add_argument("-p", "--port", help="Port to use, default is 5001", default=5001)
    # args = parser.parse_args()
    # filename = "video.mp4"
    # host = "127.0.0.1"
    # port = 2008
    # send_file(filename, host, port)
