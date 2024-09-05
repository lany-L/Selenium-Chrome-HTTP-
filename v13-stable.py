import tkinter as tk
from tkinter import filedialog, messagebox
import os
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time


class URLCategorizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("网站分拣工具")
        self.urls = []
        self.driver = None
        self.categories = []
        self.hotkeys = {}
        self.config_file = "hotkeys_config.json"
        self.load_hotkeys()  # 加载已保存的热键设置
        self.chrome_driver_path = r'c:\chromedriver-win64\chromedriver.exe'
        self.init_gui()
        self.root.focus_set()  # 将焦点设置到根窗口
        self.pp = 0
        self.pp_1 = 0
        self.max_windows = 20
        self.root.geometry("280x500")  # 宽800像素，高600像素
        self.add_category()

    def init_gui(self):
        # 导入按钮
        self.import_btn = tk.Button(self.root, text="导入网址列表", command=self.import_urls)
        self.import_btn.pack(pady=10)

        # 输入新分类名称的输入框和按钮
        self.new_category_frame = tk.Frame(self.root)
        self.new_category_frame.pack(pady=10)

        self.new_category_entry = tk.Entry(self.new_category_frame)
        self.new_category_entry.pack(side=tk.LEFT)

        self.add_category_btn = tk.Button(self.new_category_frame, text="添加分类", command=self.add_category)
        self.add_category_btn.pack(pady=20, side=tk.LEFT)

        # 分类按钮和热键选择菜单的容器
        self.category_frame = tk.Frame(self.root)
        self.category_frame.pack(pady=10)

        # 初始化已有的分类按钮
        for category in self.categories:
            self.add_category_button(category)

        # 清除数据按钮
        self.clear_btn = tk.Button(self.root, text="清除数据", command=self.clear_data)
        self.clear_btn.pack(pady=10)

    def load_hotkeys(self):
        # 从配置文件加载热键设置
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r', encoding='utf-8') as file:
                config = json.load(file)
                self.categories = config.get("categories", [])
                self.hotkeys = config.get("hotkeys", {})

            for i in self.hotkeys.keys():
                self.bbbb(i, self.hotkeys[i])

    def save_hotkeys(self):
        # 保存当前热键设置到配置文件
        config = {
            "categories": self.categories,
            "hotkeys": self.hotkeys
        }
        with open(self.config_file, 'w', encoding='utf-8') as file:
            json.dump(config, file, ensure_ascii=False, indent=4)

    def import_urls(self):
        filepath = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if filepath:
            with open(filepath, 'r', encoding='utf-8') as file:
                for line in file.readlines():
                    url = line.strip()
                    if len(url) > 0:
                        # 自动添加前缀
                        if not url.startswith(("http://", "https://")):
                            url = "http://" + url
                        self.urls.append(url)

            self.open_urls_in_browser()


    def open_urls_in_browser(self):
        chrome_service = Service(executable_path=self.chrome_driver_path)
        chrome_options = Options()
        chrome_options.add_argument("--disable-popup-blocking")
        self.driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

        # 打开一个空白页，避免出现 data:, 的空白页
        # self.driver.get("about:blank")
        self.driver.get(self.urls[0])

        # 分批次打开网址
        if len(self.urls) < 20:
            for i in range(1, len(self.urls)):
                if len(self.urls[i]) > 0:
                    self.driver.execute_script(f"window.open('{self.urls[i]}', '_blank');")
        else:
            for i in range(1, self.max_windows):
                if len(self.urls[i]) > 0:
                    self.driver.execute_script(f"window.open('{self.urls[i]}', '_blank');")

    def save_url_and_close(self, category_filename):
        if self.driver:
            try:
                # 每次操作前获取最新的窗口句柄
                handles = self.driver.window_handles
                if handles:
                    current_window = self.driver.current_window_handle
                    if current_window in handles:
                        current_url = self.driver.current_url
                        with open(category_filename, 'a', encoding='utf-8') as file:
                            file.write(current_url + "\n")
                        # messagebox.showinfo("Success", f"URL 已保存到 {category_filename}")
                        self.pp += 1
                        self.pp_1 += 1
                        if self.pp >= len(self.urls) and len(self.driver.window_handles)==1:
                            self.driver.switch_to.window(self.driver.window_handles[-1])  # 切换到最后一个打开的标签页
                            self.driver.execute_script(f"window.open('', '_blank');")
                            self.driver.switch_to.window(self.driver.window_handles[0])  # 切换到最后一个打开的标签页
                            self.driver.close()  # 关闭当前标签页
                        else:
                            self.driver.close()  # 关闭当前标签页

                        self.driver.switch_to.window(self.driver.window_handles[-1])  # 切换到最后一个打开的标签页
                        if len(self.driver.window_handles) <= 1:

                            if self.pp < len(self.urls) and self.pp_1 >= self.max_windows-1:

                                if self.pp + self.max_windows < len(self.urls):

                                    for i in range(0, self.max_windows):
                                        if len(self.urls[i]) > 0:
                                            self.driver.execute_script(
                                                f"window.open('{self.urls[self.pp+i]}', '_blank');")

                                else:

                                    for i in range(self.pp, len(self.urls)):
                                        if len(self.urls[i]) > 0:
                                            self.driver.execute_script(
                                                f"window.open('{self.urls[i]}', '_blank');")

                                self.pp_1 = 0

                                self.driver.switch_to.window(self.driver.window_handles[-1])  # 切换到最后一个打开的标签页
                    else:
                        messagebox.showwarning("警告", "当前窗口不可用，无法保存URL")
                else:
                    messagebox.showwarning("警告", "没有更多窗口可供保存")
            except Exception as e:
                messagebox.showerror("错误", f"保存URL时出现问题: {str(e)}")

    def clear_data(self):
        for category in self.categories:
            category_filename = f"{category}.txt"
            if os.path.exists(category_filename):
                os.remove(category_filename)
        messagebox.showinfo("完成", "所有分类文本已删除")

    def save_results(self):
        messagebox.showinfo("完成", "所有分类结果已保存")

    def add_category(self):
        category = self.new_category_entry.get().strip()

        if category and category not in self.categories:
            self.categories.append(category)
            self.hotkeys[category] = None
            self.add_category_button(category)
            self.save_hotkeys()  # 保存新的分类和热键设置
            self.new_category_entry.delete(0, tk.END)  # 清空输入框
            self.root.focus_set()  # 将焦点设置到根窗口

    def add_category_button(self, category):
        frame = tk.Frame(self.category_frame)
        frame.pack(pady=5)

        btn = tk.Button(frame, text=f"{category}", command=lambda c=category: self.save_url_and_close(f"{c}.txt"))
        btn.pack(side=tk.LEFT)

        # 下拉菜单选择热键（小写字母）
        hotkey_menu = tk.StringVar(value="选择热键")
        hotkey_dropdown = tk.OptionMenu(frame, hotkey_menu, *[chr(i) for i in range(97, 123)],
                                        command=lambda key, c=category: self.bind_hotkey(c, key))
        hotkey_dropdown.pack(side=tk.LEFT)

        # 如果该分类已经绑定了热键，在界面上显示
        if self.hotkeys[category]:
            hotkey_menu.set(self.hotkeys[category])

    def bbbb(self, category, key):
        if self.hotkeys[category]:
            # 如果已经有热键绑定，先解除绑定
            self.root.unbind(f"<{self.hotkeys[category]}>")
        self.hotkeys[category] = key.lower()
        self.root.bind(f"<{self.hotkeys[category]}>", lambda event, c=category: self.save_url_and_close(f"{c}.txt"))
        self.save_hotkeys()  # 每次绑定新的热键后自动保存

    def bind_hotkey(self, category, key):
        if self.hotkeys[category]:
            # 如果已经有热键绑定，先解除绑定
            self.root.unbind(f"<{self.hotkeys[category]}>")
        self.hotkeys[category] = key.lower()
        self.root.bind(f"<{self.hotkeys[category]}>", lambda event, c=category: self.save_url_and_close(f"{c}.txt"))
        self.save_hotkeys()  # 每次绑定新的热键后自动保存
        messagebox.showinfo("热键设置", f"{category} 已绑定热键 {key.lower()}")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = URLCategorizerApp(root)
    app.run()
