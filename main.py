import random
import tkinter as tk
root = tk.Tk()
root.title("Сапёр")
root.geometry("500x500")
root.minsize(500, 500) # ширина, высота


w = 10
h = 10
bombs = 10
win_var = tk.IntVar(value=0)
lose_var = tk.IntVar(value=0)
w_var = tk.IntVar(value=10)
h_var = tk.IntVar(value=10)
bombs_var = tk.IntVar(value=10)
bomb = []
map = []

for i in range(w):
    root.columnconfigure(i, weight=1)
for i in range(h):
    root.rowconfigure(i + 3, weight=1)

def inc_w():
    w_var.set(w_var.get()+1)
def dec_w():
    if w_var.get() >= 6:
        w_var.set(w_var.get()-1)
def inc_h():
    h_var.set(h_var.get()+1)
def dec_h():
    if h_var.get() >= 6:
        h_var.set(h_var.get()-1)
def inc_bomb():
    if bombs_var.get() < (w_var.get()*h_var.get()-2):
        bombs_var.set(bombs_var.get()+1)
def dec_bomb():
    if bombs_var.get() >= 1:
        bombs_var.set(bombs_var.get()-1)

top_frame = tk.Frame(root)
top_frame.grid(row=0, column=0, columnspan=w, pady=10, padx=10, sticky="ew")

#Ширина
btn_minus_w = tk.Button(top_frame, text="-", command=dec_w, width=2)
btn_minus_w.pack(side="left", padx=2)

label_text_w = tk.Label(top_frame, text="Ширина:", font=("Arial", 10))
label_text_w.pack(side="left", padx=2)

display_w = tk.Label(top_frame, textvariable=w_var, font=("Arial", 10, "bold"))
display_w.pack(side="left", padx=2)

btn_plus_w = tk.Button(top_frame, text="+", command=inc_w, width=2)
btn_plus_w.pack(side="left", padx=2)

#Высота
btn_plus_h = tk.Button(top_frame, text="+", command=inc_h, width=2)
btn_plus_h.pack(side="right", padx=2)

display_h = tk.Label(top_frame, textvariable=h_var, font=("Arial", 10, "bold"))
display_h.pack(side="right", padx=2)

label_text_h = tk.Label(top_frame, text="Высота:", font=("Arial", 10))
label_text_h.pack(side="right", padx=2)

btn_minus_h = tk.Button(top_frame, text="-", command=dec_h, width=2)
btn_minus_h.pack(side="right", padx=2)

#бомбы
center_container = tk.Frame(top_frame)
center_container.pack(side="left", expand=True)

btn_plus_bomb = tk.Button(center_container, text="+", command=inc_bomb, width=2)
btn_plus_bomb.pack(side="right", padx=2)

display_bomb = tk.Label(center_container, textvariable=bombs_var, font=("Arial", 10, "bold"))
display_bomb.pack(side="right", padx=2)

label_text_bomb = tk.Label(center_container, text="Бомбы:", font=("Arial", 10))
label_text_bomb.pack(side="right", padx=2)

btn_minus_bomb = tk.Button(center_container, text="-", command=dec_bomb, width=2)
btn_minus_bomb.pack(side="right", padx=2)

#победы, проигрыши.
bottom_container = tk.Frame(root)
bottom_container.grid(row=2, column=0, columnspan=w, pady=10, padx=10, sticky="ew")

label_text_win = tk.Label(bottom_container, text="Выигрышей:", font=("Arial", 10))
label_text_win.pack(side="left", padx=2)

display_win = tk.Label(bottom_container, textvariable=win_var, font=("Arial", 10, "bold"))
display_win.pack(side="left", padx=2)

display_lose = tk.Label(bottom_container, textvariable=lose_var, font=("Arial", 10, "bold"))
display_lose.pack(side="right", padx=2)

label_text_lose = tk.Label(bottom_container, text="Проигрышей:", font=("Arial", 10))
label_text_lose.pack(side="right", padx=2)

