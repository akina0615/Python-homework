import tkinter
from tkinter import messagebox

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class Fib:
    def __init__(self, tup: tuple[int, int] = (5, 3), method=1):
        self.__fib_list = []
        self.__fib_num = 0
        self.__n = tup[0]
        self.__k = tup[1]
        if method == 1:
            self.__fib_method_1__()
        elif method == 2:
            self.__fib_num = self.__fib_method_2__(self.__n - 1, self.__k)

    def __fib_method_1__(self):
        i = 0
        start_num = 1
        self.__fib_list.append(start_num)
        self.__fib_list.append(start_num)
        while i + 2 < self.__n:
            self.__fib_list.append(self.__k * self.__fib_list[i] + self.__fib_list[i + 1])
            i += 1
        self.__fib_num = self.__fib_list[-1]

    def __fib_method_2__(self, i, j):
        if i == 0 or i == 1:
            return 1
        else:
            return j * self.__fib_method_2__(i - 2, j) + self.__fib_method_2__(i - 1, j)

    @property
    def get_feb_list(self):
        return self.__fib_list

    @property
    def get_fib_num(self):
        return self.__fib_num


class Frame:
    def __init__(self):
        self.config = {
            "geometry": "800x600+200+200",
            "font": ("Arial", 12),
            "title": "兔子问题和递推",
            "label_n": "请输入兔子要繁殖多少代:",
            "label_k": "请输入兔子要繁殖多少对:",
            "button": "求解",
            "author": "Thank you for your use, author @ 孙伟嘉"
        }
        window = tkinter.Tk()
        window.geometry(self.config["geometry"])
        window.title(self.config["title"])
        label_author = self.__create_label__(window, text=self.config["author"],
                                             width=40, height=3)
        label_author.pack(side="bottom")
        label_n = self.__create_label__(window, text=self.config["label_n"],
                                        width=20, height=2)
        label_n.place(x=65, y=50)
        label_k = self.__create_label__(window, text=self.config["label_k"],
                                        width=20, height=2)
        label_k.place(x=365, y=50)
        entry_n = self.__combo_box__(window, width=10, height=5, x=265, y=60, range_a=1, range_b=100)
        entry_k = self.__combo_box__(window, width=10, height=5, x=565, y=60, range_a=1, range_b=100)

        def f():
            if not entry_n.get() or not entry_k.get():
                messagebox.showwarning(title="警告", message="请先输入")
                return
            tup = (int(entry_n.get()), int(entry_k.get()))
            fib = Fib(tup=tup, method=1)
            fib_list = fib.get_feb_list
            fib_num = fib.get_fib_num
            messagebox.showinfo(title="求解结果", message=f"经过{entry_n.get()}代繁殖后,共有{fib_num}对兔子.")
            d = Draw(window)
            fib_index = d.create_index(fib_list)
            d.draw_chart(x_data=fib_list, x_index=fib_index, pic_size={"x": 7, "y": 4}, title="柱形示意图",
                         y_label="对数", x_label="代", location={"x": 50.0, "y": 180.0})
            pass

        button_calculate = self.__create_button__(window, width=5, height=1, button_click=f)
        button_calculate.place(x=680, y=55)

        window.resizable(False, False)
        window.mainloop()

    def __create_label__(self, master, text, width, height):
        return tkinter.Label(master, text=text, font=self.config["font"],
                             width=width, height=height)

    def __create_text__(self, master, width, height):
        return tkinter.Text(master, font=self.config["font"], width=width, height=height)

    def __create_entry__(self, master, width, var):
        return tkinter.Entry(master, font=self.config["font"], width=width, textvariable=var)

    def __create_button__(self, master, width, height, button_click):
        return tkinter.Button(master, text=self.config["button"], font=self.config["font"], width=width, height=height,
                              command=button_click)

    def __combo_box__(self, master, width, height, x, y, range_a, range_b):
        var1 = tkinter.StringVar()
        entry = self.__create_entry__(master, width=width, var=var1)
        entry.place(x=x, y=y)
        scroll = tkinter.Scrollbar(master, orient="vertical")
        listbox = tkinter.Listbox(master, width=width, height=height)
        listbox.config(yscrollcommand=scroll.set)
        for i in range(range_a, range_b):
            listbox.insert("end", str(i))
        scroll.config(command=listbox.yview)

        def entry_n_bind(event):
            listbox.place(x=x, y=y + 20)
            scroll.place(x=x + 80, y=y + 30)

        def listbox_curselection(event):
            index = listbox.curselection()[0]
            listbox.activate(index)
            var1.set(listbox.get(index))
            listbox.place_forget()
            scroll.place_forget()

        entry.bind("<Button-1>", entry_n_bind)
        listbox.bind("<ButtonRelease-1>", listbox_curselection)
        return entry


class Draw:
    def __init__(self, master):
        self.__master = master

    def draw_chart(self, x_data, x_index, pic_size: dict[float:float] = {"x": 7, "y": 3}, title="", x_label="x",
                   y_label="y",
                   location: dict[str:float] = {"x": 60.0, "y": 250.0}):
        plt.rcParams["font.sans-serif"] = ["SimHei"]
        plt.rcParams["axes.unicode_minus"] = False
        data = x_data
        index = x_index
        fig = Figure(figsize=(pic_size["x"], pic_size["y"]), dpi=100)
        ax = fig.add_subplot(111)
        bars = ax.bar(index, data, color=['red'])
        ax.set_ylim(0, max(data) + 1)
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.set_title(title)
        for bar, height in zip(bars, data):
            y_val = height
            ax.text(bar.get_x() + bar.get_width() / 2 - 0.1, y_val,
                    y_val, ha='center', va='bottom')
        canvas = FigureCanvasTkAgg(fig, master=self.__master)
        canvas.draw()
        canvas.get_tk_widget().place(x=location["x"], y=location["y"])
        pass

    @staticmethod
    def create_index(data_list: list):
        index = []
        for i in range(len(data_list)):
            index.append(i + 1)
        return index


if __name__ == '__main__':
    test = Frame()

# 2024/11/18:author: @孙伟嘉 注:未来可以考虑增加一个输入起始兔子数量的功能
