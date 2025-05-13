import json, os
import tkinter as tk
from PIL import Image, ImageTk, ImageEnhance
from PIL.ImageOps import expand

from Litmatool import grs
from script.Litmatool import id_tran_name, cn_translate

blocks = [[[0, 1, 1], 'minecraft:glass_pane'], [[0, 1, 3], 'minecraft:sticky_piston'], [[0, 2, 1], 'minecraft:observer'], [[0, 2, 3], 'minecraft:piston_head'], [[0, 2, 4], 'minecraft:smooth_stone'], [[0, 3, 1], 'minecraft:smooth_stone'], [[0, 3, 2], 'minecraft:redstone_block'], [[0, 3, 3], 'minecraft:slime_block'], [[0, 3, 4], 'minecraft:slime_block'], [[0, 3, 5], 'minecraft:slime_block'], [[0, 4, 0], 'minecraft:smooth_stone'], [[0, 4, 1], 'minecraft:oak_trapdoor'], [[0, 4, 8], 'minecraft:smooth_stone'], [[0, 5, 0], 'minecraft:scaffolding'], [[0, 5, 1], 'minecraft:scaffolding'], [[0, 5, 3], 'minecraft:slime_block'], [[0, 5, 4], 'minecraft:slime_block'], [[0, 5, 5], 'minecraft:slime_block'], [[0, 5, 6], 'minecraft:slime_block'], [[0, 5, 8], 'minecraft:scaffolding'], [[0, 6, 3], 'minecraft:red_glazed_terracotta'], [[0, 6, 4], 'minecraft:red_glazed_terracotta'], [[0, 6, 5], 'minecraft:red_glazed_terracotta'], [[0, 7, 3], 'minecraft:pink_bed'], [[0, 7, 3], 'minecraft:pink_bed'], [[0, 7, 4], 'minecraft:pink_bed'], [[1, 0, 1], 'minecraft:smooth_stone'], [[1, 0, 2], 'minecraft:observer'], [[1, 0, 3], 'minecraft:glass_pane'], [[1, 0, 4], 'minecraft:oak_trapdoor'], [[1, 0, 5], 'minecraft:smooth_stone'], [[1, 0, 6], 'minecraft:observer'], [[1, 0, 7], 'minecraft:observer'], [[1, 1, 1], 'minecraft:oak_trapdoor'], [[1, 1, 2], 'minecraft:smooth_stone'], [[1, 1, 4], 'minecraft:glass'], [[1, 1, 5], 'minecraft:smooth_stone'], [[1, 1, 6], 'minecraft:observer'], [[1, 1, 7], 'minecraft:oak_trapdoor'], [[1, 1, 8], 'minecraft:glass_pane'], [[1, 2, 1], 'minecraft:scaffolding'], [[1, 2, 2], 'minecraft:scaffolding'], [[1, 2, 4], 'minecraft:redstone_wire'], [[1, 2, 5], 'minecraft:sticky_piston'], [[1, 2, 6], 'minecraft:observer'], [[1, 2, 7], 'minecraft:scaffolding'], [[1, 2, 8], 'minecraft:observer'], [[1, 3, 3], 'minecraft:stone_brick_wall'], [[1, 3, 4], 'minecraft:stone_brick_wall'], [[1, 3, 5], 'minecraft:stone_brick_wall'], [[1, 3, 8], 'minecraft:smooth_stone'], [[1, 4, 1], 'minecraft:observer'], [[1, 4, 3], 'minecraft:magenta_concrete_powder'], [[1, 4, 4], 'minecraft:red_concrete_powder'], [[1, 4, 5], 'minecraft:yellow_concrete_powder'], [[1, 4, 6], 'minecraft:smooth_stone'], [[1, 4, 7], 'minecraft:observer'], [[1, 4, 8], 'minecraft:oak_trapdoor'], [[1, 5, 1], 'minecraft:observer'], [[1, 5, 6], 'minecraft:sticky_piston'], [[1, 5, 7], 'minecraft:observer'], [[1, 5, 8], 'minecraft:scaffolding'], [[2, 0, 4], 'minecraft:note_block'], [[2, 0, 5], 'minecraft:observer'], [[2, 0, 6], 'minecraft:sticky_piston'], [[2, 0, 7], 'minecraft:oak_trapdoor'], [[2, 1, 1], 'minecraft:observer'], [[2, 1, 4], 'minecraft:smooth_stone'], [[2, 1, 5], 'minecraft:oak_log'], [[2, 1, 7], 'minecraft:observer'], [[2, 2, 1], 'minecraft:observer'], [[2, 2, 4], 'minecraft:redstone_block'], [[2, 2, 5], 'minecraft:slime_block'], [[2, 2, 7], 'minecraft:scaffolding'], [[2, 3, 3], 'minecraft:slime_block'], [[2, 3, 4], 'minecraft:slime_block'], [[2, 3, 5], 'minecraft:slime_block'], [[2, 3, 8], 'minecraft:redstone_block'], [[2, 4, 1], 'minecraft:smooth_stone'], [[2, 4, 3], 'minecraft:glass'], [[2, 4, 4], 'minecraft:glass'], [[2, 4, 5], 'minecraft:glass'], [[2, 5, 0], 'minecraft:slime_block'], [[2, 5, 1], 'minecraft:sticky_piston'], [[2, 5, 3], 'minecraft:gray_concrete_powder'], [[2, 5, 4], 'minecraft:light_blue_concrete_powder'], [[2, 5, 5], 'minecraft:yellow_concrete_powder'], [[3, 0, 4], 'minecraft:smooth_stone'], [[3, 0, 5], 'minecraft:oak_leaves'], [[3, 0, 7], 'minecraft:smooth_stone'], [[3, 1, 1], 'minecraft:smooth_stone'], [[3, 1, 4], 'minecraft:repeater'], [[3, 1, 7], 'minecraft:note_block'], [[3, 1, 8], 'minecraft:sticky_piston'], [[3, 2, 1], 'minecraft:sticky_piston'], [[3, 2, 2], 'minecraft:honey_block'], [[3, 2, 7], 'minecraft:scaffolding'], [[3, 2, 8], 'minecraft:piston_head'], [[3, 3, 0], 'minecraft:slime_block'], [[3, 3, 1], 'minecraft:stone_brick_wall'], [[3, 3, 2], 'minecraft:honey_block'], [[3, 3, 6], 'minecraft:honey_block'], [[3, 3, 7], 'minecraft:stone_brick_wall'], [[3, 3, 8], 'minecraft:slime_block'], [[3, 4, 1], 'minecraft:yellow_concrete_powder'], [[3, 4, 2], 'minecraft:glass'], [[3, 4, 6], 'minecraft:glass'], [[3, 4, 7], 'minecraft:white_concrete_powder'], [[3, 5, 0], 'minecraft:slime_block'], [[3, 5, 2], 'minecraft:yellow_concrete_powder'], [[3, 5, 3], 'minecraft:end_portal'], [[3, 5, 4], 'minecraft:end_portal'], [[3, 5, 5], 'minecraft:end_portal'], [[3, 5, 6], 'minecraft:orange_concrete_powder'], [[3, 5, 8], 'minecraft:slime_block'], [[3, 6, 0], 'minecraft:red_glazed_terracotta'], [[3, 6, 8], 'minecraft:red_glazed_terracotta'], [[4, 0, 2], 'minecraft:observer'], [[4, 0, 6], 'minecraft:observer'], [[4, 1, 1], 'minecraft:glass'], [[4, 1, 4], 'minecraft:smooth_stone'], [[4, 1, 7], 'minecraft:glass'], [[4, 2, 0], 'minecraft:smooth_stone'], [[4, 2, 1], 'minecraft:redstone_wire'], [[4, 2, 2], 'minecraft:redstone_block'], [[4, 2, 4], 'minecraft:observer'], [[4, 2, 6], 'minecraft:redstone_block'], [[4, 2, 7], 'minecraft:redstone_wire'], [[4, 2, 8], 'minecraft:smooth_stone'], [[4, 3, 0], 'minecraft:slime_block'], [[4, 3, 1], 'minecraft:stone_brick_wall'], [[4, 3, 2], 'minecraft:honey_block'], [[4, 3, 6], 'minecraft:honey_block'], [[4, 3, 7], 'minecraft:stone_brick_wall'], [[4, 3, 8], 'minecraft:slime_block'], [[4, 4, 1], 'minecraft:black_concrete_powder'], [[4, 4, 2], 'minecraft:glass'], [[4, 4, 4], 'minecraft:piston'], [[4, 4, 6], 'minecraft:glass'], [[4, 4, 7], 'minecraft:magenta_concrete_powder'], [[4, 5, 0], 'minecraft:slime_block'], [[4, 5, 2], 'minecraft:red_concrete_powder'], [[4, 5, 3], 'minecraft:end_portal'], [[4, 5, 4], 'minecraft:smooth_stone'], [[4, 5, 5], 'minecraft:end_portal'], [[4, 5, 6], 'minecraft:light_blue_concrete_powder'], [[4, 5, 8], 'minecraft:slime_block'], [[4, 6, 0], 'minecraft:red_glazed_terracotta'], [[4, 6, 4], 'minecraft:lever'], [[4, 6, 8], 'minecraft:red_glazed_terracotta'], [[5, 0, 1], 'minecraft:smooth_stone'], [[5, 0, 3], 'minecraft:oak_leaves'], [[5, 0, 4], 'minecraft:smooth_stone'], [[5, 1, 0], 'minecraft:sticky_piston'], [[5, 1, 1], 'minecraft:note_block'], [[5, 1, 4], 'minecraft:repeater'], [[5, 1, 7], 'minecraft:smooth_stone'], [[5, 2, 0], 'minecraft:piston_head'], [[5, 2, 1], 'minecraft:scaffolding'], [[5, 2, 6], 'minecraft:honey_block'], [[5, 2, 7], 'minecraft:sticky_piston'], [[5, 3, 0], 'minecraft:slime_block'], [[5, 3, 1], 'minecraft:stone_brick_wall'], [[5, 3, 2], 'minecraft:honey_block'], [[5, 3, 6], 'minecraft:honey_block'], [[5, 3, 7], 'minecraft:stone_brick_wall'], [[5, 3, 8], 'minecraft:slime_block'], [[5, 4, 1], 'minecraft:green_concrete_powder'], [[5, 4, 2], 'minecraft:glass'], [[5, 4, 6], 'minecraft:glass'], [[5, 4, 7], 'minecraft:yellow_concrete_powder'], [[5, 5, 0], 'minecraft:slime_block'], [[5, 5, 2], 'minecraft:brown_concrete_powder'], [[5, 5, 3], 'minecraft:end_portal'], [[5, 5, 4], 'minecraft:end_portal'], [[5, 5, 5], 'minecraft:end_portal'], [[5, 5, 6], 'minecraft:lime_concrete_powder'], [[5, 5, 8], 'minecraft:slime_block'], [[5, 6, 0], 'minecraft:red_glazed_terracotta'], [[5, 6, 8], 'minecraft:red_glazed_terracotta'], [[6, 0, 1], 'minecraft:oak_trapdoor'], [[6, 0, 2], 'minecraft:sticky_piston'], [[6, 0, 3], 'minecraft:observer'], [[6, 0, 4], 'minecraft:note_block'], [[6, 1, 1], 'minecraft:observer'], [[6, 1, 3], 'minecraft:oak_log'], [[6, 1, 4], 'minecraft:smooth_stone'], [[6, 1, 7], 'minecraft:observer'], [[6, 2, 1], 'minecraft:scaffolding'], [[6, 2, 3], 'minecraft:slime_block'], [[6, 2, 4], 'minecraft:redstone_block'], [[6, 2, 7], 'minecraft:observer'], [[6, 3, 0], 'minecraft:redstone_block'], [[6, 3, 3], 'minecraft:slime_block'], [[6, 3, 4], 'minecraft:slime_block'], [[6, 3, 5], 'minecraft:slime_block'], [[6, 4, 3], 'minecraft:glass'], [[6, 4, 4], 'minecraft:glass'], [[6, 4, 5], 'minecraft:glass'], [[6, 4, 7], 'minecraft:smooth_stone'], [[6, 5, 3], 'minecraft:purple_concrete_powder'], [[6, 5, 4], 'minecraft:light_gray_concrete_powder'], [[6, 5, 5], 'minecraft:pink_concrete_powder'], [[6, 5, 7], 'minecraft:sticky_piston'], [[6, 5, 8], 'minecraft:slime_block'], [[7, 0, 1], 'minecraft:observer'], [[7, 0, 2], 'minecraft:observer'], [[7, 0, 3], 'minecraft:smooth_stone'], [[7, 0, 4], 'minecraft:oak_trapdoor'], [[7, 0, 5], 'minecraft:glass_pane'], [[7, 0, 6], 'minecraft:observer'], [[7, 0, 7], 'minecraft:smooth_stone'], [[7, 1, 0], 'minecraft:glass_pane'], [[7, 1, 1], 'minecraft:oak_trapdoor'], [[7, 1, 2], 'minecraft:observer'], [[7, 1, 3], 'minecraft:smooth_stone'], [[7, 1, 4], 'minecraft:glass'], [[7, 1, 6], 'minecraft:smooth_stone'], [[7, 1, 7], 'minecraft:oak_trapdoor'], [[7, 2, 0], 'minecraft:observer'], [[7, 2, 1], 'minecraft:scaffolding'], [[7, 2, 2], 'minecraft:observer'], [[7, 2, 3], 'minecraft:sticky_piston'], [[7, 2, 4], 'minecraft:redstone_wire'], [[7, 2, 6], 'minecraft:scaffolding'], [[7, 2, 7], 'minecraft:scaffolding'], [[7, 3, 0], 'minecraft:smooth_stone'], [[7, 3, 3], 'minecraft:stone_brick_wall'], [[7, 3, 4], 'minecraft:stone_brick_wall'], [[7, 3, 5], 'minecraft:stone_brick_wall'], [[7, 4, 0], 'minecraft:oak_trapdoor'], [[7, 4, 1], 'minecraft:observer'], [[7, 4, 2], 'minecraft:smooth_stone'], [[7, 4, 3], 'minecraft:blue_concrete_powder'], [[7, 4, 4], 'minecraft:cyan_concrete_powder'], [[7, 4, 5], 'minecraft:gray_concrete_powder'], [[7, 4, 7], 'minecraft:observer'], [[7, 5, 0], 'minecraft:scaffolding'], [[7, 5, 1], 'minecraft:observer'], [[7, 5, 2], 'minecraft:sticky_piston'], [[7, 5, 7], 'minecraft:observer'], [[8, 1, 5], 'minecraft:sticky_piston'], [[8, 1, 7], 'minecraft:glass_pane'], [[8, 2, 4], 'minecraft:smooth_stone'], [[8, 2, 5], 'minecraft:piston_head'], [[8, 2, 7], 'minecraft:observer'], [[8, 3, 3], 'minecraft:slime_block'], [[8, 3, 4], 'minecraft:slime_block'], [[8, 3, 5], 'minecraft:slime_block'], [[8, 3, 6], 'minecraft:redstone_block'], [[8, 3, 7], 'minecraft:smooth_stone'], [[8, 4, 0], 'minecraft:smooth_stone'], [[8, 4, 7], 'minecraft:oak_trapdoor'], [[8, 4, 8], 'minecraft:smooth_stone'], [[8, 5, 0], 'minecraft:scaffolding'], [[8, 5, 2], 'minecraft:slime_block'], [[8, 5, 3], 'minecraft:slime_block'], [[8, 5, 4], 'minecraft:slime_block'], [[8, 5, 5], 'minecraft:slime_block'], [[8, 5, 7], 'minecraft:scaffolding'], [[8, 5, 8], 'minecraft:scaffolding'], [[8, 6, 3], 'minecraft:red_glazed_terracotta'], [[8, 6, 4], 'minecraft:red_glazed_terracotta'], [[8, 6, 5], 'minecraft:red_glazed_terracotta']]
blocks1 = [((0,0,0), 'minecraft:dirt'), ((0,0,1), 'minecraft:grass_block'),( (0,1,0), 'minecraft:lava'), ((1,0,0), 'minecraft:glass')]

