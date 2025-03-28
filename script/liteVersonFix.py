from amulet_nbt import load, NamedTag, IntTag
import tkinter as tk
from tkinter import filedialog
import os
from Litmatool import grs

ver_opt = ["v7 1.17+", "v5 1.15/1.16", "v4 1.13+"]

def litVerFix(version: int) -> None:
    file_path = filedialog.askopenfilename(filetypes=[("Litematic File", "*.litematic"), ("All File", "*.*")],
                                           title="选择 Litematic 文件")
    if not file_path:
        return

    nbt_file: NamedTag = load(file_path, compressed=True)

    print(nbt_file)

    if 'Version' in nbt_file.tag:
        print(f"原始 Version: {nbt_file.tag['Version']}")
    else:
        print("未找到 Version 标签，将创建它")

    nbt_file.tag['Version'] = IntTag(version)
    print(f"修改后的 Version: {nbt_file.tag['Version']}")

    file_dir, file_name = os.path.split(file_path)
    file_name_without_extension, file_extension = os.path.splitext(file_name)
    new_file_name = f"{file_name_without_extension}_v{nbt_file.tag['Version']}{file_extension}"
    new_file_path = os.path.join(file_dir, new_file_name)

    nbt_file.save_to(new_file_path, compressed=True)
    print(f"文件已保存到: {new_file_path}")

    os.startfile(os.path.dirname(file_path))

if __name__ == "__main__":
    # 创建主窗口
    root = tk.Tk()
    root.title("Litematica 文件版本修复工具")
    root.iconbitmap(grs("tm_icon.ico"))
    root.geometry("300x200")
    tk.Label(text="投影输出版本")

    selected_version = tk.IntVar()

    for idx, option in enumerate(ver_opt):
        tk.Radiobutton(root, text=option, variable=selected_version, value=idx).pack(anchor=tk.W)

    def on_button_click():
        version = 7 if selected_version.get() == 0 else 5 if selected_version.get() == 1 else 4
        print(f"选择的版本: {version}")
        litVerFix(version)

    tk.Button(root, text="修复版本", command=on_button_click).pack(pady=20)

    # 启动主循环
    root.mainloop()