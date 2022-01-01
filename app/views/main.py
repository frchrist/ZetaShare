import tkinter as tk
import sys
import os
from tkinter.ttk import Button, LabelFrame, Entry, Treeview, Style, Progressbar, Checkbutton
from tkinter import filedialog
from tkinter import messagebox
import time
from datetime import date
from about import About
from history_detail import HDetail
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'tools'))

from receiver import Receiver
from sender import send_file
from threading import Thread
from address import gethost, encode_username, decode_username
from storage import load_history, save_history
from storage import save_r_d, load_r_d 
from storage import load, set_, loadById
from storage import units_conv, format_file_name

from constant import *

#liste des clients
RECVS = []
"""
cette liste permet de garder une trace
de la connexion du client pour pouvoir
fermer cette connexion l'ors de l'arrêt brusque
du programme.

"""

class App(tk.Tk):
	def __init__(self):
		super().__init__()
		self.layout()
		self.config(bg=BACKGROUND)
		self.title(TITLE)
		self.screen_w = self.winfo_screenwidth()
		self.screen_h = self.winfo_screenheight()
		x = self.screen_w // 2 - 700 // 2
		y = self.winfo_screenheight() // 2 - 600 // 2
		# win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
		self.protocol("WM_DELETE_WINDOW", self.close_window)
		self.resizable(0,0)
		self.geometry("700x600+{}+{}".format(x,y))
		# self.eval("tk::PlaceWindow . center")
		self.filename = ""
		self.MODE = NORMAL
		self.style = Style(self)
		self.running = True

		self.style.configure("T.TButton", relief="flat", padding=0,background="#444")
		# self.style.configure("C.TButton", relief="flat", padding=0,background=RED)

		self.style.configure("TButton", relief="flat", padding=6,background="#444")

		self.style.configure("TCheckbutton", relief="flat", background=BACKGROUND, foreground=WHITE)


		self.style.map('T.TButton', foreground = [('active', '!disabled', "gray")],
					 background = [('active', 'gray')])

		self.style.map('C.TButton', foreground = [('active', '!disabled', RED)],
					 background = [('active', RED)])

		self.style.map('TButton', foreground = [('active', '!disabled', GREEN)],
					 background = [('active', '#384')])

		self.style.map('TCheckbutton', foreground = [('active', '!disabled', "gray")],
					 background = [('active', BACKGROUND)])



	def close_receiver_server(self):
		"""
		"""
		self.running = False
		if len(RECVS) == 1: RECVS[0].close()
		RECVS.remove(RECVS[0])
		self.MODE = NORMAL
		self.state_label.config(bg=B_BACKGROUND, text=READY_MSG)
		self.receiving_op_btn.config(text=RECEIVE_MSG, style="TButton", command=lambda : self.threading_func(START_RECEIVER_SERVER))

	def start_receiver_server(self):
		self.MODE = RECEIVE
		self.receiving_op_btn.config(text=STOP_MSG,style="C.TButton", command=self.close_receiver_server)
		self.username.set(encode_username())
		if self.port.get() == "":
			self.state_label.config(text=INVALID_PORT_MSG, bg=RED)
			#button.config(state="enable")
			return
		self.state_label.config(bg=GREEN)

		r = Receiver(gethost(), int(self.port.get()), self.state_label, self.Receivingprogress, self)
					# host, port, status_bar, progress_bar, current_object
		RECVS.clear()
		RECVS.append(r)

		filename, filesize = r.setup()
		data = {
				"file":os.path.basename(filename),
				"size": str(int(filesize)),
				"source":encode_username(),
				"date":date.today().strftime("%d/%m/%y")
			}
		save_history(data)
		self.reload_treeview(self.list)
		self.MODE = NORMAL
		self.start_receiver_server()
		#button.config(state="enable")


	def start_sending(self):
		if self.filename == "" or self.filename == () or len(self.filename) == 0:
			self.state_label.config(bg=RED, text=INVALID_FILE_MSG) 
			return
		if self.username.get() == "":
			self.state_label.config(bg=RED, text=INVALID_USER_MSG) 
			return
		if self.port.get() == "" or not self.port.get().isdigit():
			self.state_label.config(bg=RED, text=INVALID_PORT_MSG) 
			return
		
		try:
			username = decode_username(self.username.get())
		except:
			self.state_label.config(bg=RED, text=INVALID_USER_MSG) 
			return
		self.MODE = SEND
		try:
			for file in self.filename:
				send_file(host=username, port=self.port.get(),filename=file, state=self.state_label, progressBar=self.Receivingprogress, guiObj=self)
				data = {
					"file":file,
					"size": str(os.path.getsize(file)),
					"source":"Moi",
					"date":date.today().strftime("%d/%m/%y")

				}
				save_history(data)
				time.sleep(0.4)
				self.reload_treeview(self.list)
			self.file_label.config(text="")	
		except Exception as e:
			print(e)
			pass
		self.MODE = NORMAL
		self.filename = ()

	def threading_func(self,func):
		"""
		une gestion des évenements de click de buttons

		"""
		options = { START_RECEIVER_SERVER:self.start_receiver_server,
					START_SENDER_SERVER:self.start_sending
				}
		if func > len(options): return
		if self.MODE != NORMAL:
			messagebox.showwarning("Mode", MODE_ERROR_MSG)
			return
		thread = Thread(target=options[func])
		thread.start()
	

	def grid_conf(self,row, column):
		return {"row":row, "column":column, "pady":5,  "padx":5}

	def back_(self):
		self._r_f.pack_forget()
		self.top_frame.pack()
		self.button_frame.pack(expand=1)
		self.history_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10)

	def _format_file_name(self,file, size=15):
		return format_file_name(os.path.basename(file), size)
	
	def choose_directory(self):
		self.r_d.set(filedialog.askdirectory())
		save_r_d(self.r_d.get())
	def choose_file(self):
		self.filename = filedialog.askopenfilenames(title = CHOOSE_FILE_MSG)
		if len(self.filename) == 0: return
		self.file_label.config(text=f"{self._format_file_name(self.filename[0],50)} ({len(self.filename)})")

	def save_port(self, e):
		set_("main_port",self.main_port.get())
	def mode_sending(self):
		self.button_frame.pack_forget()
		self.top_frame.pack_forget()
		self.history_frame.pack_forget()

		self._r_f = tk.LabelFrame(self, text="Envoyer", **MAIN_STYLE)
		self._r_f.pack(fill=tk.X, padx=10, pady=20)

		self.history_frame.pack(fill=tk.X, padx=10)


		#choisir un fichier
		tk.Label(self._r_f, text="Etape 1: ", **MAIN_STYLE).grid(**self.grid_conf(0,0))
		self.choose_button = Button(self._r_f, text=CHOOSE_FILE_MSG, command=self.choose_file)
		self.choose_button.grid(**self.grid_conf(0,1))



		tk.Label(self._r_f, text="Etape 2: ", **MAIN_STYLE).grid(**self.grid_conf(1,0))
		tk.Label(self._r_f, text=f"Identifiant  : {self.username.get()}", **MAIN_STYLE).grid(**self.grid_conf(1,1))


		tk.Label(self._r_f, text="Etape 3: ", **MAIN_STYLE).grid(**self.grid_conf(2,0))

		button = Button(self._r_f, text=SEND_MSG, command=lambda : self.threading_func(START_SENDER_SERVER))
		button.grid(**self.grid_conf(2,1))

		self.file_label = tk.Label(self._r_f, fg=BLUE, bg=BACKGROUND)
		if len(self.filename) > 0:
			self.file_label.config(text=f"{self._format_file_name(self.filename[0],50)} ({len(self.filename)})")
		self.file_label.grid(**self.grid_conf(0,3), columnspan=2, sticky=tk.E)

		Button(self._r_f, text=BACK_MSG, command=self.back_).grid(**self.grid_conf(4,0))

			
	def reload_treeview(self,list):
		h = load_history()
		if len(h) > 0:
			for k,item in enumerate(h):
				self.insert_history_item(list,item, k)
	def insert_history_item(self, list,item, index):
		try:
			list.insert(parent='', index=index, iid=index, text='', 
									values=(self._format_file_name(os.path.basename(item["file"])),
									units_conv(str(item["size"]+" Bytes")),
									item["source"]))
		except:
			pass

	def OnClick(self, e):
		try:
			item = self.list.selection()[0]
			HDetail(self, self.screen_w, self.screen_h, loadById("history", int(item)))
		except IndexError:
			pass
		except Exception as e:
			print("Others Error accur "+e)

	def history(self):
		self.history_frame = tk.LabelFrame(self, text=HISTORY_MSG, height=300, **MAIN_STYLE)
		self.history_frame.pack(fill=tk.X, padx=10)

		self.Receivingprogress = Progressbar(self.history_frame, orient="horizontal", mode="determinate", value=0, max=1000)

		self.list = Treeview(self.history_frame, columns=("Fichier", "Taille", "Source"))
		self.list.bind('<Double-1>', self.OnClick)
		self.list.pack(fill=tk.X)

		self.list.heading("#0", text="", anchor=tk.CENTER)
		self.list.heading("Fichier", text="Fichier", anchor=tk.CENTER)
		self.list.heading("Taille", text="Taille", anchor=tk.CENTER)
		self.list.heading("Source", text="Source", anchor=tk.CENTER)
		self.reload_treeview(self.list)

		self.list.column("#0",stretch=tk.NO, width=0)
		self.list.column("Fichier",anchor=tk.CENTER, width=80)
		self.list.column("Taille",anchor=tk.CENTER, width=80)
		self.list.column("Source",anchor=tk.CENTER, width=80)
		
		
	def open_About(self):
		About(self, self.screen_w, self.screen_h)

	def config_UI(self):
		
		self.config_frame = tk.LabelFrame(self.top_frame, text="configuration", **MAIN_STYLE)
		self.config_frame.grid(row=0, column=0,sticky=tk.N, padx=4)

		tk.Label(self.config_frame, text="ID", **MAIN_STYLE).grid(**self.grid_conf(0,0))
		tk.Label(self.config_frame, text="Port", **MAIN_STYLE).grid(**self.grid_conf(1,0))

		self.username, self.port = tk.StringVar(), tk.StringVar()
		self.port.set(4000)
	

		user_input = tk.Entry(self.config_frame, textvariable=self.username)
		user_input.grid(**self.grid_conf(0,1));

		port_input = Entry(self.config_frame, textvariable=self.port)
		port_input.grid(**self.grid_conf(1,1))

		Button(self.config_frame, text="Save", style="T.TButton").grid(**self.grid_conf(3,0), columnspan=2)
	def setting_UI(self):
		self.r_d, self.main_port = tk.StringVar(), tk.StringVar()

		self.main_port.set(load("main_port"))
		self.r_d.set(load_r_d())
		
		self.setting_frame = tk.LabelFrame(self.top_frame, text="Paramétre", **MAIN_STYLE)
		self.setting_frame.grid(row=0, column=1, sticky=tk.N)
		tk.Label(self.setting_frame, text="Destination", **MAIN_STYLE).grid(**self.grid_conf(0,0), sticky=tk.W)
		tk.Label(self.setting_frame, text="Port principal", **MAIN_STYLE).grid(**self.grid_conf(1,0), sticky=tk.W)


		tk.Entry(self.setting_frame, width=20, textvariable=self.r_d, **ENTRY_FONT).grid(**self.grid_conf(0,1), sticky=tk.E)
		
		self.main_port_entry = tk.Entry(self.setting_frame, width=5,fg=WHITE,bg=B_BACKGROUND,textvariable=self.main_port, **ENTRY_FONT)
		self.main_port_entry.grid(**self.grid_conf(1,1), sticky=tk.E)
		self.main_port_entry.bind('<Return>', self.save_port)

		Checkbutton(self.setting_frame, text="Protocol Internet").grid(**self.grid_conf(2,0), sticky=tk.W)
		Checkbutton(self.setting_frame, text="Securité", name="sec").grid(**self.grid_conf(3,0), sticky=tk.W)

		Button(self.setting_frame, text="naviguer", style="T.TButton", command=self.choose_directory).grid(**self.grid_conf(0,3), sticky=tk.E)
		Button(self.setting_frame, text="Metre à jour").grid(**self.grid_conf(4,1), columnspan=2,  sticky=tk.E)
		Button(self.setting_frame, text="Info", command=self.open_About).grid(**self.grid_conf(4,3), columnspan=2,  sticky=tk.E)



	def main_actions_btn_IU(self):
		self.button_frame = tk.Frame(self, height=200, width=300, bg=BACKGROUND )
		self.button_frame.pack(expand=1)

		self.receiving_op_btn = Button(self.button_frame, text=RECEIVE_MSG, command=lambda : self.threading_func(START_RECEIVER_SERVER))
		self.receiving_op_btn.pack(side=tk.LEFT, padx=5, pady=4)

		self.sending_op_btn = Button(self.button_frame, text=SEND_MSG, command=self.mode_sending )
		self.sending_op_btn.pack(side=tk.RIGHT, padx=5, pady=4)

		self.state_label = tk.Label(self, text=READY_MSG, bg=B_BACKGROUND, fg=WHITE)
		self.state_label.pack(side=tk.BOTTOM, fill=tk.X)

	def layout(self):
		label = tk.Label(self, text=APP_LABEL,  font=("Roboto", 15, "italic", "underline"), bg=B_BACKGROUND, fg=WHITE)
		label.pack(fill=tk.BOTH, expand=1)

		self.top_frame = tk.Frame(self,bg=BACKGROUND)
		self.top_frame.pack()

		self.config_UI()
		self.setting_UI()
		
		
		self.main_actions_btn_IU()
		self.history()


	def close_window(self):
		if len(RECVS) == 1 : RECVS[0].close()
		self.destroy()



	
