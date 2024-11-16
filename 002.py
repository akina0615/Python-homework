import time
import tkinter
from tkinter import filedialog, messagebox

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class Transcription:
    str_data = None
    read_path = None
    save_path = None

    def __init__(self):
        self.__create_frame__()

    def __replace__(self):
        return self.str_data.replace('T', 'U')

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

    def __create_frame__(self):
        config = {
            "geometry": "800x600+200+200",
            "font": ("Arial", 12),
            "title": "DNA转录",
            "label1": "待转录的碱基序列:",
            "label2": "从文件中导入:",
            "label3": "转录结果:",
            "label4": "导出路径:",
            "button1": "转录",
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
            if self.str_data != '\n' and self.str_data:
                text3.config(state=tkinter.NORMAL)
                text3.delete("1.0", "end")
                text3.insert("1.0", self.__replace__())
                text3.config(state=tkinter.DISABLED)

                position_list = []
                for i in range(0, len(self.str_data) - 1):
                    if self.str_data[i] == 'T':
                        position_list.append(1)
                    else:
                        position_list.append(0)
                self.__display_chart__(window, position_list)

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
                    messagebox.showwarning(title='警告', message="转录内容为空!")
            else:
                messagebox.showwarning(title='错误', message='文件不存在!')

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

    def __display_chart__(self, master, list1):
        plt.rcParams["font.sans-serif"] = ["SimHei"]
        plt.rcParams["axes.unicode_minus"] = False
        fig = Figure(figsize=(7, 3), dpi=100)
        ax = fig.add_subplot(111)
        bars = ax.bar(list(range(1, len(list1) + 1)), list1, color=['red'])
        ax.set_ylim(0, 1)
        ax.set_xlabel('位置')
        ax.set_ylabel("1为转录点位")
        ax.set_title('DNA转录位点统计')
        for bar, height in zip(bars, list1):
            y_val = height
            ax.text(bar.get_x() + bar.get_width() / 2 - 0.1, y_val,
                    str(y_val), ha='center', va='bottom')
        canvas = FigureCanvasTkAgg(fig, master=master)
        canvas.draw()
        canvas.get_tk_widget().place(x=60, y=250)


if __name__ == "__main__":
    test = Transcription()
