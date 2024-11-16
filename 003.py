import tkinter
import time
from tkinter import filedialog, messagebox

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class Translation:
    def __init__(self, rna):
        self.__rna = rna
        self.__protein = ""
        self.__table = {
            'U': {
                'UUU': 'F', 'UUC': 'F', 'UUA': 'L', 'UUG': 'L',
                'UCU': 'S', 'UCC': 'S', 'UCA': 'S', 'UCG': 'S',
                'UAU': 'Y', 'UAC': 'Y', 'UAA': 'Stop', 'UAG': 'Stop',
                'UGU': 'C', 'UGC': 'C', 'UGA': 'Stop', 'UGG': 'W'
            },
            'C': {
                'CUU': 'L', 'CUC': 'L', 'CUA': 'L', 'CUG': 'L',
                'CCU': 'P', 'CCC': 'P', 'CCA': 'P', 'CCG': 'P',
                'CAU': 'H', 'CAC': 'H', 'CAA': 'Q', 'CAG': 'Q',
                'CGU': 'R', 'CGC': 'R', 'CGA': 'R', 'CGG': 'R'
            },
            'A': {
                'AUU': 'I', 'AUC': 'I', 'AUA': 'I', 'AUG': 'M',
                'ACU': 'T', 'ACC': 'T', 'ACA': 'T', 'ACG': 'T',
                'AAU': 'N', 'AAC': 'N', 'AAA': 'K', 'AAG': 'K',
                'AGU': 'S', 'AGC': 'S', 'AGA': 'R', 'AGG': 'R'
            },
            'G': {
                'GUU': 'V', 'GUC': 'V', 'GUA': 'V', 'GUG': 'V',
                'GCU': 'A', 'GCC': 'A', 'GCA': 'A', 'GCG': 'A',
                'GAU': 'D', 'GAC': 'D', 'GAA': 'E', 'GAG': 'E',
                'GGU': 'G', 'GGC': 'G', 'GGA': 'G', 'GGG': 'G'
            }
        }
        self.__translation__()

    def get_protein(self):
        return self.__protein

    def __translation__(self):
        buffer = []
        countPtr = 0
        for c in self.__rna:
            if c == 'A' or c == 'C' or c == 'G' or c == 'U':
                buffer.append(c)
                countPtr += 1
                if countPtr % 3 == 0:
                    cipher = "" + buffer[0] + buffer[1] + buffer[2]
                    temp_protein = self.__table[buffer[0]][cipher]
                    if temp_protein == "Stop":
                        break
                    else:
                        self.__protein += temp_protein
                    buffer.clear()
            else:
                # author:孙伟嘉 注:这里面对非法碱基应当有两种处理策略,一个是整个密码子全部抛弃,一个是跳过,这里选择第二种策略
                continue


class Frame:
    str_data = None
    read_path = None
    save_path = None

    def __init__(self):
        config = {
            "geometry": "800x600+200+200",
            "font": ("Arial", 12),
            "title": "RNA翻译",
            "label1": "待翻译的碱基序列:",
            "label2": "从文件中导入:",
            "label3": "翻译结果:",
            "label4": "导出路径:",
            "button1": "翻译",
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
            translation = Translation(self.str_data)
            if self.str_data != '\n' and self.str_data:
                text3.config(state=tkinter.NORMAL)
                text3.delete("1.0", "end")
                text3.insert("1.0", translation.get_protein())
                text3.config(state=tkinter.DISABLED)
                self.__draw_pie__(window, translation.get_protein())

                for c in self.str_data:
                    if c != 'A' and c != 'U' and c != 'C' and c != 'G' and c != '\n':
                        messagebox.showwarning(title="警告", message='RNA序列中存在非法字符,请检查!')
                        break
            else:
                messagebox.showwarning(title='警告', message='请先导入或输入RNA序列!')

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
                    messagebox.showwarning(title='警告', message="翻译内容为空!")
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
                if c in dict_t.keys():
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
        sizes = dict1.values()
        labels = dict1.keys()
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
    "AUGGCCAUGGCGCCCAGAACUGAGAUCAAUAGUACCCGUAUUAACGGGUGA"
    test = Frame()
