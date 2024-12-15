import tkinter
from threading import Thread
from tkinter import scrolledtext

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

        label_author = self._create_label_(self._window, self._author, font=("Arial", 12))
        label_author.pack(side='bottom')

        read_me = scrolledtext.ScrolledText(self._window, width=400, height=400, font=('Arial', 16), wrap=tkinter.WORD)
        read_me.pack(side='top', fill='both', expand=True)
        initial_text = "感谢您使用本应用。请按需选择菜单上的对应功能！"
        read_me.config(foreground='grey')
        read_me.insert(tkinter.END, initial_text)

        def read_me_key_Handler(event):
            read_me.config(foreground='black')
            read_me.delete('1.0', 'end')
            read_me.unbind("<Key>")

        read_me.bind("<Key>", read_me_key_Handler)

        def on_copy(event=None):
            try:
                selected_text = read_me.get(tkinter.SEL_FIRST, tkinter.SEL_LAST)
                self._window.clipboard_clear()
                self._window.clipboard_append(selected_text)
            except tkinter.TclError:
                print("没有选中文本！")

        def on_paste(event=None):
            try:
                clipboard_text = self._window.clipboard_get()
                read_me.insert(tkinter.INSERT, clipboard_text)
            except tkinter.TclError:
                print("剪贴板没有文本内容！")

        def on_delete(event=None):
            try:
                read_me.delete(tkinter.SEL_FIRST, tkinter.SEL_LAST)
                print("删除选中文本")
            except tkinter.TclError:
                print("没有选中文本可以删除！")

        context_menu = tkinter.Menu(self._window, tearoff=0)
        context_menu.add_command(label="复制", command=on_copy)
        context_menu.add_command(label="粘贴", command=on_paste)
        context_menu.add_command(label="删除", command=on_delete)

        def read_me_click_Handler(event):
            context_menu.post(event.x_root, event.y_root)
            pass

        read_me.bind("<Button-3>", read_me_click_Handler)


if __name__ == '__main__':
    c = ControlWindow()
