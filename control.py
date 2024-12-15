import tkinter
from threading import Thread

import w001, w002, w003, w004, w005, w006, w007, w008, w009, w010, w011, w012, w013


class Frame:
    def __init__(self):
        self._window = tkinter.Tk()

    @staticmethod
    def _create_frame_(master, width, height, propagate=False, box=False):
        frame = tkinter.Frame(master, width=width, height=height)
        frame.pack_propagate(propagate)
        if box:
            frame.config(highlightbackground="black", highlightthickness=2)
        return frame

    @staticmethod
    def _create_label_(master, text, font: tuple = ("Arial", 14), width=0, height=0):
        if width == 0 and height == 0:
            return tkinter.Label(master, font=font, text=text)
        elif width == 0:
            return tkinter.Label(master, font=font, text=text, height=height)
        elif height == 0:
            return tkinter.Label(master, font=font, text=text, width=width)
        else:
            return tkinter.Label(master, font=font, text=text, width=width, height=height)

    @staticmethod
    def _create_text_(master, font: tuple = ("Arial", 14), width=0, height=0):
        if width == 0 and height == 0:
            return tkinter.Text(master, font=font)
        elif width == 0:
            return tkinter.Text(master, font=font, height=height)
        elif height == 0:
            return tkinter.Text(master, font=font, width=width)
        else:
            return tkinter.Text(master, font=font, width=width, height=height)

    @staticmethod
    def _create_button_(master, text, width, height, font: tuple = ("Arial", 14), button_click=None):
        return tkinter.Button(master, text=text, font=font,
                              width=width, height=height, command=button_click)

    @staticmethod
    def _create_menu_(master, font: tuple = ("Arial", 14), tearoff=False):
        return tkinter.Menu(master, font=font, tearoff=tearoff)


class ControlWindow(Frame):
    def __init__(self, config_path: str = None):
        super().__init__()
        if not config_path:
            self._x = 800
            self._y = 600
            self._x_offset = 190
            self._y_offset = 190
            self._geometry = f"{self._x}x{self._y}+{self._x_offset}+{self._y_offset}"
            self._font = ("Arial", 14)
            self._title = "Python大作业"
            self._author = "Thank you for your use, author @ 孙伟嘉"
        else:
            with open(config_path, 'r') as config_file:
                read_file: str = config_file.readline()
                # 留下一个从文件中读取配置的接口
                pass
        self._window.geometry(self._geometry)
        self._window.resizable(False, False)
        self._window.title(self._title)
        self._init_GUI_()
        self._window.mainloop()

    @staticmethod
    def _create_thread(target_class):
        t = Thread(target=lambda: target_class(), name=target_class.__name__)
        t.start()

    def _init_GUI_(self):
        menu_list = [
            ('碱基统计', w001.CountDna),
            ('中心法则：转录', w002.Transcription),
            ('中心法则：翻译', w003.Frame),
            ('求DNA的反向互补序列', w004.Frame),
            ('GC含量计算', w005.Frame),
            ('计算点突变数', w006.Frame),
            ('兔子问题和递推', w007.Frame),
            ('008 孟德尔第一定律', w008.Frame),
            ('查找DNA中的motif', w009.Frame),
            ('DNA一致性序列计算', w010.Frame),
            ('DNA六框翻译', w011.Frame),
            ('排列组合', w012.Frame),
            ('随机DNA序列', w013.Frame)
        ]
        menu1 = super()._create_menu_(self._window, font=("Arial", 20), tearoff=False)

        for label, module in menu_list:
            menu1.add_command(label=label, command=lambda m=module: self._create_thread(m))

        self._window.config(menu=menu1, padx=10, pady=10)


if __name__ == '__main__':
    c = ControlWindow()
