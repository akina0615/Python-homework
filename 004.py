import time
import tkinter
from tkinter import filedialog, messagebox

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class MatchDna():
    def __init__(self, dna):
        self.__dna = dna.upper()[:-1]
        self.__r_dna = self.__dna[::-1]
        self.__match__()

    def __match__(self):
        self.__r_dna = self.__r_dna.replace('A', 'temp1')
        self.__r_dna = self.__r_dna.replace('T', 'temp2')
        self.__r_dna = self.__r_dna.replace('G', 'temp3')
        self.__r_dna = self.__r_dna.replace('C', 'temp4')
        self.__r_dna = self.__r_dna.replace('temp1', 'T')
        self.__r_dna = self.__r_dna.replace('temp2', 'A')
        self.__r_dna = self.__r_dna.replace('temp3', 'C')
        self.__r_dna = self.__r_dna.replace('temp4', 'G')

    def get_r(self):
        return self.__r_dna


class Frame:
    str_data = None
    read_path = None
    save_path = None

    def __init__(self):
        config = {
            "geometry": "800x600+200+200",
            "font": ("Arial", 12),
            "title": "DNA反向互补序列",
            "label1": "待匹配的碱基序列:",
            "label2": "从文件中导入:",
            "label3": "翻译结果:",
            "label4": "导出路径:",
            "button1": "匹配",
            "button2": "浏览",
            "button3": "导出",
            "button4": "浏览",
            "filename": "",
            "author": "Thank you for your use, author @ 孙伟嘉"
        }
        window = tkinter.Tk()
        window.geometry(config["geometry"])
        window.title(config["title"])
        tkinter.Label(window, text=config["author"], font=config["font"], width=40, height=3).pack(side="bottom")
        tkinter.Label(window, text=config["label1"], font=config["font"], width=20, height=2).place(x=50, y=50)
        tkinter.Label(window, text=config["label2"], font=config["font"], width=20, height=2).place(x=65, y=100)
        tkinter.Label(window, text=config["label3"], font=config["font"], width=20, height=2).place(x=65, y=150)
        tkinter.Label(window, text=config["label4"], font=config["font"], width=20, height=2).place(x=65, y=200)
        text1 = tkinter.Text(window, font=config["font"], width=50, height=1.5)
        text1.place(x=230, y=50)
        text2 = tkinter.Text(window, font=config["font"], width=50, height=1.5)
        text2.place(x=230, y=100)
        text3 = tkinter.Text(window, state=tkinter.DISABLED, font=config["font"], width=50, height=1.5)
        text3.place(x=230, y=150)
        text4 = tkinter.Text(window, font=config["font"], width=50, height=1.5)
        text4.place(x=230, y=200)

        def button1_click():
            self.str_data = text1.get("1.0", "end")
            match = MatchDna(self.str_data)
            if self.str_data != '\n' and self.str_data:
                text3.config(state=tkinter.NORMAL)
                text3.delete("1.0", "end")
                text3.insert("1.0", match.get_r())
                text3.config(state=tkinter.DISABLED)
                self.__draw_pie__(window, match.get_r())

            else:
                messagebox.showwarning(title='警告', message='请先导入或输入DNA序列!')

        tkinter.Button(window, text=config["button1"], font=config["font"], width=5, height=1,
                       command=button1_click).place(x=700, y=55)

        def button2_click():
            if self.__select_file__():
                text1.delete("1.0", "end")
                text1.insert("1.0", self.str_data)
                text2.delete("1.0", "end")
                text2.insert("1.0", self.read_path)

        tkinter.Button(window, text=config["button2"], font=config["font"], width=5, height=1,
                       command=button2_click).place(x=700, y=105)

        def button3_click():
            if self.save_path:
                if text3.get("1.0", "end") != '\n' and text3.get("1.0", "end"):
                    if text4.get("1.0", "end").rfind(".") != -1:
                        filename = text4.get("1.0", "end")[0:-1]
                    else:
                        filename = "" + self.save_path + '/' + time.strftime("%Y-%m-%d %H°%M'%S''.txt",
                                                                             time.localtime())
                    with open(filename, 'w') as fh:
                        fh.write(text3.get("1.0", "end"))
                        messagebox.showinfo(title="提示", message="导出成功")
                else:
                    messagebox.showwarning(title='警告', message="匹配内容为空!")
            else:
                messagebox.showwarning(title='错误', message='路径不存在!')

        tkinter.Button(window, text=config["button3"], font=config["font"], width=5, height=1,
                       command=button3_click).place(x=700, y=155)

        def button4_click():
            self.save_path = filedialog.askdirectory(title="导出文件")
            if self.save_path:
                text4.delete("1.0", "end")
                text4.insert("1.0", self.save_path)
            else:
                messagebox.showwarning(title='错误', message='文件不存在!')

        tkinter.Button(window, text=config["button4"], font=config["font"], width=5, height=1,
                       command=button4_click).place(x=700, y=205)

        window.mainloop()

    def __select_file__(self):
        file_path = filedialog.askopenfilename(title="选择文件")
        if file_path:
            self.read_path = file_path
            self.__read_file__()
            return True
        else:
            messagebox.showwarning(title='错误', message='文件不存在!')
            return False

    def __read_file__(self):
        with open(self.read_path, 'r') as fh:
            self.str_data = fh.read().upper()

    def __draw_pie__(self, master, str1):
        def __select_dict__(str_t):
            dict_t = {}
            for c in str_t:
                if c in list(dict_t.keys()):
                    dict_t[c] += 1
                else:
                    dict_t[c] = 1
            return dict_t

        dict1 = __select_dict__(str1)
        plt.rcParams["font.sans-serif"] = ["SimHei"]
        plt.rcParams["axes.unicode_minus"] = False
        fig = Figure(figsize=(3, 3), dpi=100)
        ax = fig.add_subplot(111)
        ax.axis('equal')
        sizes = list(dict1.values())
        labels = list(dict1.keys())
        ax.pie(sizes, labels=labels, autopct='%1.1f%%')
        ax.set_title("氨基酸占比图")
        canvas = FigureCanvasTkAgg(fig, master=master)
        canvas.draw()
        canvas.get_tk_widget().place(x=100, y=250)
        self.__draw_chart__(master, dict1)

    def __draw_chart__(self, master, data_dict):
        plt.rcParams["font.sans-serif"] = ["SimHei"]
        plt.rcParams["axes.unicode_minus"] = False
        data = data_dict.values()
        index = data_dict.keys()
        fig = Figure(figsize=(3, 3), dpi=100)
        ax = fig.add_subplot(111)
        bars = ax.bar(index, data, color=['blue', 'green', 'red', 'purple', 'gray'])
        ax.set_ylim(0, max(data) + 1)
        ax.set_xlabel('氨基酸类型')
        ax.set_ylabel('数量')
        ax.set_title('氨基酸统计')
        for bar, height in zip(bars, data):
            y_val = height
            ax.text(bar.get_x() + bar.get_width() / 2 - 0.1, y_val,
                    str(y_val), ha='center', va='bottom')
        canvas = FigureCanvasTkAgg(fig, master=master)
        canvas.draw()
        canvas.get_tk_widget().place(x=400, y=250)
        pass


if __name__ == '__main__':
    test = Frame()
