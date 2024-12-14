import math
import tkinter
from tkinter import messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class BaseError(Exception):
    def __init__(self, msg):
        self._msg = msg

    def __str__(self):
        return self._msg


class RandomDNA:
    def __init__(self, dna, probabilities: list):

        self._dna: str = dna.strip().upper()
        self._probabilities: list = [float(x) for x in probabilities]
        self._result = []
        try:
            for probability in self._probabilities:
                self._result.append(self._random_dna(probability))
        except BaseError:
            pass

    def _random_dna(self, probability):
        CG_content = 0
        AT_content = 0
        C_or_G_probability = math.log10(probability / 2)
        A_or_T_probability = math.log10(1 / 2 - probability / 2)
        for base in self._dna:
            if base == 'C' or base == 'G':
                CG_content += 1
            if base == 'A' or base == 'T':
                AT_content += 1
            if base not in 'CGAT':
                raise BaseError(f"Invalid character {base} found in DNA sequence")
        return round(AT_content * A_or_T_probability + C_or_G_probability * CG_content, 3)

    @property
    def result(self):
        return self._result


class Frame:
    def __init__(self):
        self._probabilities_list = []
        self._dna = ""
        self.config = {
            "geometry": "800x600+200+200",
            "size_x": 800,
            "size_y": 600,
            "font": ("Arial", 14),
            "title": "随机DNA序列",
            "label_1": "DNA序列",
            "label_2": "从文件中选择",
            "label_3": "概率列表",
            "label_4": "从文件中选择",
            "button1": "求解",
            "button2": "浏览",
            "button3": "报表",
            "button4": "浏览",
            "tips": "提示:请用空格分割概率",
            "author": "Thank you for your use, author @ 孙伟嘉"
        }
        window = tkinter.Tk()
        window.geometry(self.config["geometry"])
        window.title(self.config["title"])
        window.resizable(False, False)

        frame_offset = 10
        frame_1_offset = (20, 16)
        frame_author = self._create_frame_(window, 800 - frame_offset, 50 - frame_offset)
        frame_author.pack(side="bottom", pady=frame_offset)
        frame_1 = self._create_frame_(window, 200 - frame_offset, 600 / 2 - frame_offset - 50)
        frame_1.pack(side="left", anchor="nw", padx=frame_offset)
        frame_2 = self._create_frame_(window, 400 - frame_offset, 600 / 2 - frame_offset - 50)
        frame_2.pack(side="left", anchor="n", padx=frame_offset)
        frame_3 = self._create_frame_(window, 200 - frame_offset, 600 / 2 - frame_offset - 50)
        frame_3.pack(side="right", anchor="ne", padx=frame_offset)

        label_author = self._create_label_(frame_author, self.config["author"], width=40, height=3)
        label_author.pack()
        label_1 = self._create_label_(frame_1, self.config["label_1"])
        label_1.pack(side="top", anchor="n", padx=frame_1_offset[0], pady=frame_1_offset[1])
        label_2 = self._create_label_(frame_1, self.config["label_2"])
        label_2.pack(side="top", anchor="n", padx=frame_1_offset[0], pady=frame_1_offset[1])
        label_3 = self._create_label_(frame_1, self.config["label_3"])
        label_3.pack(side="top", anchor="n", padx=frame_1_offset[0], pady=frame_1_offset[1])
        label_4 = self._create_label_(frame_1, self.config["label_4"])
        label_4.pack(side="top", anchor="n", padx=frame_1_offset[0], pady=frame_1_offset[1])

        text_1 = self._create_text_(frame_2, 1, 1)
        text_1.pack(side="top", fill="x", padx=0, pady=frame_1_offset[1])
        text_2 = self._create_text_(frame_2, 1, 1)
        text_2.pack(side="top", fill="x", padx=0, pady=frame_1_offset[1])
        text_3 = self._create_text_(frame_2, 1, 1)
        text_3.pack(side="top", fill="x", padx=0, pady=frame_1_offset[1])
        text_4 = self._create_text_(frame_2, 1, 1)
        text_4.pack(side="top", fill="x", padx=0, pady=frame_1_offset[1])

        text_3.insert('end', self.config["tips"])
        text_3.config(foreground='grey')

        def text_3_Handler(event):
            text_3.config(foreground='black')
            text_3.delete('1.0', 'end')

        text_3.bind("<Button-1>", text_3_Handler)

        def button_click_1():
            self._dna = text_1.get('1.0', 'end').strip()
            self._probabilities_list = [float(x) for x in text_3.get('1.0', 'end').split() if x != self.config["tips"]]
            if self._dna and self._probabilities_list:
                r = RandomDNA(self._dna, self._probabilities_list)
                # print(r.result)
                messagebox.showinfo(title="结果", message=f"对应概率为:\n{r.result}")
            else:
                messagebox.showwarning(title="警告", message="缺少DNA字段或概率列表")
            pass

        def button_click_2():
            path = self._select_file_()
            if path != 'none':
                dna_file = self._read_file_(path)
                if dna_file.strip():
                    self._dna = dna_file
                    text_2.delete('1.0', 'end')
                    text_2.insert('end', path)
                    text_1.delete('1.0', 'end')
                    text_1.insert('end', dna_file)
            pass

        def button_click_3():
            self._dna = text_1.get('1.0', 'end').strip()
            self._probabilities_list = [float(x) for x in text_3.get('1.0', 'end').split() if x != self.config["tips"]]
            if self._dna and self._probabilities_list:
                r = RandomDNA(self._dna, self._probabilities_list)
                # print(r.result)
                d = Draw(window)
                d.draw_chart(x_data=[(-1) * x for x in r.result], x_index=self._probabilities_list,
                             pic_size={"x": 7, "y": 3},
                             title="概率结果",
                             x_label="在X概率下", y_label="概率", location={"x": 60.0, "y": 250.0})
            else:
                messagebox.showwarning(title="警告", message="缺少DNA字段或概率列表")
            pass

        def button_click_4():
            path = self._select_file_()
            if path != 'none':
                probabilities_file = self._read_file_(path)
                if probabilities_file.strip():
                    text_4.delete('1.0', 'end')
                    text_4.insert('end', path)
                    text_3.config(foreground='black')
                    text_3.delete('1.0', 'end')
                    text_3.insert('end', probabilities_file)
                    self._probabilities_list = [float(x) for x in probabilities_file.split()]
            pass

        button_1 = self._create_button_(frame_3, text=self.config["button1"], width=6, height=1,
                                        button_click=button_click_1)
        button_1.pack(side="top", padx=0, pady=frame_1_offset[1] - 6)
        button_2 = self._create_button_(frame_3, text=self.config["button2"], width=6, height=1,
                                        button_click=button_click_2)
        button_2.pack(side="top", padx=0, pady=frame_1_offset[1] - 6)
        button_3 = self._create_button_(frame_3, text=self.config["button3"], width=6, height=1,
                                        button_click=button_click_3)
        button_3.pack(side="top", padx=0, pady=frame_1_offset[1] - 6)
        button_4 = self._create_button_(frame_3, text=self.config["button4"], width=6, height=1,
                                        button_click=button_click_4)
        button_4.pack(side="top", padx=0, pady=frame_1_offset[1] - 6)
        window.mainloop()

    @staticmethod
    def _create_frame_(master, width, height, propagate=False, box=False):
        frame = tkinter.Frame(master, width=width, height=height)
        frame.pack_propagate(propagate)
        if box:
            frame.config(highlightbackground="black", highlightthickness=2)
        return frame

    def _create_label_(self, master, text, width=0, height=0):
        if width == 0 and height == 0:
            return tkinter.Label(master, font=self.config["font"], text=text)
        elif width == 0:
            return tkinter.Label(master, font=self.config["font"], text=text, height=height)
        elif height == 0:
            return tkinter.Label(master, font=self.config["font"], text=text, width=width)
        else:
            return tkinter.Label(master, font=self.config["font"], text=text, width=width, height=height)

    @staticmethod
    def _create_text_(master, width=0, height=0):
        if width == 0 and height == 0:
            return tkinter.Text(master, font=("Arial", 14 + 2))
        elif width == 0:
            return tkinter.Text(master, font=("Arial", 14 + 2), height=height)
        elif height == 0:
            return tkinter.Text(master, font=("Arial", 14 + 2), width=width)
        else:
            return tkinter.Text(master, font=("Arial", 14 + 2), width=width, height=height)

    def _create_button_(self, master, text, width, height, button_click):
        return tkinter.Button(master, text=text, font=self.config["font"],
                              width=width, height=height, command=button_click)

    @staticmethod
    def _select_file_():
        file_path = filedialog.askopenfilename(title="选择文件")
        if file_path:
            return file_path
        else:
            messagebox.showwarning(title='错误', message='文件不存在!')
            return "none"

    @staticmethod
    def _read_file_(path):
        with open(path, 'r') as fh:
            return fh.read()


class Draw:
    def __init__(self, master):
        self.__master = master

    def draw_chart(self, x_data, x_index, pic_size: dict[float:float] = {"x": 7, "y": 3}, title="查找结果",
                   x_label="位点",
                   y_label="是否符合",
                   location: dict[str:float] = {"x": 60.0, "y": 250.0}):
        plt.rcParams["font.sans-serif"] = ["SimHei"]
        plt.rcParams["axes.unicode_minus"] = False
        data = x_data
        index = x_index
        fig = Figure(figsize=(pic_size["x"], pic_size["y"]), dpi=100)
        ax = fig.add_subplot(111)
        bars = ax.bar(index, data, color=['red', 'blue', 'green', 'yellow', 'pink', 'grey'])
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

    @staticmethod
    def create_bool_data(data_list: list, n, m):
        data = []
        for i in range(n):
            data.append(0)
        for i in data_list:
            for j in range(i, i + m):
                data[j - 1] = 1
        return data


if __name__ == '__main__':
    test = Frame()
