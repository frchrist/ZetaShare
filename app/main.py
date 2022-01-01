import sys, os
sys.path.append(
	os.path.join(
		os.path.dirname(__file__), 'views')
	)

from views.main import App



if __name__ == '__main__':
	App().mainloop()