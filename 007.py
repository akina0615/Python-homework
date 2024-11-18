import tkinter


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
            "title": "DNA突变点查找",
            "label_n": "请输入兔子要繁殖多少代:",
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
        self.__combo_box__(window, 20, 5, 265, 60, 1, 1000)

        window.resizable(False, False)
        window.mainloop()

    def __create_label__(self, master, text, width, height):
        return tkinter.Label(master, text=text, font=self.config["font"],
                             width=width, height=height)

    def __create_text__(self, master, width, height):
        return tkinter.Text(master, font=self.config["font"], width=width, height=height)

    def __create_entry__(self, master, width, var):
        return tkinter.Entry(master, font=self.config["font"], width=width, textvariable=var)

    def __combo_box__(self, master, width, height, x, y, range_a, range_b):
        var1 = tkinter.StringVar()
        entry_n = self.__create_entry__(master, width=width, var=var1)
        entry_n.place(x=x, y=y)
        listbox = tkinter.Listbox(master, width=width, height=height)

        def entry_n_bind(event):
            listbox.place(x=x, y=y+12)
            for i in range(range_a, range_b):
                listbox.insert("end", str(i))
                # scroll

        def listbox_curselection(event):
            index = listbox.curselection()[0]
            listbox.activate(index)
            var1.set(listbox.get(index))
            listbox.place_forget()

        entry_n.bind("<Button-1>", entry_n_bind)
        listbox.bind("<ButtonRelease-1>", listbox_curselection)


if __name__ == '__main__':
    test = Frame()

# 2024/11/18:author: @孙伟嘉 注:未来可以考虑增加一个输入起始兔子数量的功能