class LitStepChecker:
    def __init__(self,blocks):
        self.blocks = blocks
        data = json.load(open(grs(os.path.join('lang', 'data.json')), 'r', encoding='utf-8'))
        self.color_map = data["Color_map"][data["Save"]["ui"]["ColorMap"]]

        self.xl = max([x for (x, _, _), _ in blocks])
        self.yl = max([y for (_, y, _), _ in blocks])
        self.zl = max([z for (_, _, z), _ in blocks])
        print((self.xl, self.yl, self.zl))
        self.pos_blocks = [[[None] * (self.zl + 1) for _ in range(self.yl + 1)] for _ in range(self.xl + 1)]
        for position, block_id in blocks:
            x, y, z = position
            self.pos_blocks[x][y][z] = block_id
        print(self.pos_blocks)

        self.cy = 0
        self.md = 4
        self.images = []

        self.roots = tk.Tk()
        self.roots.title("Litematica Step Checker")
        self.roots.iconbitmap(grs("icon.ico"))
        self.roots.geometry("1000x1000")
        self.frame = tk.Frame(self.roots)
        self.frame.pack(side=tk.TOP)
        self.button_up = tk.Button(self.frame, text="↑", command=lambda: self.change_y("up"))
        self.button_up.pack(side=tk.LEFT)
        self.button_down = tk.Button(self.frame, text="↓", command=lambda: self.change_y("down"))
        self.button_down.pack(side=tk.LEFT)
        self.ck = tk.IntVar(value=1)
        self.checkbutton = tk.Checkbutton(self.frame, text="BEHIND", variable=self.ck)
        self.checkbutton.pack(side=tk.LEFT)
        self.button_re = tk.Button(self.frame, text="Redo", command=lambda: self.update_canvas())
        self.button_re.pack(side=tk.LEFT)
        self.label_y = tk.Label(self.frame, text="Y=0")
        self.label_y.pack(side=tk.LEFT)
        self.canvas = tk.Canvas(self.roots, bg=self.color_map["MC"])
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.update_canvas()
        self.roots.mainloop()

    def update_canvas(self):
        global images
        rwidth = min(self.roots.winfo_width(), self.roots.winfo_height())
        self.images = []
        self.canvas.delete("all")
        self.sx = int((rwidth - 10) / (min(self.xl, self.yl) + 1) / self.md)
        if self.cy > 0 and self.ck.get():
            for i in range(self.xl + 1):
                for j in range(self.zl + 1):
                    id = self.pos_blocks[i][self.cy - 1][j]
                    if not id:
                        continue
                    try:
                        image_path = grs(os.path.join('block', f"{id_tran_name(id)}.png"))
                        image = Image.open(image_path)
                        image = image.convert('RGBA')
                        enc = ImageEnhance.Brightness(image)
                        image = enc.enhance(0.5)
                        image = image.resize((self.sx, self.sx), Image.LANCZOS)
                        new_alpha = Image.new('L', image.size, 64)
                        image.putalpha(new_alpha)
                        photo = ImageTk.PhotoImage(image)
                        self.canvas.create_image(i * self.sx + 5, j * self.sx + 5, anchor="nw", image=photo)
                    except:
                        image_path = grs(os.path.join('block', 'info_update.png'))
                        self.canvas.create_text(i * self.sx + 5, j * self.sx + 5, anchor=tk.NW, text=cn_translate(id))
                        image = Image.open(image_path)
                        image = image.convert('RGBA')
                        enc = ImageEnhance.Brightness(image)
                        image = enc.enhance(0.5)
                        image = image.resize((self.sx, self.sx), Image.LANCZOS)
                        new_alpha = Image.new('L', image.size, 64)
                        image.putalpha(new_alpha)
                        photo = ImageTk.PhotoImage(image)
                        self.canvas.create_image(i * self.sx + 5, j * self.sx + 5, anchor="nw", image=photo)
                    self.images.append((photo, i, j, 0))
                    print(f"Behind layer: {(i, j)}|{id}")

        for i in range(self.xl + 1):
            for j in range(self.zl + 1):
                id = self.pos_blocks[i][self.cy - 1][j]
                print(f"Current layer: {(i, j)}|{id}")
                if not id:
                    continue
                self.photo = None
                try:
                    image = Image.open(grs(os.path.join('block', f"{id_tran_name(id)}.png")))
                    image = image.convert('RGBA').resize((self.sx, self.sx), Image.LANCZOS)
                    self.photo = ImageTk.PhotoImage(image)
                    self.images.append(self.photo)
                    self.canvas.create_image(i * self.sx + 5, j * self.sx + 5, anchor=tk.NW, image=self.photo)
                except Exception as e:
                    print(e)
                    # 加载备用图片
                    image = Image.open(grs(os.path.join('block', 'info_update.png')))
                    image = image.convert('RGBA').resize((self.sx, self.sx), Image.LANCZOS)
                    self.photo = ImageTk.PhotoImage(image)
                    self.images.append(self.photo)
                    self.canvas.create_text(i * self.sx + 5, j * self.sx + 5,
                                            text=cn_translate(id),
                                            anchor=tk.NW)
                self.images.append(self.photo)
                print(f"Current layer: {(i, j)}|{id}")

    def change_y(self,direction):
        if direction == "up" and self.cy > 0:
            self.cy -= 1
        elif direction == "down" and self.cy < self.yl:
            self.cy += 1
        print(self.cy)
        self.label_y.config(text=f"Y={self.cy}")
        self.update_canvas()
        self.roots.update_idletasks()

if __name__ == "__main__":
    LSC = LitStepChecker(blocks)