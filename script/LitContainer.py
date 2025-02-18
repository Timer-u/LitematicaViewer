from amulet_nbt import load, NamedTag, IntTag, StringTag, ByteTag
import tkinter as tk
from tkinter import filedialog

def LitContainer() -> None:
    #file_path = filedialog.askopenfilename(filetypes=[("Litematic File", "*.litematic"), ("All File", "*.*")],title="选择 Litematic 文件")
    file_path = "C:/.minecraft2/versions/XPlus1.21.4/schematics/albert/containers.litematic"
    if not file_path:
        return

    nbt_file: NamedTag = load(file_path, compressed=True)
    container = list(nbt_file.tag['Regions'].values())[0]['TileEntities']
    for nt in container:
        x = IntTag(nt['x'])
        y = IntTag(nt['y'])
        z = IntTag(nt['z'])
        id = nt['id']
        print(f"x:{x},y:{y},z:{z},id:{id}---------")
        if 'item' in nt:
            item = nt['item']
            print(f"id:{StringTag(item['id'])}, Count:{IntTag(item['count'])}")
        elif 'Items' in nt:
            item = nt['Items']
            for i in item:
                print(f"id:{StringTag(i['id'])}, Count:{IntTag(i['count'])}, Slot:{ByteTag(i['Slot'])}")
        #print(nt)
        print("\n=================")

if __name__ == "__main__":
    LitContainer()