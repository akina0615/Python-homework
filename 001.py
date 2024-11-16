import tkinter
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class CountDna:
    str_data = None
    count_dict = {'A': 0, 'T': 0, 'C': 0, 'G': 0, 'other': 0}
    path = None

    def __init__(self):
        self.__create_frame__()

    def __count_dna__(self, str_input):
        self.str_data = str_input
        self.__count__()

    def __count__(self):
        for char in self.str_data.upper():
            if char == 'A':
                self.count_dict['A'] += 1
            elif char == 'T':
                self.count_dict['T'] += 1
            elif char == 'C':
                self.count_dict['C'] += 1
            elif char == 'G':
                self.count_dict['G'] += 1
            else:
                if char != '\n':
                    self.count_dict['other'] += 1

    def __select_file__(self):
        file_path = filedialog.askopenfilename(title="选择文件")
        if file_path:
            self.path = file_path
            self.__read_file__()
            return True
        else:
            messagebox.showwarning(title='错误', message='文件不存在!')
            return False

    def __read_file__(self):
        with open(self.path, 'r') as fh:
            self.str_data = fh.read()

    def __create_frame__(self):
        config = {
            "geometry": "800x600+200+200",
            "font": ("Arial", 12),
            "title": "DNA碱基个数统计",
            "label1": "待统计的碱基序列:",
            "label2": "从文件中导入:",
            "button1": "浏览",
            "button2": "统计",
            "author": "Thank you for your use, author @ 孙伟嘉"
        }
        window = tkinter.Tk()
        window.geometry(config["geometry"])
        window.title(config["title"])
        tkinter.Label(window, text=config["author"], font=config["font"], width=40, height=3).pack(side="bottom")
        tkinter.Label(window, text=config["label1"], font=config["font"], width=20, height=2).place(x=50, y=50)
        tkinter.Label(window, text=config["label2"], font=config["font"], width=20, height=2).place(x=65, y=100)
        text1 = tkinter.Text(window, font=config["font"], width=50, height=1.5)
        text1.place(x=230, y=50)
        text2 = tkinter.Text(window, font=config["font"], width=50, height=1.5)
        text2.place(x=230, y=100)

        def button1_click():
            if self.__select_file__():
                text1.delete("1.0", "end")
                text1.insert("1.0", self.str_data)
                text2.delete("1.0", "end")
                text2.insert("1.0", self.path)

        tkinter.Button(window, text=config["button1"], font=config["font"], width=5, height=1,
                       command=button1_click).place(x=700, y=105)

        def button2_click():
            self.str_data = text1.get("1.0", "end")
            self.count_dict = {'A': 0, 'T': 0, 'C': 0, 'G': 0, 'other': 0}
            if self.str_data != '\n' and self.str_data:
                self.__count_dna__(self.str_data)
                self.__display_chart__(window)
                # print(self.count_dict)
            else:
                messagebox.showwarning(title='警告', message='请先导入或输入DNA序列!')

        tkinter.Button(window, text=config["button2"], font=config["font"], width=5, height=1,
                       command=button2_click).place(x=700, y=55)

        window.mainloop()

    def __display_chart__(self, master):
        plt.rcParams["font.sans-serif"] = ["SimHei"]
        plt.rcParams["axes.unicode_minus"] = False
        data = self.count_dict.values()
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        bars = ax.bar(self.count_dict.keys(), data, color=['blue', 'green', 'red', 'purple', 'gray'])
        ax.set_ylim(0, max(data)+1)
        ax.set_xlabel('碱基类型')
        ax.set_ylabel('数量')
        ax.set_title('DNA碱基统计')
        for bar, height in zip(bars, data):
            y_val = height
            ax.text(bar.get_x() + bar.get_width() / 2 - 0.1, y_val,
                    str(y_val), ha='center', va='bottom')
        canvas = FigureCanvasTkAgg(fig, master=master)
        canvas.draw()
        canvas.get_tk_widget().place(x=160, y=150)


if __name__ == "__main__":
    test = CountDna()
