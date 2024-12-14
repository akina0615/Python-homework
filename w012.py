import tkinter
from tkinter import messagebox, filedialog, DISABLED, NORMAL, scrolledtext


class PAC:
    def __init__(self, n):
        self._pac_list = []
        self._number_list = [x for x in range(1, eval(n) + 1)]
        self._pac_list = self.generate_permutations(self._number_list)

    @staticmethod
    def generate_permutations(nums):
        def backtrack(start):
            if start == len(nums):
                result.append(nums[:])
                return
            for i in range(start, len(nums)):
                nums[start], nums[i] = nums[i], nums[start]
                backtrack(start + 1)
                nums[start], nums[i] = nums[i], nums[start]

        result = []
        backtrack(0)
        return result

    @property
    def pac_list(self):
        return self._pac_list


class Frame:
    def __init__(self):
        self._dna_dict = {}
        self._protein_dict = {}
        self.config = {
            "geometry": "800x600+200+200",
            "size_x": 800,
            "size_y": 600,
            "font": ("Arial", 14),
            "title": "排列组合",
            "label_1": "请输入数字",
            "label_2": "排列结果",
            "button1": "排列组合",
            "button2": "展开",
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

        text_1 = self._create_text_(frame_2, 1, 1)
        text_1.pack(side="top", fill="x", padx=0, pady=frame_1_offset[1])
        text_2 = self._create_text_(frame_2, 1, 1)
        text_2.pack(side="top", fill="x", padx=0, pady=frame_1_offset[1])
        text_2.configure(state=DISABLED)
        text_3 = scrolledtext.ScrolledText(window, width=70, height=5, font=self.config["font"])
        text_3.place(x=0, y=300)

        def button_click_1():
            if text_1.get('1.0', 'end').strip():
                pac = PAC(text_1.get('1.0', 'end').strip())
                text_2.configure(state=NORMAL)
                text_2.delete('1.0', 'end')
                text_2.insert('end', str(len(pac.pac_list)))
                text_2.configure(state=DISABLED)
                pass
            else:
                messagebox.showwarning(title="警告", message="请输入数值")

        def button_click_2():
            if text_1.get('1.0', 'end').strip():
                pac = PAC(text_1.get('1.0', 'end').strip())
                text_2.configure(state=NORMAL)
                text_2.delete('1.0', 'end')
                text_2.insert('end', str(len(pac.pac_list)))
                text_2.configure(state=DISABLED)

                text_3.delete('1.0', 'end')
                for item in pac.pac_list:
                    text_3.insert('end', item)
                    text_3.insert('end', '\n')
                pass
            else:
                messagebox.showwarning(title="警告", message="请输入数值")

            pass

        button_1 = self._create_button_(frame_3, text=self.config["button1"], width=6, height=1,
                                        button_click=button_click_1)
        button_1.pack(side="top", padx=0, pady=frame_1_offset[1] - 6)
        button_2 = self._create_button_(frame_3, text=self.config["button2"], width=6, height=1,
                                        button_click=button_click_2)
        button_2.pack(side="top", padx=0, pady=frame_1_offset[1] - 6)

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

    def _read_file_(self, path):
        dna: dict[str, str] = {}
        tempName = ""
        tempDna = ""
        with open(path, 'r') as fh:
            lines = fh.readlines()
            for line in lines:
                if line[0] == '>':
                    tempName = line.strip('>')
                    tempDna = ""
                else:
                    tempDna += line.strip()
                    dna[tempName] = tempDna.upper()
        self._dna_dict = dna
        with open(path, 'r') as fh:
            str_data = fh.read()
        return str_data


if __name__ == '__main__':
    test = Frame()
