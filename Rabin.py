import tkinter as tk
from tkinter import scrolledtext, messagebox
from rabin_lib import (
    miyao, JiaMi, JieMi, 

    add_random_letter_to_string,   
    string_to_unicode_with_tuple,
    filter_decrypt_combinations,
    get_reduced_alphabet,
    remove_letters_from_string,

    add_sequence_and_checksum_to_string,
    split_encoding,
    combine_and_verify,

    add_timestamp_to_unicode,
    verify_and_extract_characters
)
import string

class CryptoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Rabin加密解密工具")
        self.root.geometry("700x650")
        self.root.rowconfigure(0, weight=1)  # 配置主窗口的唯一一行
        self.root.columnconfigure(0, weight=1)  # 配置主窗口的唯一一列

        # 初始化商列表
        self.shang = []
        # 初始化加密数据存储
        self.encrypted_data = {}
        
        # 设置GUI布局
        self.setup_gui()

    def setup_gui(self):

        # 创建一个主框架，填充整个窗口
        main_frame = tk.Frame(self.root)
        main_frame.grid(row=0, column=0, sticky='nsew')
        main_frame.rowconfigure(0, weight=0)  # 模式选择框
        main_frame.rowconfigure(1, weight=0)  # 输入框
        main_frame.rowconfigure(2, weight=1)  # 显示框
        main_frame.rowconfigure(3, weight=0)  # 按钮框
        main_frame.columnconfigure(0, weight=1)  # 仅有一列

        # 标签方式选择
        mode_frame = tk.Frame(main_frame)
        mode_frame.grid(row=0, column=0, padx=10, pady=10, sticky='ew')
        mode_frame.columnconfigure(1, weight=1)  # 让下拉菜单扩展

        mode_label = tk.Label(mode_frame, text="选择标签方式：")
        mode_label.grid(row=0, column=0, padx=5,pady=5,sticky='w')

        self.mode_var = tk.StringVar(value='方式一（随机字母）')
        mode_options = ['方式一（随机字母）', '方式二（序列号和校验和）','方式三（时间戳）']
        mode_dropdown = tk.OptionMenu(mode_frame, self.mode_var, *mode_options)
        mode_dropdown.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        # 字母范围选择（仅适用于方式一）
        self.range_frame = tk.Frame(mode_frame)
        self.range_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky='ew')
        self.range_frame.columnconfigure(1, weight=1)
        self.range_frame.columnconfigure(3, weight=1)


        start_label = tk.Label(self.range_frame, text="起始字母：")
        start_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')

        self.letter_start = tk.StringVar(value='a')
        start_dropdown = tk.OptionMenu(self.range_frame, self.letter_start, *string.ascii_lowercase)
        start_dropdown.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        end_label = tk.Label(self.range_frame, text="结束字母：")
        end_label.grid(row=0, column=2, padx=5, pady=5, sticky='w')

        self.letter_end = tk.StringVar(value='f')
        end_dropdown = tk.OptionMenu(self.range_frame, self.letter_end, *string.ascii_lowercase)
        end_dropdown.grid(row=0, column=3, padx=5, pady=5, sticky='ew')

        # 将 range_frame 放置在 mode_frame 的下一行（row=1）
        self.range_frame.grid(row=1, column=0, columnspan=2, pady=10, sticky='w')

       # 绑定模式变化事件
        self.mode_var.trace_add('write', self.update_range_frame_visibility)

        # 初始化时根据当前模式设置range_frame的可见性
        self.update_range_frame_visibility()

        # 输入框
        entry_frame = tk.Frame(main_frame)
        entry_frame.grid(row=1, column=0, padx=10, pady=5, sticky='ew')
        entry_frame.columnconfigure(1, weight=1)

        entry_label = tk.Label(entry_frame, text="请输入一段字符串：")
        entry_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')

        self.entry = tk.Entry(entry_frame, width=80)
        self.entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        # 显示框
        self.result_box = scrolledtext.ScrolledText(main_frame, width=100, height=30, wrap=tk.WORD)
        self.result_box.grid(row=2, column=0, padx=10, pady=10, sticky='nsew')
        self.result_box.configure(state='normal')


        # 按钮框
        button_frame = tk.Frame(main_frame)
        button_frame.grid(row=3, column=0, padx=10, pady=10, sticky='ew')
        button_frame.columnconfigure((0,1,2), weight=1)  # 让三个按钮均分空间

        # 加密按钮
        encrypt_button = tk.Button(button_frame, text="加密", command=self.on_encrypt)
        encrypt_button.grid(row=0, column=0, padx=5, pady=5, sticky='ew')

        # 解密按钮
        decrypt_button = tk.Button(button_frame, text="解密", command=self.on_decrypt)
        decrypt_button.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        # 清空按钮
        clear_button = tk.Button(button_frame, text="清空",command=self.clear)
        clear_button.grid(row=0, column=2, padx=5, pady=5, sticky='ew')

        # 添加程序说明按钮
        info_button = tk.Button(main_frame, text="程序说明", command=self.show_info)
        info_button.grid(row=4, column=0, padx=10, pady=10, sticky='ew')

    def show_info(self):
        # 弹出说明对话框
        messagebox.showinfo("程序说明", """
        这是一个Rabin加密解密工具，您可以选择不同的标签方式进行字符串的加密与解密：   
                                        
        方式一：通过添加随机字母进行加密。
                实现方式：随机取26个小写英文字母中的一个，转化为Unicode编码，并固定格式为4为，比如“a",转化为“0097”，并缀在每个字符的Unicode编码后面，解密的时候取后四位并转化为字符，判断是否在勾选的字母范围内
                            
        方式二：通过序列号和校验和进行加密。
                实现方式：按顺序从0开始为每个字符进行编号，且格式为0000，即最大输入编号为9999，该编号与输入字符转化为的Unicode编码进行哈希运算，取哈希值的后四位作为校验码，并只对输入的字符Unicode码进行加密解密，最后按顺序来与每个字符解密得到的四种结果进行哈希运算，与正确的哈希值后四位进行比对
                            
        方式三：通过时间戳进行加密。
                实现方式：为每个字符后缀添加时间戳（精确到年月日时分，一共12位），并将时间戳剥离保存作为后续比对标准，对每个字符的整体（Unicode码值+时间戳）进行加密解密，最后比对结果中的时间戳即可   

        作者：倪硕                                    
        """)


    def update_range_frame_visibility(self, *args):
        if self.mode_var.get() == '方式一（随机字母）':
            self.range_frame.grid()
        else:
            self.range_frame.grid_remove()


    def clear(self):
        self.entry.delete(0, tk.END)  # 清空输入框
        self.result_box.delete(1.0, tk.END)  # 清空显示框
        self.encrypted_data = {}  # 清空加密数据

    def on_encrypt(self):
        input_text = self.entry.get().strip()  # 获取输入框的内容并去除前后空格

        if not input_text:
            messagebox.showwarning("输入错误", "请输入一段字符串进行加密。")
            return

        mode = self.mode_var.get()
        self.result_box.insert(tk.END, "=== 加密过程 ===\n\n")

        # 每次加密时生成新的 p 和 q
        p, q = miyao()
        n = p * q
        self.result_box.insert(tk.END, f"生成的密钥 p 和 q：{p}, {q}\n\n")

        if mode == '方式一（随机字母）':
            # 获取字母范围
            start = self.letter_start.get()
            end = self.letter_end.get()

            if start > end:
                messagebox.showwarning("范围错误", "起始字母不能大于结束字母。")
                return

            letter_range = get_reduced_alphabet(start, end)

            # 增加随机字母标签
            encoded_string = add_random_letter_to_string(input_text, letter_range)
            self.result_box.insert(tk.END, f"处理后的字符串（每个字符后附加一个随机字母）：{encoded_string}\n\n")  

            # 转换为Unicode整数列表
            unicode_ints = string_to_unicode_with_tuple(encoded_string)
            self.result_box.insert(tk.END, f"处理后字符串对应的Unicode码值（整型）：{unicode_ints}\n\n")

            # 执行加密
            miwen, shang = JiaMi(unicode_ints, p, q)
            self.result_box.insert(tk.END, f"加密后的密文Unicode码值：{miwen}\n\n")
            self.encrypted_data['方式一'] = {'miwen': miwen, 'shang': shang, 'p': p, 'q': q}

        elif mode == '方式二（序列号和校验和）':
            # 添加序列号和校验和标签
            encoded_string = add_sequence_and_checksum_to_string(input_text)
            self.result_box.insert(tk.END, f"处理后的字符串（每个字符前添加序列号和校验和）：{encoded_string}\n\n")  

            prefixes, char_codes = split_encoding(encoded_string)
            self.result_box.insert(tk.END, f"序列号和校验和部分：{prefixes}\n")
            self.result_box.insert(tk.END, f"字符Unicode码值部分：{char_codes}\n\n")

            # 执行加密
            miwen, shang = JiaMi(char_codes, p, q)
            self.result_box.insert(tk.END, f"加密后的密文Unicode码值：{miwen}\n\n")
            self.encrypted_data['方式二'] = {'miwen': miwen, 'shang': shang, 'prefixes': prefixes, 'p': p, 'q': q}
        
        elif mode == '方式三（时间戳）':

            # 为每个Unicode编码添加时间戳
            unicode_with_timestamps, timestamps = add_timestamp_to_unicode(input_text)
            self.result_box.insert(tk.END, f"带有时间戳的Unicode编码（整型）：{unicode_with_timestamps}\n\n")
            self.result_box.insert(tk.END, f"每个字符对应的时间戳：{timestamps}\n\n")

            # 执行加密
            miwen, shang = JiaMi(unicode_with_timestamps, p, q)
            self.result_box.insert(tk.END, f"加密后的密文Unicode码值：{miwen}\n\n")
        
        # 存储加密数据
            self.encrypted_data['方式三'] = {'p': p,'q': q,'miwen': miwen,'shang': shang,'timestamps': timestamps  # 存储每个字符的时间戳
                                          }
        else:
            messagebox.showwarning("模式错误", "未选择有效的标签方式。")
            return

    def on_decrypt(self):
        input_text = self.entry.get().strip()  # 获取输入框的内容并去除前后空格

        if not input_text:
            messagebox.showwarning("输入错误", "请输入一段字符串进行加密。")
            return
        
        mode = self.mode_var.get()

        if mode == '方式一（随机字母）':
            data = self.encrypted_data.get('方式一')
            if not data:
                messagebox.showwarning("解密错误", "未找到加密数据，请先进行加密操作。")
                return
            miwen = data['miwen']
            shang = data['shang']
            p = data['p']
            q = data['q']
        
            # 执行解密
            decrypted_chars = JieMi(miwen, p, q, shang)
            # 获取字母范围
            start = self.letter_start.get()
            end = self.letter_end.get()

            if start > end:
                messagebox.showwarning("范围错误", "起始字母不能大于结束字母。")
                return

            letter_range = get_reduced_alphabet(start, end)

            # 筛选符合条件的解组合
            valid_combinations = filter_decrypt_combinations(decrypted_chars, letter_range)

            # 移除字母后缀
            cleaned_combinations = [remove_letters_from_string(s) for s in valid_combinations]

            # 输出解密结果
            self.result_box.insert(tk.END, "=== 解密结果 ===\n\n")
            self.result_box.insert(tk.END, f"使用的密钥 p 和 q：{p}, {q}\n\n")
            self.result_box.insert(tk.END, f"解密得到的所有解：{decrypted_chars}\n\n")

            if valid_combinations:
                self.result_box.insert(tk.END, f"符合条件的解组合：{', '.join(valid_combinations)}\n\n")
                self.result_box.insert(tk.END, f"解密后的字符串（不带字母后缀）：{', '.join(cleaned_combinations)}\n\n")
            else:
                self.result_box.insert(tk.END, "没有符合条件的解组合。\n\n")

        elif mode == '方式二（序列号和校验和）':
                
            data = self.encrypted_data.get('方式二')
            if not data:
                messagebox.showwarning("解密错误", "未找到加密数据，请先进行加密操作。")
                return
            miwen = data['miwen']
            shang = data['shang']
            prefixes = data['prefixes']
            p = data['p']
            q = data['q']

                # 执行解密
            decrypted_chars = JieMi(miwen, p, q, shang)

            # 筛选符合条件的解组合
            valid_combinations = combine_and_verify(prefixes, decrypted_chars)

            # 输出解密结果
            self.result_box.insert(tk.END, "=== 解密结果 ===\n\n")
            self.result_box.insert(tk.END, f"使用的密钥 p 和 q：{p}, {q}\n\n")
            self.result_box.insert(tk.END, f"解密得到的所有解：{decrypted_chars}\n\n")
            self.result_box.insert(tk.END, f"符合条件的解组合：{valid_combinations}\n\n")
        
        elif mode == '方式三（时间戳）':
            data = self.encrypted_data.get('方式三')
            if not data:
                messagebox.showwarning("解密错误", "未找到加密数据，请先进行加密操作。")
                return
            p = data['p']
            q = data['q']
            miwen = data['miwen']
            shang = data['shang']
            original_timestamps = data['timestamps']
        
            # 执行解密
            decrypted_chars = JieMi(miwen, p, q, shang)

            self.result_box.insert(tk.END, "=== 解密过程 ===\n\n")
            self.result_box.insert(tk.END, f"使用的密钥 p 和 q：{p}, {q}\n\n")
            self.result_box.insert(tk.END, f"解密后的带时间戳的Unicode码值：{decrypted_chars}\n\n")

            # 比对并提取正确字符
            valid_chars_with_timestamps, valid_chars ,all_valid_combinations= verify_and_extract_characters(original_timestamps, decrypted_chars)

            if valid_chars_with_timestamps:
                # 显示比对成功的字符（带时间戳）
                flattened_valid_chars_with_ts = [item for sublist in valid_chars_with_timestamps for item in sublist]
                self.result_box.insert(tk.END, f"比对成功的字符（带时间戳）：{', '.join(flattened_valid_chars_with_ts)}\n\n")
        
                # 显示剥离时间戳后的字符
                flattened_valid_chars = [item for sublist in valid_chars for item in sublist]
                self.result_box.insert(tk.END, f"剥离时间戳后的字符：{', '.join(flattened_valid_chars)}\n\n")
        
                # 显示所有可能的解密组合
                self.result_box.insert(tk.END, f"符合条件的解组合：{', '.join(all_valid_combinations)}\n\n")
            else:
                self.result_box.insert(tk.END, "没有比对成功的解组合。\n\n")
           
        else:
            messagebox.showwarning("模式错误", "未选择有效的标签方式。")
            return

def main():
    root = tk.Tk()
    app = CryptoGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()