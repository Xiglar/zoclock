import tkinter as tk

# create window
window = tk.Tk()
window.title('test')
window.geometry('800x500')

# create widget
text = tk.Text(master = window)
text.pack()

# run
window.mainloop()