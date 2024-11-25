import tkinter
import tkinter.ttk
from tkinter import messagebox

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class Segregation:
    def __init__(self, k, m, n):
        self._k = k
        self._m = m
        self._n = n
        self._t = self._k + self._m + self._n
        if self._t <= 1:
            pass
        self._probability = {'显性纯合子占比': 0, '显性杂合子占比': 0, '隐性纯合子占比': 0}
        self._segregation_()

    def _segregation_(self):
        self._probability['显性纯合子占比'] = (self._k * self._k - self._k + self._k * self._m +
                                               0.25 * self._m * self._m - 0.25 * self._m) / (
                                                      self._t * self._t - self._t)
        self._probability['显性杂合子占比'] = (
                                                      0.5 * self._m * self._m - 0.5 * self._m + self._k * self._m + 2 * self._k * self._n + self._m * self._n) / \
                                              (self._t * self._t - self._t)
        self._probability['隐性纯合子占比'] = (self._n * self._n - self._n + self._m * self._n +
                                               0.25 * self._m * self._m - 0.25 * self._m) / (
                                                      self._t * self._t - self._t)

    def get_probability(self):
        return self._probability


class Frame:
    def __init__(self):
        self.config = {
            "geometry": "800x600+200+200",
            "size_x": 800,
            "size_y": 600,
            "font": ("Arial", 12),
            "title": "孟德尔第一定律",
            "label_k": "显性纯合个体数:",
            "label_m": "杂合个体数:",
            "label_n": "隐性纯合个体数:",
            "button": "求解",
            "author": "Thank you for your use, author @ 孙伟嘉"
        }
        window = tkinter.Tk()
        window.geometry(self.config["geometry"])
        window.title(self.config["title"])
        label_author = self._create_label_(window, text=self.config["author"],
                                           width=40, height=3)
        label_author.pack(side="bottom")
        frame_1 = self._create_frame_(window, width=self.config["size_x"] / 3, height=100)
        frame_1.place(x=0, y=0)
        frame_2 = self._create_frame_(window, width=self.config["size_x"] / 3, height=100)
        frame_2.place(x=0 + self.config["size_x"] / 3, y=0)
        frame_3 = self._create_frame_(window, width=self.config["size_x"] / 3, height=100)
        frame_3.place(x=0 + 2 * self.config["size_x"] / 3, y=0)
        label_k = self._create_label_(frame_1, text=self.config["label_k"], width=15, height=2)
        label_k.pack(side='left', pady=50)
        label_m = self._create_label_(frame_2, text=self.config["label_m"], width=15, height=2)
        label_m.pack(side='left', pady=50)
        label_n = self._create_label_(frame_3, text=self.config["label_n"], width=15, height=2)
        label_n.pack(side='left', pady=50)

        combobox_values = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
        var_k = tkinter.StringVar
        combobox_k = self._create_combobox_(frame_1, var=var_k, values=combobox_values)
        combobox_k.pack(side='right', pady=50)
        var_m = tkinter.StringVar
        combobox_m = self._create_combobox_(frame_2, var=var_m, values=combobox_values)
        combobox_m.pack(side='right', pady=50)
        var_n = tkinter.StringVar
        combobox_n = self._create_combobox_(frame_3, var=var_n, values=combobox_values)
        combobox_n.pack(side='right', pady=50)

        def button_calculate_f():
            k = combobox_k.get()
            m = combobox_m.get()
            n = combobox_n.get()
            if k == '' or m == '' or n == '':
                messagebox.showwarning(title='警告', message='输入存在空值')
                return
            seg = Segregation(k=int(k), m=int(m), n=int(n))
            # print(seg.get_probability())
            d = Draw(master=window)
            index = list(seg.get_probability().keys())
            data = list(seg.get_probability().values())
            d.draw_chart(data, index, {"x": 7, "y": 4}, title="基因型在群体中的比率", x_label="基因型", y_label="占比",
                         location={"x": 60, "y": 200})
            pass

        button_calculate = self._create_button_(window, width=5, height=1, button_click=button_calculate_f)
        button_calculate.place(x=740, y=100)

        window.resizable(False, False)
        window.mainloop()

    @staticmethod
    def _create_frame_(master, width, height):
        return tkinter.Frame(master, width=width, height=height)

    def _create_label_(self, master, text, width, height):
        return tkinter.Label(master, text=text, font=self.config["font"],
                             width=width, height=height)

    def _create_text_(self, master, width, height):
        return tkinter.Text(master, font=self.config["font"], width=width, height=height)

    def _create_entry_(self, master, width, var):
        return tkinter.Entry(master, font=self.config["font"], width=width, textvariable=var)

    def _create_button_(self, master, width, height, button_click):
        return tkinter.Button(master, text=self.config["button"], font=self.config["font"],
                              width=width, height=height, command=button_click)

    def _create_combobox_(self, master, var, values: tuple, width=10, height=2):
        return tkinter.ttk.Combobox(master, textvariable=var, font=self.config["font"],
                                    value=values, width=width, height=height)


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
        bars = ax.bar(index, data, color=['red', 'green', 'blue'])
        ax.set_ylim(0, 1)
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.set_title(title)
        for bar, height in zip(bars, data):
            y_val = round(height,5)
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
