import os
import time

import pyperclip
import keyboard

from PIL import ImageGrab
from win11toast import toast


class SaveClipboardPicToFile(object):
    def __init__(self, img_folder):
        self.img_folder = img_folder
        self.img = None
        self.img_name = ""
        
    def _createImgObject(self):
        self.img = ImageGrab.grabclipboard()

    def chdirToWorkdir(self):
        os.chdir(self.img_folder)

    def _createFileName(self):
        """
        生成一个图片的文件名，命名方式为：年月日小时分钟秒.png
        """
        self.img_name = time.strftime("%Y%m%d%H%M%S.png", time.localtime())

    def _saveToFile(self):
        """
        保存图片的操作，要检测剪贴板里是图片，否则会报错
        """
        try:
            self.img.save(self.img_name, "png")
        except AttributeError:
            print("必须是一个截图存在剪贴板")

    def getMarkdownCode(self):
        """
        返回一个markdown格式的图片路径给剪贴板
        """
        pyperclip.copy("![[%s]]" % self.img_name)

    def toastNotification(self):
        """
        给windows系统发送一个右下脚的通知
        """
        toast("已复制", "已保存图片文件，请按ctrl+v粘贴Markdown")

    def save2file(self):
        self._createFileName()
        self._createImgObject()
        self._saveToFile()

def on_hotkey():
    img_folder = "D:\\MyFiles\\Obsidian\\ZoteroMetadata\\Items\\attachments"  # 存放图片的文件夹位置
    img = SaveClipboardPicToFile(img_folder)
    img.chdirToWorkdir()
    img.save2file()
    img.getMarkdownCode()
    img.toastNotification()
    # print("已保存图片文件，请按ctrl+v粘贴Markdown")


if __name__=="__main__":
    keyboard.add_hotkey("ctrl+shift+y", on_hotkey)  # 自定义一个快捷键
    print("开始执行监听键盘操作（快捷键ctrl+ship+y）：")

    while True:
        keyboard.wait()  # 监听事件

        