#рестарт
def restart():
    global w, h, bombs
    w = w_var.get()
    h = h_var.get()
    bombs = bombs_var.get()
    for i in map:
        for j in i:
            j.btn.destroy()
    for i in range(root.grid_size()[0]):
        root.columnconfigure(i, weight=0)
    for i in range(root.grid_size()[1]):
        root.rowconfigure(i, weight=0)
    for i in range(w):
        root.columnconfigure(i, weight=1)
    for i in range(h):
        root.rowconfigure(i + 3, weight=1)
    bomb.clear()
    map.clear()
    cellcreator()
    bombcreator()

bottom_center_container = tk.Frame(bottom_container)
bottom_center_container.pack(side="left", expand=True)

btn_restart = tk.Button(bottom_center_container, text="Рестарт", command=restart, width=10)
btn_restart.pack(side="right", padx=2)
class Cell:
    def __init__(self, row, col, mine, bombs, open):
        self.row = row
        self.col = col
        self.mine = mine
        self.bombs = bombs
        self.open = open
        self.btn = tk.Button(root, text="", command=self.click)
        self.btn.grid(row=row + 3, column=col, sticky="nsew", padx=1, pady=1)
        self.btn.bind("<Button-3>", self.rightclick)
    def rightclick(self, event):
        if self.open == 0:
            if self.btn.cget("text") == "P":
                self.btn.config(text="", fg="black")
            else:
                self.btn.config(text="P", fg="red")
    def click(self):
        if self.open == 1 or self.btn.cget("text") == "P":
            return
        self.open = 1
        if self.mine == 1:
            for i in range(len(map)):
                for j in range(len(map[i])):
                    if map[i][j].mine == 1:
                        map[i][j].btn.config(text="X", bg="red")
            root.after(1000, restart)
            lose_var.set(lose_var.get() + 1)
        elif self.bombs == 0:
            self.btn.config(text=f"{self.bombs}", bg="lightgray", fg="black")
            openaround(self.row, self.col)
            countopen = 0
            for i in range(len(map)):
                for j in range(len(map[i])):
                    if map[i][j].open == 1:
                        countopen += 1
            if countopen == (w * h - bombs):
                win_var.set(win_var.get() + 1)
                root.after(1000, restart)
        else:
            self.btn.config(text=f"{self.bombs}", bg="lightgray", fg="black")
            countopen = 0
            for i in range(len(map)):
                for j in range(len(map[i])):
                    if map[i][j].open == 1:
                        countopen += 1
            if countopen == (w*h-bombs):
                win_var.set(win_var.get() + 1)
                root.after(1000, restart)


def openaround(x, y):
    valid = countvalid(x, y)
    another = []
    for i in valid:
        if map[i[0]][i[1]].open == 0 and map[i[0]][i[1]].btn.cget("text") != "P":
            if map[i[0]][i[1]].bombs == 0:
                another.append([i[0], i[1]])
            map[i[0]][i[1]].open = 1
            map[i[0]][i[1]].btn.config(text=f"{map[i[0]][i[1]].bombs}", bg="lightgray")
    if len(another) != 0:
        for i in another:
            openaround(i[0], i[1])
def countvalid(x, y):
    valid = []
    around2 = {0: [x - 1, y - 1],
               1: [x - 0, y - 1],
               2: [x + 1, y - 1],
               3: [x - 1, y - 0],
               4: [x - 1, y + 1],
               5: [x - 0, y + 1],
               6: [x + 1, y + 1],
               7: [x + 1, y - 0]}
    for i in range(8):
        if (around2[i][0] < h and around2[i][0] >= 0) and (around2[i][1] < w and around2[i][1] >= 0):
            valid.append(around2[i])
    return valid
def amountbombs(x, y):
    count = 0
    valid = countvalid(x, y)
    for i in valid:
        if map[i[0]][i[1]].mine == 1:
            count += 1
    return count
def bombcreator():
    for i in range(bombs):
        while True:
            f = [random.randint(0, h - 1), random.randint(0, w - 1)]
            if f not in bomb:
                bomb.append(f)
                map[f[0]][f[1]].mine = 1
                break
    for i in range(len(map)):
        for j in range(len(map[i])):
            map[i][j].bombs = amountbombs(i, j)
def cellcreator():
    for row_index in range(h):
        list1 = []
        for col_index in range(w):
            cell = Cell(row_index, col_index, 0, 0, 0)
            list1.append(cell)
        map.append(list1)
cellcreator()
bombcreator()
root.mainloop()
