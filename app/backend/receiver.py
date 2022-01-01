"""
Server receiver of the file
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'tools'))
import socket
# import tqdm

from constant import WAITING_FOR_FILE_MSG, READY_MSG
from storage import format_file_name, destination_path


class Receiver:
    def __init__(self, host, port, state, progressBar, guiObject):
        self.HOST = host
        self.PORT = port
        self.state = state
        self.BUFFER_SIZE = 4096
        self.SEPARATOR = "<SEPARATOR>"
        self.server = socket.socket()
        self.client_socket = None
        self.serverIsRunning = False
        self.rec_progressbar= progressBar
        self.rec_gui = guiObject

    def init_server(self):
        
        self.server.bind((self.HOST, self.PORT))
        self.serverIsRunning = True
        self.state.config(text=WAITING_FOR_FILE_MSG)
        self.server.listen(5)
        

    def accept_connection(self):
        if not self.serverIsRunning : return
        self.client_socket, self.address = self.server.accept()

    def receive_file(self):
        if not self.serverIsRunning : return
        receiption = self.client_socket.recv(self.BUFFER_SIZE).decode()

        filename, filesize = receiption.split(self.SEPARATOR)
        filename = os.path.basename(filename)
        self.state.config(text=f"reception de fichier '{format_file_name(filename, 15)}' encours ... ")
        self.rec_progressbar.config(max=filesize)
        self.rec_progressbar["value"] = 0
        with open(f"{destination_path()}/"+filename, "wb") as f:
            self.rec_progressbar.pack(expand=1, fill="x", pady=2)
            while True:
                # read 1024 bytes from the socket (receive)

                bytes_read = self.client_socket.recv(self.BUFFER_SIZE)
                if not bytes_read:    
                    # nothing is received
                    # file transmitting is done
                    break
                # write to the file the bytes we just received
                f.write(bytes_read)
                #updating the progressbar

               
                self.rec_progressbar["value"] += self.BUFFER_SIZE
                current_parent = (int(self.rec_progressbar["value"]) / int(filesize)) * 100
                self.state.config(text=f"reception de fichier '{format_file_name(filename, 15)}' {round(current_parent, 0)} %")
                self.rec_gui.update_idletasks()
                
        self.client_socket.close()
        self.server.close()
        self.state.config(text=READY_MSG)
        self.rec_progressbar.pack_forget()
        return receiption.split(self.SEPARATOR)

    def setup(self):
        self.init_server()
        try:
            self.accept_connection()

            return self.receive_file()
            if self.client_socket != None : self.client_socket.close()
            self.server.close()
        except OSError:
            import sys
            sys.exit()

    def forced(self):
        raise ValueError
    def close(self):
        if self.client_socket != None : self.client_socket.close()
        self.server.close()
        try:
            self.forced()
        except:
            pass

#https://www.figma.com/file/htjzqd57xzyFB7WgOWEKOe/Untitled?node-id=0%3A1
#297102-f7aabf30-795f-4f84-9d55-f30fe956bd6b

if __name__ == "__main__":
    pass