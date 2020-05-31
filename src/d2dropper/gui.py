import tkinter as tk

window = tk.Tk()
window.title("D2 Dropper a Helper  for Limedrop")


canvas = tk.Canvas(window, width=450, height=500)
canvas.pack()


frame = tk.Frame(window, bg="red")
frame.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.9)

search_entry_field = tk.Entry(frame, bd='3', justify='center')


window.mainloop()
