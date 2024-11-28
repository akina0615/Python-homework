import tkinter
from tkinter import messagebox, filedialog


class ConsistentSequence:
    def __init__(self, dna_dict: dict[str:str]):
        self._dna_dict = dna_dict
        self._values_length = []
        self._profile = {'A': [], 'C': [], 'G': [], 'T': []}
        self._consistent_sequence = ""
        self._consistent_sequence_()

    def _consistent_sequence_(self):
        for dna in list(self._dna_dict.values()):
            self._values_length.append(len(dna))
        for value in self._values_length:
            if value != self._values_length[0]:
                messagebox.showwarning(title="警告", message="DNA序列长度不相同")
                return
        for i in range(self._values_length[0]):
            self._profile['A'].append(0)
            self._profile['C'].append(0)
            self._profile['G'].append(0)
            self._profile['T'].append(0)
        for line in list(self._dna_dict.values()):
            for i in range(len(line)):
                if line[i] == 'A' or line[i] == 'C' or line[i] == 'G' or line[i] == 'T':
                    self._profile[line[i]][i] += 1
        for i in range(self._values_length[0]):
            temp_list = [self._profile['A'][i], self._profile['C'][i], self._profile['G'][i], self._profile['T'][i]]
            if max(temp_list) == self._profile['A'][i]:
                self._consistent_sequence += 'A'
            elif max(temp_list) == self._profile['C'][i]:
                self._consistent_sequence += 'C'
            elif max(temp_list) == self._profile['G'][i]:
                self._consistent_sequence += 'G'
            elif max(temp_list) == self._profile['T'][i]:
                self._consistent_sequence += 'T'
        pass

    @property
    def profile(self):
        return self._profile

    @property
    def consistentSequence(self):
        return self._consistent_sequence


class Frame:
    def __init__(self):
        self._dna_dict = {}
        self.config = {
            "geometry": "800x600+200+200",
            "size_x": 800,
            "size_y": 600,
            "font": ("Arial", 14),
            "title": "查找DNA的一致性序列",
            "label_1": "DNA序列",
            "label_2": "从文件中选择",
            "button1": "生成",
            "button2": "浏览",
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

        def button_click_1():
            if text_1.get('1.0', 'end').strip():
                consistent_sequence = ConsistentSequence(self._dna_dict)
                profile = consistent_sequence.profile
                consistentSequence = consistent_sequence.consistentSequence
                answer = ""
                for key in profile.keys():
                    answer = answer + f"{key}: {profile[key]}\n"
                messagebox.showinfo(title="计算结果",
                                    message=f"profile矩阵为:\n{answer}一致性序列为{consistentSequence}")
                # 目前采取这种方式展示结果,以后可能会改进结果显示
                pass
            else:
                messagebox.showwarning(title="警告", message="DNA序列为空")

        def button_click_2():
            path = self._select_file_()
            if path != "none":
                text_2.delete('1.0', 'end')
                text_2.insert('end', path)
                text = self._read_file_(path)
                text_1.delete('1.0', 'end')
                text_1.insert('end', text)
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
