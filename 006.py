import tkinter
from tkinter import filedialog, messagebox

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class CountMutations:
    def __init__(self, dna1, dna2):
        self.__dna1: str = dna1.strip().upper()
        self.__dna2: str = dna2.strip().upper()
        self.__count_mutations = 0
        self.__mutations = []
        self.__count__()

    def __count__(self):
        if len(self.__dna1) != len(self.__dna2):
            self.__count_mutations = -1
            return
        else:
            for t1, t2 in zip(self.__dna1, self.__dna2):
                if t1 == t2:
                    self.__mutations.append(0)
                else:
                    self.__mutations.append(1)
                    self.__count_mutations += 1
            for t1 in self.__dna1:
                if t1 not in ['A', 'T', 'G', 'C']:
                    messagebox.showwarning(title="警告", message='DNA序列1中存在非法字符,计算结果可能存在问题请检查!')
                    break
            for t2 in self.__dna2:
                if t2 not in ['A', 'T', 'G', 'C']:
                    messagebox.showwarning(title="警告", message='DNA序列1中存在非法字符,计算结果可能存在问题请检查!')
                    break

    def get_count_mutations(self):
        return self.__count_mutations

    def get_mutations(self):
        return self.__mutations


class Frame:
    str_data1 = ""
    str_data2 = ""
    read_path1 = ""
    read_path2 = ""

    # read_path = None
    def __init__(self):
        config = {
            "geometry": "800x600+200+200",
            "font": ("Arial", 12),
            "title": "DNA突变点查找",
            "label1": "DNA序列1:",
            "label2": "从文件中导入:",
            "label3": "DNA序列2:",
            "label4": "从文件中导入:",
            "button1": "查找",
            "button2": "浏览",
            "button3": "报表",
            "button4": "浏览",
            "author": "Thank you for your use, author @ 孙伟嘉"
        }
        window = tkinter.Tk()
        window.geometry(config["geometry"])
        window.title(config["title"])
        tkinter.Label(window, text=config["author"], font=config["font"], width=40, height=3).pack(side="bottom")
        tkinter.Label(window, text=config["label1"], font=config["font"], width=20, height=2).place(x=65, y=50)
        tkinter.Label(window, text=config["label2"], font=config["font"], width=20, height=2).place(x=65, y=100)
        tkinter.Label(window, text=config["label3"], font=config["font"], width=20, height=2).place(x=65, y=150)
        tkinter.Label(window, text=config["label4"], font=config["font"], width=20, height=2).place(x=65, y=200)
        text1 = tkinter.Text(window, font=config["font"], width=50, height=1.5)
        text1.place(x=230, y=50)
        text2 = tkinter.Text(window, font=config["font"], width=50, height=1.5)
        text2.place(x=230, y=100)
        text3 = tkinter.Text(window, font=config["font"], width=50, height=1.5)
        text3.place(x=230, y=150)
        text4 = tkinter.Text(window, font=config["font"], width=50, height=1.5)
        text4.place(x=230, y=200)

        def button1_click():
            self.str_data1 = text1.get("1.0", "end").strip()
            self.str_data2 = text3.get("1.0", "end").strip()
            if self.str_data1 and self.str_data2:
                count_mutations = CountMutations(self.str_data1, self.str_data2)
                if count_mutations.get_count_mutations() != -1:
                    messagebox.showinfo(title="统计信息",
                                        message=f"突变个数为:{count_mutations.get_count_mutations()}个碱基。")
                else:
                    messagebox.showwarning(title='错误', message='两条DNA序列长度不等!')
            else:
                messagebox.showwarning(title='警告', message='请先导入或输入DNA序列!')

        tkinter.Button(window, text=config["button1"], font=config["font"], width=5, height=1,
                       command=button1_click).place(x=700, y=55)

        def button2_click():
            if self.__select_file_1__():
                text1.delete("1.0", "end")
                text1.insert("1.0", self.str_data1)
                text2.delete("1.0", "end")
                text2.insert("1.0", self.read_path1)

        tkinter.Button(window, text=config["button2"], font=config["font"], width=5, height=1,
                       command=button2_click).place(x=700, y=105)

        def button3_click():
            self.str_data1 = text1.get("1.0", "end").strip()
            self.str_data2 = text3.get("1.0", "end").strip()
            if self.str_data1 and self.str_data2:
                count_mutations = CountMutations(self.str_data1, self.str_data2)
                data = count_mutations.get_mutations()
                index = list(range(1, len(data) + 1))
                d = Draw(window)
                d.draw_chart(data, index, {"x": 7, "y": 3}, "突变位置图", "位置", "是否突变", {"x": 50.0, "y": 250.0})
            else:
                messagebox.showwarning(title='警告', message='请先导入或输入DNA序列!')

        tkinter.Button(window, text=config["button3"], font=config["font"], width=5, height=1,
                       command=button3_click).place(x=700, y=155)

        def button4_click():
            if self.__select_file_2__():
                text3.delete("1.0", "end")
                text3.insert("1.0", self.str_data2)
                text4.delete("1.0", "end")
                text4.insert("1.0", self.read_path2)

        tkinter.Button(window, text=config["button4"], font=config["font"], width=5, height=1,
                       command=button4_click).place(x=700, y=205)

        window.mainloop()

    def __select_file_1__(self):
        file_path = filedialog.askopenfilename(title="选择文件")
        if file_path:
            self.read_path1 = file_path
            self.__read_file_1__()
            return True
        else:
            messagebox.showwarning(title='错误', message='文件不存在!')
            return False

    def __read_file_1__(self):
        with open(self.read_path1, 'r') as fh:
            self.str_data1 = fh.read().upper()

    def __select_file_2__(self):
        file_path = filedialog.askopenfilename(title="选择文件")
        if file_path:
            self.read_path2 = file_path
            self.__read_file_2__()
            return True
        else:
            messagebox.showwarning(title='错误', message='文件不存在!')
            return False

    def __read_file_2__(self):
        with open(self.read_path2, 'r') as fh:
            self.str_data2 = fh.read().upper()


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
        if max(data) != 0:
            ax.set_ylim(0, max(data))
        else:
            ax.set_ylim(0, max(data) + 1)
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.set_title(title)
        for bar, height in zip(bars, data):
            y_val = height
            ax.text(bar.get_x() + bar.get_width() / 2 - 0.1, y_val,
                    "{:.2f}".format(y_val) + '%', ha='center', va='bottom')
        canvas = FigureCanvasTkAgg(fig, master=self.__master)
        canvas.draw()
        canvas.get_tk_widget().place(x=location["x"], y=location["y"])
        pass


if __name__ == "__main__":
    test = Frame()
