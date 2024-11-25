import tkinter
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class FindMotif:
    def __init__(self, dna: str, motif: str):
        self._dna = dna.upper().strip()
        self._motif = motif.upper().strip()
        self._pos: list[int] = []
        self._find_motif_()

    def _find_motif_(self):
        dna_len = len(self._dna)
        motif_len = len(self._motif)
        for i in range(dna_len):
            if self._dna[i] == self._motif[0]:
                temp = self._dna[i:i + motif_len]
                if temp == self._motif:
                    self._pos.append(i + 1)

    @property
    def pos(self):
        return self._pos


class Frame:
    def __init__(self):
        self.config = {
            "geometry": "800x600+200+200",
            "size_x": 800,
            "size_y": 600,
            "font": ("Arial", 14),
            "title": "查找DNA中的Motif",
            "label_1": "DNA序列",
            "label_2": "从文件中选择",
            "label_3": "motif序列",
            "label_4": "从文件中选择",
            "button1": "查找",
            "button2": "浏览",
            "button3": "报表",
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
            pass

        def button_click_2():
            pass

        def button_click_3():
            pass

        def button_click_4():
            pass

        button_1 = self._create_button_(frame_3, text=self.config["button1"], width=6, height=1,
                                        button_click=button_click_1())
        button_1.pack(side="top", padx=0, pady=frame_1_offset[1]-6)
        button_2 = self._create_button_(frame_3, text=self.config["button2"], width=6, height=1,
                                        button_click=button_click_2())
        button_2.pack(side="top", padx=0, pady=frame_1_offset[1]-6)
        button_3 = self._create_button_(frame_3, text=self.config["button3"], width=6, height=1,
                                        button_click=button_click_3())
        button_3.pack(side="top", padx=0, pady=frame_1_offset[1]-6)
        button_4 = self._create_button_(frame_3, text=self.config["button4"], width=6, height=1,
                                        button_click=button_click_4())
        button_4.pack(side="top", padx=0, pady=frame_1_offset[1]-6)

        window.mainloop()

    @staticmethod
    def _create_frame_(master, width, height, propagate=0, box=False):
        frame = tkinter.Frame(master, width=width, height=height)
        frame.pack_propagate(propagate)
        if not box:
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


if __name__ == '__main__':
    test = Frame()
