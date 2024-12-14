import time
import tkinter
from tkinter import messagebox, filedialog


class ORFTranslate:
    def __init__(self, dna_1):
        table = """TTT F      CTT L      ATT I      GTT V
        TTC F      CTC L      ATC I      GTC V
        TTA L      CTA L      ATA I      GTA V
        TTG L      CTG L      ATG M      GTG V
        TCT S      CCT P      ACT T      GCT A
        TCC S      CCC P      ACC T      GCC A
        TCA S      CCA P      ACA T      GCA A
        TCG S      CCG P      ACG T      GCG A
        TAT Y      CAT H      AAT N      GAT D
        TAC Y      CAC H      AAC N      GAC D
        TAA Stop   CAA Q      AAA K      GAA E
        TAG Stop   CAG Q      AAG K      GAG E
        TGT C      CGT R      AGT S      GGT G
        TGC C      CGC R      AGC S      GGC G
        TGA Stop   CGA R      AGA R      GGA G
        TGG W      CGG R      AGG R      GGG G"""
        self._table = dict(zip(table.split()[::2], table.split()[1::2]))
        self._dna_1 = dna_1
        self._dna_2 = self._reverse_complement_()
        self._translate_results = []
        self._ort_()

    def _reverse_complement_(self):
        temp = ""
        basepair = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}
        for c in self._dna_1:
            temp = basepair[c] + temp
        return temp

    def _translate_(self, dna):
        temp = ''
        begin = False
        end = False
        for i in range(0, len(dna), 3):
            codon = dna[i:i + 3]
            if len(codon) < 3:
                continue
            if codon == 'ATG':
                begin = True
            if begin:
                if codon not in self._table:
                    continue
                if self._table[codon] == 'Stop':
                    end = True
                    break
                temp += self._table[dna[i:i + 3]]
        if not end:
            return
        return temp

    def _ort_(self):
        self._translate_results.append(self._translate_(self._dna_1[0:]))
        self._translate_results.append(self._translate_(self._dna_1[1:]))
        self._translate_results.append(self._translate_(self._dna_1[2:]))
        self._translate_results.append(self._translate_(self._dna_2[0:]))
        self._translate_results.append(self._translate_(self._dna_2[1:]))
        self._translate_results.append(self._translate_(self._dna_2[2:]))
        for result in self._translate_results:
            if result is not None:
                for pos in range(len(result)):
                    if result[pos] == 'M' and pos != 0:
                        self._translate_results.append(result[pos:])
        self._translate_results = list(filter(None, set(self._translate_results)))
        # self._translate_results = [t for t in set(self._translate_results) if t]

    @property
    def translate_results(self):
        return self._translate_results


class Frame:
    def __init__(self):
        self._dna_dict = {}
        self._protein_dict = {}
        self.config = {
            "geometry": "800x600+200+200",
            "size_x": 800,
            "size_y": 600,
            "font": ("Arial", 14),
            "title": "六框翻译DNA",
            "label_1": "DNA序列",
            "label_2": "从文件中选择",
            "label_3": "蛋白质序列",
            "label_4": "导出路径",
            "button1": "翻译",
            "button2": "浏览",
            "button3": "导出",
            "button4": "浏览",
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

        def button_click_1():
            if text_1.get('1.0', 'end').strip():
                if not text_2.get('1.0', 'end').strip():
                    sequences = text_1.get('1.0', 'end').strip().split('>')
                    for seq in sequences:
                        if seq:
                            lines = seq.splitlines()
                            header = lines[0]
                            sequence = ''.join(lines[1:])
                            self._dna_dict[header] = sequence
                    pass
                for key in self._dna_dict.keys():
                    orf = ORFTranslate(self._dna_dict[key])
                    self._protein_dict[key] = orf.translate_results
                for key in self._protein_dict.keys():
                    text_3.insert(tkinter.END, '>' + key + '\n')
                    for item in self._protein_dict[key]:
                        text_3.insert(tkinter.END, item + '\n')

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

        def button_click_3():
            if text_3.get('1.0', 'end').strip():
                if text_4.get('1.0', 'end').strip():
                    path = text_4.get('1.0', 'end').strip()
                    filename = path + '/' + time.strftime("%Y-%m-%d %H°%M'%S''.txt", time.localtime())
                    with open(filename, 'w') as fh:
                        fh.write(text_3.get("1.0", "end"))
                        messagebox.showinfo(title="提示", message="导出成功")

                else:
                    messagebox.showwarning(title="警告", message="路径为空")
            else:
                messagebox.showwarning(title="警告", message="翻译内容不存在")
            pass

        def button_click_4():
            save_path = filedialog.askdirectory(title="导出文件")
            if save_path:
                text_4.delete("1.0", "end")
                text_4.insert("1.0", save_path)
            else:
                messagebox.showwarning(title='错误', message='文件不存在!')
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
