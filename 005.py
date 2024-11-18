import tkinter
from tkinter import filedialog, messagebox

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class CGContent:
    def __init__(self, dna_dict):
        self.__dna = dna_dict
        for t in self.__dna.keys():
            self.__dna[t] = self.__cal_content__(self.__dna[t])

    def __cal_content__(self, dna):
        count_c = 0
        count_g = 0
        for c in dna.strip():
            if c == 'C':
                count_c += 1
            if c == 'G':
                count_g += 1
            if c != 'C' and c != "G" and c != 'A' and c != 'T':
                messagebox.showwarning(title="警告", message='DNA序列中存在非法字符,请检查!')
                pass
        content = ((count_c + count_g) / len(dna) * 100)
        # content = "{:.2f}".format(content)
        return content

    def get_dict(self):
        return self.__dna


class Frame:
    str_data = None
    dna_dict = None
    read_path = None

    def __init__(self):
        config = {
            "geometry": "800x600+200+200",
            "font": ("Arial", 12),
            "title": "DNA中CG含量计算",
            "label1": "请输入DNA名称和内容:",
            "label2": "从文件中导入:",
            "button1": "计算",
            "button2": "浏览",
            "filename": "",
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
        text1.config(state=tkinter.DISABLED)
        text2 = tkinter.Text(window, font=config["font"], width=50, height=1.5)
        text2.place(x=230, y=100)

        def button1_click():
            self.__read_file__()
            self.str_data = text1.get("1.0", "end")
            if self.dna_dict:
                percent_dict = CGContent(self.dna_dict).get_dict()
                max_percent_name = ""
                max_percent = 0
                for t in percent_dict.keys():
                    if float(percent_dict[t]) > float(max_percent):
                        max_percent_name = t
                        max_percent = percent_dict[t]
                # print(max_percent_name, max_percent)
                d = Draw(window)
                d.draw_chart(self.dna_dict.values(), self.dna_dict.keys(), {"x": 5, "y": 4}, "CG含量", "DNA名称",
                             "CG含量", {"x": 160, "y": 150})
                messagebox.showinfo(title="统计结果",
                                    message=f"CG含量最高的DNA序列名称为:{max_percent_name},含量为:{max_percent:.2f}%")
                pass

            else:
                messagebox.showwarning(title='警告', message='请先导入或输入DNA序列!')

        tkinter.Button(window, text=config["button1"], font=config["font"], width=5, height=1,
                       command=button1_click).place(x=700, y=55)

        def button2_click():
            if self.__select_file__():
                text1.config(state=tkinter.NORMAL)
                text1.delete("1.0", "end")
                text1.insert("1.0", self.str_data)
                text1.config(state=tkinter.DISABLED)
                text2.delete("1.0", "end")
                text2.insert("1.0", self.read_path)

        tkinter.Button(window, text=config["button2"], font=config["font"], width=5, height=1,
                       command=button2_click).place(x=700, y=105)

        window.resizable(False, False)
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
        dna: dict[str, str] = {}
        tempName = ""
        tempDna = ""
        with open(self.read_path, 'r') as fh:
            lines = fh.readlines()
            for line in lines:
                if line[0] == '>':
                    tempName = line.strip('>')
                    tempDna = ""
                else:
                    tempDna += line.strip()
                    dna[tempName] = tempDna
        self.dna_dict = dna
        with open(self.read_path, 'r') as fh:
            self.str_data = fh.read()
        pass


class Draw:
    def __init__(self, master):
        self.__master = master

    def draw_chart(self, x_data, x_index, pic_size: dict[float:float] = {"x": 3, "y": 3}, title="", x_label="x",
                   y_label="y",
                   location: dict[str:float] = {"x": 400.0, "y": 250.0}):
        plt.rcParams["font.sans-serif"] = ["SimHei"]
        plt.rcParams["axes.unicode_minus"] = False
        data = x_data
        index = x_index
        fig = Figure(figsize=(pic_size["x"], pic_size["y"]), dpi=100)
        ax = fig.add_subplot(111)
        bars = ax.bar(index, data, color=['blue', 'green', 'red', 'purple', 'gray'])
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
