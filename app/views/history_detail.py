import tkinter
from tkinter.ttk import Button
from functools import wraps
import os, sys
sys.path.append(
	os.path.join(
		os.path.dirname("__name__"),
		"tools"
		)
	)
from constant import BACKGROUND, MAIN_STYLE
from storage import getFileType, cutFileName, units_conv








class HDetail:
	def __init__(self, parent, w,h,data):
		self.parent = parent
		self.screen_w = w
		self.screen_h = h
		self.data = data
		self.window = tkinter.Toplevel(self.parent)
		x = self.screen_w // 2 - 300 // 2
		y = self.screen_h // 2 - 130 // 2
		self.window.config(bg=BACKGROUND)
		self.window.geometry("530x270+{}+{}".format(x,y))
		self.window.resizable(0, 0)
		self.window.transient(self.parent)
		self.window.protocol("WM_DELETE_WINDOW", self.Close_Window)
		self.parent.wm_attributes("-disabled", True)
		self.layout()

	def layout(self) -> None:
		
		# f1 = tkinter.Frame(self.window, bg=BACKGROUND)
		f2 = tkinter.Frame(self.window, bg=BACKGROUND)
		# p = 
		image=  tkinter.PhotoImage(file=os.path.dirname(__file__)+"/assets/folder.gif")

		tkinter.Label(self.window, text="Trensfert Information", font=("helvetica", 16, "italic") , **MAIN_STYLE).pack(side="top", pady=6)

		# tkinter.Label(f1, text="Type Image ", font=("helvetica", 10, "italic") , image=image,**MAIN_STYLE).pack()

		tkinter.Label(f2, text="Nom du ficher : ", font=("helvetica", 10, "italic"), **MAIN_STYLE).grid(row=1, column=0, sticky="w")
		tkinter.Label(f2, text=cutFileName(self.data["file"]), font=("helvetica", 8, "italic"), **MAIN_STYLE).grid(row=1, column=1, sticky="e")

		tkinter.Label(f2, text="Date :", font=("helvetica", 10, "italic"), **MAIN_STYLE).grid(row=2, column=0, sticky="w")
		tkinter.Label(f2, text=self.data.get("date","unknown"), font=("helvetica", 10, "italic"), **MAIN_STYLE).grid(row=2, column=1, sticky="e")


		tkinter.Label(f2, text="Source :", font=("helvetica", 10, "italic"), **MAIN_STYLE).grid(row=3, column=0, sticky="w")
		tkinter.Label(f2, text=self.data["source"], font=("helvetica", 10, "italic"), **MAIN_STYLE).grid(row=3, column=1, sticky="e")

		tkinter.Label(f2, text="Taille :", font=("helvetica", 10, "italic"), **MAIN_STYLE).grid(row=4, column=0, sticky="w")
		tkinter.Label(f2, text=units_conv(self.data["size"]+" Bytes"), font=("helvetica", 10, "italic"), **MAIN_STYLE).grid(row=4, column=1, sticky="e")


		tkinter.Label(f2, text="Type de de fichier :", font=("helvetica", 10, "italic"), **MAIN_STYLE).grid(row=5, column=0, sticky="w")
		tkinter.Label(f2, text=getFileType(self.data["file"]), font=("helvetica", 10, "italic"), **MAIN_STYLE).grid(row=5, column=1, sticky="e")


		Button(self.window, text="fermé", command=self.Close_Window).pack(side="bottom", pady=6)


		# f1.pack(side="left", expand=1)
		f2.pack(expand=1)

	def Close_Window(self) -> None:
		# IMPORTANT!
		self.parent.wm_attributes("-disabled", False) # IMPORTANT!

		self.window.destroy()
		# Possibly not needed, used to focus parent window again
		self.parent.deiconify()

if __name__ == "__main__":
	pass