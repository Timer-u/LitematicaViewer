import threading,sys,os
from amulet_nbt import load, NamedTag, IntTag
from idlelib.history import History
import tkinter as tk
from tkinter import ttk, font, filedialog

from PIL.ImageOps import expand
from customtkinter import *
from litemapy import Schematic, BlockState
from PIL import Image, ImageTk
from easygui import boolbox,choicebox,msgbox,enterbox
from xonsh.completers.tools import justify

sys.path.extend(os.path.join(os.path.dirname(__file__), ".."))


import LitRender
try:
    from script.LitRender import OpenGLView, main_render_loop
    from script.Litmatool import *
    from script.Structure import *
except:
    from LitRender import OpenGLView, main_render_loop
    from Litmatool import *
    from Structure import *
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import importlib, webbrowser, codecs, atexit
import traceback

data = json.load(open(grs(os.path.join('lang', 'data.json')), 'r', encoding='utf-8'))
color_map = data["Color_map"][data["Save"]["ui"]["ColorMap"]]
DefaultFont = data["Save"]["ui"]["Font"]
DefaultFontSize = int(data["Save"]["ui"]["FontSize"])
DefaultCorner = data["Save"]["ui"]["cornerRadius"]

def handle_exception(exc_type, exc_value, exc_traceback):
    error_msg = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    with open("error.log", "w") as f:
        f.write(error_msg)
    sys.exit(1)
sys.excepthook = handle_exception #ERROW.log


your_module = importlib.import_module('litemapy')
YourClass = getattr(your_module, 'Region')
plt.rcParams['font.sans-serif'] = [DefaultFont]  # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

APP_VERSION = '0.7.2'
schematic : Schematic = None
file_path = ""
file_name = "litematica"
#log_path = "../"
Block : dict[str:int] = {} #{id:num,...}
Block_pos : list[tuple[tuple,str,list]] = [] #[(pos,id,prop),...]
Cla_Block = {"实体": [], "羊毛": [], "陶瓦": [], "混凝土": [], "玻璃": [], "木制": [], "石质": [],
                     "其他岩石": [], "石英": [], "矿类": [], "自然类": [], "末地类": [], "地狱类": [], "海晶类": [],
                     "粘土类": [], "红石":[], "铁类":[], "容器":[], "液体":[], "其他": []}
images = {}

if not os.path.exists(grs("history.json")):
    with open(grs("history.json"), "w") as file:
        file.write("{}")

class Setting:
    def __init__(self):
        self.choice = None
    def set_colormap(self):
        self.colormap = ""
        global color_map, data, litem
        cm = data["Save"]["ui"]["ColorMap"]
        self.choice = choicebox(f"更换界面主题色\n目前:{cm}", title="Setting", choices=["蔚蓝色BlueAr","亮绿色LiGreen","暗色Darkly","深蓝色DarkBlue","粉色Pink"])
        if self.choice == "亮绿色LiGreen":
            self.colormap = "Green"
        elif self.choice == "暗色Darkly":
            self.colormap = "Dark"
        elif self.choice == "深蓝色DarkBlue":
            self.colormap = "DBlue"
        elif self.choice == "粉色Pink":
            self.colormap = "Pink"
        elif self.choice == "蔚蓝色BlueAr":
            self.colormap = "BlueAr"
        else:
            return
        data["Save"]["ui"]["ColorMap"] = self.colormap
        color_map = data["Color_map"][self.colormap]
        self.update()

    def set_font(self):
        global DefaultFont
        self.choice = choicebox(f"选择字体\n目前:{DefaultFont}\n如字体前有@则为竖排字体", title="Setting", choices=sorted(font.families()))
        if not self.choice:
            return
        DefaultFont = self.choice
        data["Save"]["ui"]["Font"] = self.choice
        self.update()

    def set_fontsize(self):
        global DefaultFontSize
        self.choice = enterbox(f"选择字体大小\n目前:{DefaultFontSize} | 默认:10\n字体大小建议选择5~15", title="Setting", strip=True, default=DefaultFontSize)
        if not (self.choice or self.choice.isdigit()):
            return
        DefaultFontSize = self.choice
        data["Save"]["ui"]["FontSize"] = int(self.choice)
        self.update()

    def update(self):
        with open(grs(os.path.join('lang', 'data.json')), 'w') as js:
            json.dump(data, js, indent=4)
            print(f"Successfully Upload Setting")
        if boolbox("是否关闭 | 如没关闭请自行重启", title="Setting"):
            exit()

def on_exit():
    with open(grs('log.txt'), "w") as file:
        fw = ""
        for logvar in LogVar:
            fw += str(globals()[logvar].get())
        print(f"Log Rewrite:{fw}")
        file.write(fw)
atexit.register(on_exit) #退出绑定

def ConAly():
    try:
        from script.LitContainer import LitConImport
    except:
        from LitContainer import LitConImport
    threading.Thread(target=LitConImport, daemon=True).start()

def litVerFix(version: int) -> None:
    #["v7 1.20.6+", "v6 1.14~1.20.5", "v3 1.12/1.13"]
    global file_path
    if not file_path:
        file_path = filedialog.askopenfilename(filetypes=[("Litematic File", "*.litematic"), ("All File", "*.*")],title="选择 Litematic 文件")
    if not file_path:
        return
    nbt_file: NamedTag = load(file_path, compressed=True)
    if 'Version' not in nbt_file.tag:
        return
    nbt_file.tag['Version'] = IntTag(version)
    print(f"修改后的 Version: {nbt_file.tag['Version']}")
    file_dir, file_name = os.path.split(file_path)
    file_name_without_extension, file_extension = os.path.splitext(file_name)
    new_file_name = f"{file_name_without_extension}_v{nbt_file.tag['Version']}{file_extension}"
    new_file_path = os.path.join(file_dir, new_file_name)
    nbt_file.save_to(new_file_path, compressed=True)
    print(f"文件已保存到: {new_file_path}")
    os.startfile(os.path.dirname(file_path))

def CS_trans_dict(inp:str) -> dict:
    d1 = inp.strip("\n").split(",")

    d2 = {}
    print(d1, d2)
    for i,s in enumerate(d1):
        init, final =tuple(s.split("-"))
        print(init,final)
        init = "minecraft:"+str(cn_translate(init,False))
        final = "minecraft:"+str(cn_translate(final,False))
        d2[init] = final

    return d2

def import_file():
    global file_path, file_name
    file_path = filedialog.askopenfilename(filetypes=[("Litematic File","*.litematic"),("All File","*.")])
    if not file_path:
        return
    file_path = os.path.normpath(file_path)
    file_name = file_path.split("\\")[-1]
    label_middle.config(text=f"{file_name}")
    print(f"Imported file: {file_path}")

def hide(root , vari , prop = None):
    if not prop: prop = lambda: root.pack(side=tk.LEFT, fill=tk.Y)
    if not vari.get():
        root.pack_forget()
    else:
        prop()
        litem.update_idletasks()

def load_image(block_name):
    try:
        img_path = grs(os.path.join('block', f"{block_name}.png"))
        img = Image.open(img_path)
        img = img.resize((20, 20), Image.LANCZOS)
        img = ImageTk.PhotoImage(img)
        images[block_name] = img
        return img
    except:
        img_path = grs(os.path.join('block', 'info_update.png'))
        img = Image.open(img_path)
        img = img.resize((20, 20), Image.LANCZOS)
        img = ImageTk.PhotoImage(img)
        images[block_name] = img
        return img

def insert_table(block_state, count):
    if isinstance(block_state, BlockState):
        block_id = block_state._BlockState__block_id
        block_name = block_id.split(":")[-1]
    else:
        block_id = block_state
        block_name = block_id.split(":")[-1]
    img = load_image(block_name)
    count_table.insert('', 'end', image=img, values=(cn_translate(block_name), str(count), convert_units(count), block_name))
    litem.update_idletasks()

def output_data(classification : bool = False):
    global Block
    output_file_path = tk.filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"),
                                                                                            ("CSV Chart files",
                                                                                            "*.csv")],
                                                           title="Litematica Analysis Data Save As",
                                                           initialfile=f'''{file_name.split(".")[0]}.txt''')
    if not output_file_path:
        return
    with codecs.open(output_file_path, 'w', encoding='utf-8-sig') as f:
        Block = dict(sorted(Block.items(), key=lambda x: x[1], reverse=True))  # Block = list
        if not classification:
            for val in Block:
                num = Block[val]
                id = val.split("[")[0].split(":")[-1]
                extension = os.path.splitext(output_file_path)[1].lower()
                if extension == ".csv":
                    f.write(f"{cn_translate(id)},{id},{num},{convert_units(num)}\n")
                else:
                    f.write(f"{num}[{convert_units(num)}] | {cn_translate(id)} [{id}]\n")
        else:
            for catigory in Cla_Block:
                if Cla_Block[catigory]:
                    f.write(f"\n{catigory}\n" + "-" * 20 + "\n")
                for val in Cla_Block[catigory]:
                    num = val[0]
                    id = str(val[1]).split("[")[0].split(":")[-1]
                    extension = os.path.splitext(output_file_path)[1].lower()
                    if extension == ".csv":
                        f.write(f"{cn_translate(id)},{id},{num},{convert_units(num)}\n")
                    else:
                        f.write(f"{num}[{convert_units(num)}] | {cn_translate(id)}[{id}]\n")
    if sys.platform == 'darwin':
        subprocess.call(['open', output_file_path])
    elif sys.platform == 'win32':
        os.startfile(output_file_path)

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']  # 指定中文字体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
#plt.figure(facecolor=color_map["MC"])

def Draw_Chart():
    ax1.clear()
    ax2.clear()

    sorted_block = sorted(Block.items(), key=lambda x: x[1], reverse=True)
    top_5 = sorted_block[:5]
    other_count = sum(count for _, count in sorted_block[5:])
    labels1 = [cn_translate(block_id.split(":")[-1]) for block_id, _ in top_5]
    sizes1 = [count for _, count in top_5]
    if other_count > 0:
        labels1.append("其他")
        sizes1.append(other_count)
    ax1.pie(sizes1, labels=labels1, autopct='%1.1f%%', startangle=90)
    ax1.set_title("方块统计")

    cla_bl = {}
    for category, blocks in Cla_Block.items():
        if blocks:
            total = sum(count for count, _ in blocks)
            cla_bl[category] = total

    # 处理“其他”类别
    if "其他" in cla_bl:
        cat_other = cla_bl.pop("其他")
    else:
        cat_other = 0

    sorted_block = sorted(cla_bl.items(), key=lambda x: x[1], reverse=True)
    top_5 = sorted_block[:5]
    other_count = sum(count for _, count in sorted_block[5:]) + cat_other
    labels2 = [cate for cate, _ in top_5]
    sizes2 = [count for _, count in top_5]
    if other_count > 0:
        labels2.append("其他")
        sizes2.append(other_count)
    ax2.pie(sizes2, labels=labels2, autopct='%1.1f%%', startangle=90)
    ax2.set_title("分类统计")

    canvas1.draw()
    canvas2.draw()
    return sorted_block[:1]


def start_analysis():
    global schematic, Cla_Block, Block_pos, gl_view, Block
    historyFile = json.load(open(grs("history.json"), 'r', encoding='utf-8'))
    print(f"HistoryFile loaded: {historyFile}")
    print(file_path)
    if not file_path:
        import_file()
    Cla_Block = {"实体": [], "羊毛": [], "陶瓦": [], "混凝土": [], "玻璃": [], "木制": [], "石质": [],
                 "其他岩石": [], "石英": [], "矿类": [], "自然类": [], "末地类": [], "地狱类": [], "海晶类": [],
                 "粘土类": [], "红石": [], "铁类": [], "容器": [], "液体": [], "其他": []}
    Block_pos = []
    Block.clear()
    count_table.delete(*count_table.get_children())
    schematic = Schematic.load(file_path)
    nbt_file: NamedTag = load(file_path, compressed=True)
    SCblock = nbt_file.tag['Metadata']['TotalBlocks']
    SCname = schematic.name
    SCauthor = schematic.author
    SCdesc = schematic.description
    SClv = schematic.lm_version
    SCver : str
    if SClv <= 3:
        SCver = "1.12/1.13"
    elif SClv <= 6:
        SCver = "1.14~1.20.5"
    elif SClv >= 7:
        SCver = "1.20.6+"
    else:
        SCver = "1.12+"
    #if str(schematic) not in historyFile:
    num = 0
    acnum = 0
    print(f"--Schematic loaded: {schematic}|Name:{SCname}|Author:{SCauthor}|Description:{SCdesc}|Version:{SCver}|")
    for region_index, region in enumerate(schematic.regions.values()):
        print(f"--Analyzing region {region_index + 1}")
        size_x = region.maxx() - region.minx() + 1
        size_y = region.maxy() - region.miny() + 1
        size_z = region.maxz() - region.minz() + 1
        for x in range(size_x):
            for y in range(size_y):
                for z in range(size_z):
                    block_state = region._Region__palette[region._Region__blocks[x, y, z]]
                    block_id = block_state._BlockState__block_id
                    block_property = block_state._BlockState__properties
                    if block_id not in ["minecraft:air", "minecraft:cave_air", "minecraft:void_air"]:
                        Block_pos.append([[x, y, z], str(block_id)])
                        num += 1
                        if block_id not in ["minecraft:piston_head",
                                            "minecraft:nether_portal", "minecraft:moving_piston",
                                            "minecraft:bedrock"]:
                            MBB = ["potted_", "_cake", "wall_", "_cauldron"] #组合逆天方块
                            Analysis= { #简单转换方块
                                "minecraft:farmland": "minecraft:dirt",
                                "minecraft:dirt_path": "minecraft:dirt",
                                "minecraft:bubble_column": "minecraft:water",
                                "minecraft:soul_fire": "minecraft:fire"
                            }
                            prop_list = [('waterlogged', 'true', "minecraft:water", 1), #属性判断方块
                                         ('type', 'double', None, 2),
                                         ('half', 'upper', None, -1),
                                         ('part', 'head', None, -1),
                                         ('eggs', '', "minecraft:turtle_egg", 0),
                                         ('pickles', '', "minecraft:sea_pickle", 0),
                                         ('charges', '', "minecraft:glowstone", 0),
                                         ('flower_amount', '', "minecraft:pink_petals", 0)]
                            output = block_id
                            # 简单转换方块
                            for a in Analysis:
                                output = Analysis[a] if block_id == a else block_id
                            # 组合逆天方块
                            for root in MBB:
                                if root in block_id:
                                    output = block_id.replace(root, "")
                            # 属性判断方块
                            for pt, pv, pf, pn in prop_list:
                                if pt in block_property:
                                    if not pn: pn = int(block_property[pt])
                                    if block_property[pt] == pv or not pv:
                                        if not pf:
                                            Block[output] = Block[output]+pn if output in Block else pn
                                        elif pf not in Block:
                                            Block[pf] = pn
                                        else:
                                            Block[pf] = Block[pf]+pn
                                        continue
                            Block[output] = Block[output]+1 if output in Block else 1

        if DoEntity.get():
            for entity in region._Region__entities:
                entity_type = "E/" + str(entity.id)
                if entity_type not in ["E/minecraft:item", "E/minecraft:bat", "E/minecraft:experience_orb",
                                       "E/minecraft:shulker_bullet"]:
                    if entity_type not in Block:
                        Block[entity_type] = 1
                    else:
                        Block[entity_type] += 1
        '''historyFile[str(schematic)] = [Block, Block_pos, [size_x, size_y, size_z, num]]
        print(historyFile)
        with open("history.json", 'w') as jh:
            json.dump(historyFile, jh, indent=4)
            print(f"History File saved with {str(schematic)}")'''

    '''else:
        print(f"Find History File with {str(schematic)}")
        Block = historyFile[str(schematic)][0]
        Block_pos = historyFile[str(schematic)][1]
        size_x,size_y,size_z,num=historyFile[str(schematic)][2]'''

    time = 1 if entry_times.get() == "" else int(entry_times.get())
    for val in Block:
        id = val.split("[")[0].split(":")[-1]
        typeB = Category_Tran(id)
        if val.split("/")[0]=="E":
            Cla_Block["实体"].append((Block[val], val))
        elif typeB != "":
            Cla_Block[typeB].append((Block[val], val))
        else:
            Cla_Block["其他"].append((Block[val], val))
    print(f"{Cla_Block}")
    label_bottom.config(
        text=f"Size体积: {size_x}x{size_y}x{size_z} | Number数量: {num} | Times倍数: {time} | Types种类: {len(Block)}")

    top1 = Draw_Chart()
    sorted_block = sorted(Block.items(), key=lambda x: x[1], reverse=True)
    a_den.config(text=f"{num / (size_x * size_y * size_z) * 100:.1f}%")
    redly = (sum(n for n, _ in Cla_Block["红石"])+sum(n for n, _ in Cla_Block["容器"])) / (num-sorted_block[0][1] if len(Block)>5 else num)
    if num > 10:
        if redly>0.5:
            me_type = "红石机器"
        elif redly>=0.3:
            me_type = "生电红石"
        elif redly>=0.1:
            me_type = "生电机器"
        elif redly>=0.01:
            me_type = "结构性机器"
        elif redly<0.01:
            me_type = top1[0][0]+"建筑"
    else:
        me_type = "方块太少"
    a_red.config(text=f"{redly*100:.1f}%")
    a_redt.config(text=f"{me_type}")
    fluid = sum(n for n, _ in Cla_Block["液体"])
    a_liq.config(text=f"{fluid / num * 100:.1f}%\n{fluid}u")
    a_auth.config(text=SCauthor)
    a_ver.config(text=SCver)
    a_desc.config(text=SCdesc)
    analysis_debug.config(text=f"Analysis DEBUG: {SCblock==num}")
    for index, (block_state, count) in enumerate(sorted_block):
        try:
            count = count * int(entry_times.get())
        except:
            count = count * 1
        insert_table(block_state, count)

    if Do3d.get():
        if Pn3d.get():
            gl_view.destroy()
            if Li3d.get() and num>1000:
                if num>5000:
                    check = boolbox("Block Number over 5000, keep rendering?\n方块数量超过5千,是否继续渲染,可能会崩溃\n继续渲染将关闭旋转模式 Keep rendering will shut spinning mode",default_choice="是/Y 会变一次性",cancel_choice="取消/N 明智的选择")
                    if not check: return
                    threading.Thread(target=LitRender.main_render_loop(Block_pos,bool(False)), daemon=True).start()
                    return
                gl_view = OpenGLView(frame_3d, Block_pos, False, width=300, height=300, bg=color_map["PC"])
            else:
                gl_view = OpenGLView(frame_3d, Block_pos, bool(Sp3d.get()), width=300, height=300, bg=color_map["PC"])
            gl_view.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            gl_view.after(1000, gl_view.redraw)
        else:
            if Li3d.get() and num>1000:
                if num>5000:
                    check = boolbox("Block Number over 5000, keep rendering?\n方块数量超过5千,是否继续渲染,可能会崩溃\n继续渲染将关闭旋转模式 Keep rendering will shut spinning mode",default_choice="是/Y 会变一次性",cancel_choice="取消/N 明智的选择")
                    if not check: return
                threading.Thread(target=LitRender.main_render_loop(Block_pos,bool(False)), daemon=True).start()
            else:
                threading.Thread(target=LitRender.main_render_loop(Block_pos,bool(Sp3d.get())), daemon=True).start()
    litem.update_idletasks()

if __name__ == "__main__":
    #  主窗口
    litem = tk.Tk()
    litem.title(f"Litematica Viewer投影查看器 v{APP_VERSION}")
    litem.iconbitmap(grs("icon.ico"))
    litem.geometry("1280x768")
    litem.configure(bg=color_map["BG"])

    if data["Save"]["First_open"] == "0":
        msgbox('''LitematicaViewer投影查看器V0.7.2更新报告Log
        1. 更新界面主题颜色 帮助-界面颜色更改主题色
        2. 修改分析BUG 特殊方块将正常分析 (门,海龟蛋,土径...)''')
        data["Save"]["First_open"] = "1"
        with open(grs(os.path.join('lang', 'data.json')), 'w') as js:
            json.dump(data, js, indent=2)

    LogVar = ["DoEntity", "DoLifr", "DoStat", "DoAnal", "Do3d", "Pn3d", "Li3d", "Sp3d"]
    menu = tk.Menu(litem)
    DoEntity = tk.IntVar()
    DoLifr = tk.IntVar()
    DoStat = tk.IntVar()
    DoAnal = tk.IntVar()
    Do3d = tk.IntVar()
    Pn3d = tk.IntVar()
    Li3d = tk.IntVar()
    Sp3d = tk.IntVar()
    if not os.path.exists(grs("log.txt")):
        with open(grs("log.txt"), "w") as file:
            file.write("11111111")  # d1:Entity, d2-4:Frame, d5-8:3D
            for logvar in LogVar:
                globals()[logvar] = tk.IntVar(value=1)
    else:
        with open(grs("log.txt"), "r") as file:
            fr = file.read()
            try:
                logvan = 0
                for logvar in LogVar:
                    globals()[logvar] = tk.IntVar(value=int(fr[logvan]))
                    logvan+=1

            except:
                for logvar in LogVar:
                    globals()[logvar] = tk.IntVar(value=1)

    menu_analysis = tk.Menu(menu, tearoff=0)
    menu_analysis.add_command(label="导入", command=import_file, font=(DefaultFont, DefaultFontSize))
    menu_analysis.add_command(label="导出", command=lambda:output_data(False), font=(DefaultFont, DefaultFontSize))
    menu_analysis.add_command(label="分类导出", command=lambda:output_data(True), font=(DefaultFont, DefaultFontSize))
    menu_analysis.add_command(label="分析", command=lambda:threading.Thread(target=start_analysis(True), daemon=True).start(), font=(DefaultFont, DefaultFontSize))
    #menu_analysis.add_command(label="FullAnalysis全面分析", command=lambda:threading.Thread(target=start_analysis(True), daemon=False).start(), font=(DefaultFont, DefaultFontSize))
    menu_analysis.add_command(label="生成图形投影", command=lambda : create_structure(f"minecraft:{cn_translate(entry_id.get(),False)}",
                                                            (entry_x.get(),entry_y.get(),entry_z.get()),
                                                            (entry_length.get(),entry_width.get(),entry_height.get()), False, 0, [False,False,False,False,False,False]
                                                            ), font=(DefaultFont, DefaultFontSize))
    menu_analysis.add_command(label="替换特定方块", command=lambda : change_Schematic(schematic, text_change.get("1.0", tk.END), ((entry_min_x.get(),entry_max_x.get()),(entry_min_y.get(),entry_max_y.get()),(entry_min_z.get(),entry_max_z.get())), file_name.split(".")[0]+"_Modified"), font=(DefaultFont, DefaultFontSize))
    menu.add_cascade(label="数据分析", menu=menu_analysis, font=(DefaultFont, int(DefaultFontSize*2.0)))
    menu_AnaSet = tk.Menu(menu, tearoff=0)
    menu.add_cascade(label="设置",menu=menu_AnaSet, font=(DefaultFont, int(DefaultFontSize*2.0)))
    menu_AnaSet.add_checkbutton(label="是否分析实体",variable=DoEntity, font=(DefaultFont, DefaultFontSize))
    menu_AnaSet.add_separator()
    menu_AnaSet.add_checkbutton(label="是否显示投影面板",variable=DoLifr,command=lambda:hide(frame_func,DoLifr), font=(DefaultFont, DefaultFontSize))
    menu_AnaSet.add_checkbutton(label="是否显示统计面板",variable=DoStat,command=lambda:hide(frame_data,DoStat), font=(DefaultFont, DefaultFontSize))
    menu_AnaSet.add_checkbutton(label="是否显示分析面板", variable=DoAnal,command=lambda: hide(frame_middle,DoAnal), font=(DefaultFont, DefaultFontSize))
    menu_AnaSet.add_separator()
    menu_3d = tk.Menu(menu, tearoff=0)
    menu_AnaSet.add_cascade(label="3D选项", menu=menu_3d, font=(DefaultFont, DefaultFontSize))
    menu_3d.add_checkbutton(label="是否3D渲染", variable=Do3d, font=(DefaultFont, DefaultFontSize))
    menu_3d.add_checkbutton(label="3D面板集中显示", variable=Pn3d, font=(DefaultFont, DefaultFontSize))
    menu_3d.add_checkbutton(label="3D渲染限制(1000u限制)", variable=Li3d, font=(DefaultFont, DefaultFontSize))
    menu_3d.add_checkbutton(label="3D渲染是否旋转", variable=Sp3d, font=(DefaultFont, DefaultFontSize))
    menu_Setting = tk.Menu(menu, tearoff=0)
    menu_AnaSet.add_cascade(label="界面设置", menu=menu_Setting, font=(DefaultFont, DefaultFontSize))
    setting = Setting()
    menu_Setting.add_command(label="界面颜色", font=(DefaultFont, DefaultFontSize), command=setting.set_colormap)
    menu_Setting.add_command(label="界面字体", font=(DefaultFont, DefaultFontSize), command=setting.set_font)
    menu_Setting.add_command(label="字体大小", font=(DefaultFont, DefaultFontSize), command=setting.set_fontsize)
    menu_Func = tk.Menu(menu, tearoff=0)
    menu.add_cascade(label="功能",menu=menu_Func, font=(DefaultFont, int(DefaultFontSize*2.0)))
    menu_Func.add_command(label="跨版本-1.17+", command=lambda:litVerFix(7), font=(DefaultFont, DefaultFontSize))
    menu_Func.add_command(label="跨版本-1.15+", command=lambda:litVerFix(6), font=(DefaultFont, DefaultFontSize))
    menu_Func.add_command(label="跨版本-1.13+", command=lambda:litVerFix(3), font=(DefaultFont, DefaultFontSize))
    menu_Func.add_separator()
    menu_Func.add_command(label="容器分析", command=lambda:ConAly(), font=(DefaultFont, DefaultFontSize))
    menu_Func.add_command(label="手动3D渲染", command=lambda: threading.Thread(target=LitRender.main_render_loop(Block_pos,bool(False)), daemon=True).start(), font=(DefaultFont, DefaultFontSize))
    menu_Help = tk.Menu(menu, tearoff=0)
    menu.add_cascade(label="帮助",menu=menu_Help, font=(DefaultFont, int(DefaultFontSize*2.0)))
    menu_Help.add_command(label="关于", command=lambda:webbrowser.open("https://github.com/albertchen857/LitematicaViewer"), font=(DefaultFont, DefaultFontSize))
    menu_Help.add_command(label="关于作者", command=lambda:webbrowser.open("https://space.bilibili.com/3494373232741268"), font=(DefaultFont, DefaultFontSize))
    menu_Help.add_command(label="手动更新软件库", command=manual_install_pk, font=(DefaultFont, DefaultFontSize))
    litem.config(menu=menu, padx=10)

    #  顶容器
    frame_top = tk.Frame(litem)
    frame_top.configure(bg=color_map["BG"], bd=5)
    frame_top.pack(side=tk.TOP, fill=tk.X)

    btn_import = CTkButton(frame_top, text="Import导入", command=import_file, font=(DefaultFont, DefaultFontSize*1.5))
    btn_import.configure(fg_color=color_map["PC"],text_color=color_map["BG"],corner_radius=DefaultCorner)
    btn_import.pack(side=tk.LEFT, padx=5)
    btn_simstart = CTkButton(frame_top, text="Analysis简洁分析", command=lambda:threading.Thread(target=start_analysis, daemon=True).start(), font=(DefaultFont, DefaultFontSize*1.5))
    btn_simstart.configure(fg_color=color_map["PC"],text_color=color_map["BG"],corner_radius=DefaultCorner)
    btn_simstart.pack(side=tk.LEFT, padx=5)
    btn_hint = CTkButton(frame_top, text="!HINT注意事项!",
                             command=lambda: msgbox('''----HINT----\n1. 导入文件后需手动点击「简介分析」\n2. 首次点击「简介分析」自动打开导入界面\n3. 非必要关闭 设置-渲染是否渲染 设置. 低配置请关闭渲染 设置-是否3d渲染\n4. 方块ID和替换表可输入中文名或游戏ID (泥土 & minecraft:dirt)\n5. 替换表格式为 原方块-替换方块,原方块2-替换方块2,...\n\t「-」分割新旧方块, 「,」分割不同的组 方块可以中文名和ID混搭使用'''),
                             font=(DefaultFont, DefaultFontSize*1.5))
    btn_hint.configure(fg_color=color_map["PC"], text_color=color_map["BG"], corner_radius=DefaultCorner)
    btn_hint.pack(side=tk.LEFT, padx=5)

    btn_github = CTkButton(frame_top, text="GitHub", command=lambda:webbrowser.open("https://github.com/albertchen857/LitematicaViewer"), font=(DefaultFont, DefaultFontSize*1.5))
    btn_github.configure(fg_color="black",text_color="#f8f9fa",corner_radius=DefaultCorner)
    btn_github.pack(side=tk.RIGHT, padx=5)
    btn_bilibili = CTkButton(frame_top, text="Bilibili", command=lambda:webbrowser.open("https://space.bilibili.com/3494373232741268"), font=(DefaultFont, DefaultFontSize*1.5))
    btn_bilibili.configure(fg_color="#FF6699", text_color="#f8f9fa",corner_radius=DefaultCorner)
    btn_bilibili.pack(side=tk.RIGHT, padx=5)

    #  func容器
    frame_func = CTkFrame(litem, fg_color=color_map["MC"], corner_radius=DefaultCorner)
    hide(frame_func, DoLifr,lambda :frame_func.pack(side=tk.RIGHT, fill=tk.BOTH, padx=10, pady=10))
    #  投影创建容器：frame_func_new
    frame_func_new = tk.Frame(frame_func, bg=color_map["MC"])
    frame_func_new.pack(side=tk.TOP, fill=tk.X,  padx=20, pady=20)
    frame_new_title = tk.Label(frame_func_new, text="生成图形投影", font=(DefaultFont, int(DefaultFontSize*1.8)), bg=color_map["MC"], fg=color_map["TT"])
    frame_new_title.grid(row=0, column=0, padx=5, pady=5, columnspan=4)
    # -- ID 输入框
    label_id = tk.Label(frame_func_new, text="方块ID", font=(DefaultFont, int(DefaultFontSize*1.2)), bg=color_map["MC"], fg=color_map["TT"])
    label_id.grid(row=1, column=0, padx=5, pady=5)
    entry_id = tk.Entry(frame_func_new, width=20, bg=color_map["BG"], fg=color_map["PC"], font=(DefaultFont, DefaultFontSize))
    entry_id.grid(row=1, column=1, padx=5, pady=5, columnspan=3)
    # -- XYZ 长宽高输入框
    label_xyz = tk.Label(frame_func_new, text="原点XYZ", font=(DefaultFont, int(DefaultFontSize*1.2)), bg=color_map["MC"], fg=color_map["TT"])
    label_xyz.grid(row=2, column=0, padx=5, pady=5)
    label_lwh = tk.Label(frame_func_new, text="宽高长Size", font=(DefaultFont, int(DefaultFontSize*1.2)), bg=color_map["MC"], fg=color_map["TT"])
    label_lwh.grid(row=3, column=0, padx=5, pady=5)
    entry_x = tk.Entry(frame_func_new, width=5, bg=color_map["BG"], fg=color_map["PC"], font=(DefaultFont, DefaultFontSize))
    entry_x.grid(row=2, column=1, padx=2, pady=5)
    entry_y = tk.Entry(frame_func_new, width=5, bg=color_map["BG"], fg=color_map["PC"], font=(DefaultFont, DefaultFontSize))
    entry_y.grid(row=2, column=2, padx=2, pady=5)
    entry_z = tk.Entry(frame_func_new, width=5, bg=color_map["BG"], fg=color_map["PC"], font=(DefaultFont, DefaultFontSize))
    entry_z.grid(row=2, column=3, padx=2, pady=5)
    entry_length = tk.Entry(frame_func_new, width=5, bg=color_map["BG"], fg=color_map["PC"], font=(DefaultFont, DefaultFontSize))
    entry_length.grid(row=3, column=3, padx=2, pady=5)
    entry_width = tk.Entry(frame_func_new, width=5, bg=color_map["BG"], fg=color_map["PC"], font=(DefaultFont, DefaultFontSize))
    entry_width.grid(row=3, column=2, padx=2, pady=5)
    entry_height = tk.Entry(frame_func_new, width=5, bg=color_map["BG"], fg=color_map["PC"], font=(DefaultFont, DefaultFontSize))
    entry_height.grid(row=3, column=1, padx=2, pady=5)
    btn_spawn = CTkButton(frame_func_new, text="生成", font=(DefaultFont, DefaultFontSize*1.6, "bold"),
                          command=lambda : create_structure(f"minecraft:{cn_translate(entry_id.get(),False)}",
                                                            (entry_x.get(),entry_y.get(),entry_z.get()),
                                                            (entry_length.get(),entry_width.get(),entry_height.get()), False, 0, [False,False,False,False,False,False]
                                                            ))
    btn_spawn.configure(fg_color=color_map["BG"],text_color=color_map["TT"],corner_radius=DefaultCorner)
    btn_spawn.grid(row=8, column=0, padx=2, pady=2, columnspan=4)
    label_tip = tk.Label(frame_func_new, text="ID输入可以为纯英文或中文名", font=(DefaultFont, DefaultFontSize, "bold"), bg=color_map["MC"], fg="#f70400")
    label_tip.grid(row=9, column=0, padx=5, pady=5, columnspan=4)
    #  方块替换容器：frame_func_change
    frame_func_change = tk.Frame(frame_func, bg=color_map["MC"])
    frame_func_change.pack(side=tk.TOP, fill=tk.X, pady=20, padx=20)
    frame_change_title = tk.Label(frame_func_change, text="替换特定方块", font=(DefaultFont, int(DefaultFontSize*1.8)), bg=color_map["MC"],fg=color_map["TT"])
    frame_change_title.grid(row=0, column=0, padx=5, pady=20, columnspan=4)

    # -- Limit 标签和 XYZ 输入框
    label_min = tk.Label(frame_func_change, text="最小限制XYZ", font=(DefaultFont, int(DefaultFontSize*1.2)), bg=color_map["MC"], fg=color_map["TT"])
    label_min.grid(row=1, column=0, padx=5, pady=5)
    entry_min_x = tk.Entry(frame_func_change, width=5, bg=color_map["BG"], fg=color_map["PC"], font=(DefaultFont, DefaultFontSize))
    entry_min_x.grid(row=1, column=1, padx=2, pady=5)
    entry_min_y = tk.Entry(frame_func_change, width=5, bg=color_map["BG"], fg=color_map["PC"], font=(DefaultFont, DefaultFontSize))
    entry_min_y.grid(row=1, column=2, padx=2, pady=5)
    entry_min_z = tk.Entry(frame_func_change, width=5, bg=color_map["BG"], fg=color_map["PC"], font=(DefaultFont, DefaultFontSize))
    entry_min_z.grid(row=1, column=3, padx=2, pady=5)
    label_max = tk.Label(frame_func_change, text="最大限制XYZ", font=(DefaultFont, int(DefaultFontSize*1.2)), bg=color_map["MC"], fg=color_map["TT"])
    label_max.grid(row=2, column=0, padx=5, pady=5)
    entry_max_x = tk.Entry(frame_func_change, width=5, bg=color_map["BG"], fg=color_map["PC"], font=(DefaultFont, DefaultFontSize))
    entry_max_x.grid(row=2, column=1, padx=2, pady=5)
    entry_max_y = tk.Entry(frame_func_change, width=5, bg=color_map["BG"], fg=color_map["PC"], font=(DefaultFont, DefaultFontSize))
    entry_max_y.grid(row=2, column=2, padx=2, pady=5)
    entry_max_z = tk.Entry(frame_func_change, width=5, bg=color_map["BG"], fg=color_map["PC"], font=(DefaultFont, DefaultFontSize))
    entry_max_z.grid(row=2, column=3, padx=2, pady=5)

    # -- Change 标签和多行输入框
    tk.Label(frame_func_change, text="替换表", font=(DefaultFont, int(DefaultFontSize*1.2)), bg=color_map["MC"], fg=color_map["TT"]).grid(row=3, column=0, padx=5, pady=5)
    text_change = tk.Text(frame_func_change,width=20, height=5, bg=color_map["BG"], fg=color_map["PC"], font=(DefaultFont, DefaultFontSize))
    text_change.grid(row=3, column=1, columnspan=3, padx=5, pady=5)

    btn_spawn2 = CTkButton(frame_func_change, text="生成", font=(DefaultFont, DefaultFontSize*1.6, "bold"), command=lambda : change_Schematic(schematic, CS_trans_dict(text_change.get("1.0", tk.END)), ((entry_min_x.get(),entry_max_x.get()),(entry_min_y.get(),entry_max_y.get()),(entry_min_z.get(),entry_max_z.get())), file_name.split(".")[0]+"_Modified"))
    btn_spawn2.configure(fg_color=color_map["BG"],text_color=color_map["TT"],corner_radius=DefaultCorner)
    btn_spawn2.grid(row=5, column=0, padx=2, pady=2, columnspan=4)
    tk.Label(frame_func_change, text="替换表= 旧方块-新方块,...", font=(DefaultFont, DefaultFontSize, "bold"), bg=color_map["MC"], fg="#f70400").grid(row=6, column=0, padx=5, pady=5, columnspan=4)
    # -- 分析设置
    frame_Output = CTkScrollableFrame(frame_func, fg_color=color_map["BG"], corner_radius=DefaultCorner)
    frame_Output.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=20, pady=20)
    CTkLabel(frame_Output, text="分析设置", font=(DefaultFont, int(DefaultFontSize*2.0), "bold"), fg_color=color_map["BG"], text_color=color_map["TT"]).pack(side=tk.TOP, fill=tk.BOTH, padx=10, pady=10)
    frame_times = tk.Frame(frame_Output, bg=color_map["BG"])
    frame_times.pack(side=tk.TOP, fill=tk.BOTH, padx=10, pady=5)
    tk.Label(frame_times, text="Times倍数", font=(DefaultFont, int(DefaultFontSize*1.5)),bg=color_map["BG"], fg=color_map["TT"]).pack(side=tk.LEFT, padx=5)
    entry_times = tk.Entry(frame_times, width=10, bg=color_map["BG"], fg=color_map["PC"], font=(DefaultFont, DefaultFontSize))
    entry_times.pack(side=tk.RIGHT, padx=5)
    frame_debug = tk.Frame(frame_Output, bg=color_map["BG"])
    frame_debug.pack(side=tk.TOP, fill=tk.BOTH, padx=10, pady=10)
    analysis_debug = tk.Label(frame_debug, text="分析DEBUG: True", bg=color_map["BG"], font=(DefaultFont, int(DefaultFontSize*1.5)))
    analysis_debug.pack(side=tk.TOP, padx=10)
    CTkLabel(frame_debug, text="如debug为false为分析有误 请勿使用!", font=(DefaultFont, int(DefaultFontSize), "bold"), fg_color=color_map["BG"], text_color="#f70400").pack(side=tk.TOP, fill=tk.BOTH, padx=10)

    #  中分析容器
    frame_middle = CTkFrame(litem, fg_color=color_map["MC"], corner_radius=DefaultCorner)
    hide(frame_middle,DoAnal,lambda :frame_middle.pack(side=tk.RIGHT, fill=tk.BOTH, padx=10, pady=10, expand=True))
    # - 标题容器
    frame_middle_top = CTkFrame(frame_middle, fg_color=color_map["BG"], corner_radius=DefaultCorner)
    frame_middle_top.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
    label_middle = tk.Label(frame_middle_top, text="LitematicaViewer投影查看器", font=(DefaultFont, DefaultFontSize*3, 'bold'))
    label_middle.configure(bg=color_map["BG"], fg=color_map["TT"], bd=5)
    label_middle.pack(fill=tk.Y)
    label_bottom = tk.Label(frame_middle_top, text="Size体积 | Number数量 | Times倍数 | Types种类", font=(DefaultFont, int(DefaultFontSize*1.4), "bold"))
    label_bottom.configure(bg=color_map["BG"], fg=color_map["PC"], bd=5)
    label_bottom.pack(side=tk.LEFT, fill=tk.X, padx=20, pady=10)
    
    # 统计图标容器
    frame_data = tk.Frame(frame_middle, bg=color_map["MC"])
    hide(frame_data, DoStat, lambda: frame_data.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10))
    frame_pie1 = CTkFrame(frame_data, fg_color=color_map["BG"], corner_radius=DefaultCorner)
    frame_pie1.pack(side=tk.TOP, fill=tk.BOTH, pady=10)
    frame_pie2 = CTkFrame(frame_data, fg_color=color_map["BG"], corner_radius=DefaultCorner)
    frame_pie2.pack(side=tk.TOP, fill=tk.BOTH, pady=10)
    fig1 = Figure(figsize=(4, 3), dpi=80)
    ax1 = fig1.add_subplot(111)
    canvas1 = FigureCanvasTkAgg(fig1, master=frame_pie1)
    canvas1.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    fig2 = Figure(figsize=(4, 3), dpi=80)
    ax2 = fig2.add_subplot(111)
    canvas2 = FigureCanvasTkAgg(fig2, master=frame_pie2)
    canvas2.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    table_sty = ttk.Style()
    table_sty.configure("Treeview", font=(DefaultFont, int(DefaultFontSize*1.2)), rowheight=25, background=color_map["PC"], foreground=color_map["BG"])
    table_sty.configure("Treeview.Heading", font=(DefaultFont, int(DefaultFontSize*1.4), "bold"), background=color_map["PC"], foreground=color_map["MC"])
    table_sty.map('Treeview', background=[('selected', color_map["MC"])])
    # 中容器表格
    frame_chart = tk.Frame(frame_middle, bg=color_map["TT"], background=color_map["MC"])
    frame_chart.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=5)

    sroll = tk.Scrollbar(frame_chart, orient="vertical")
    sroll.pack(side=tk.RIGHT, fill=tk.Y, padx=10)
    count_table = ttk.Treeview(frame_chart, column=('blockID', 'num', 'unit', 'ID'), height=7, yscrollcommand=sroll.set)
    sroll.config(command=count_table.yview)
    count_table.heading('blockID', text='名字', anchor="center")
    count_table.heading('num', text='数', anchor="e")
    count_table.heading('unit', text='量', anchor="w")
    count_table.heading('ID', text='ID', anchor="center")
    count_table.column("#0", width=10)
    count_table.column("blockID", width=150)
    count_table.column("num", width=40)
    count_table.column("unit", width=80, anchor="e")
    count_table.column("ID", width=200)
    count_table.config(height=20)
    count_table.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=10)

    # 统计数据容器
    frame_left = tk.Frame(litem, bg=color_map["BG"])
    hide(frame_left, DoStat, lambda: frame_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=10, pady=10))
    frame_3d = CTkFrame(frame_left, fg_color=color_map["PC"], corner_radius=DefaultCorner)
    frame_3d.pack(side=tk.TOP, fill=tk.BOTH, expand=False, padx=10, pady=0)
    frame_stati = CTkFrame(frame_left, fg_color=color_map["MC"], corner_radius=DefaultCorner)
    frame_stati.pack(side=tk.TOP, fill=tk.X, expand=False, padx=10, pady=30)
    frame_stati2 = tk.Frame(frame_stati, bg=color_map["MC"])
    frame_stati2.pack(fill=tk.BOTH, padx=20, pady=20)

    gl_view = OpenGLView(frame_3d, [((0, 0, 0), 'minecraft:dirt')], False, width=300, height=300, bg=color_map["PC"])
    gl_view.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    gl_view.after(1000, gl_view.redraw)
    stat_red = CTkFrame(frame_stati2, fg_color=color_map["PC"])
    stat_red.pack(fill=tk.BOTH, side=tk.TOP, padx=5, pady=5)
    stat_redt = CTkFrame(frame_stati2, fg_color=color_map["PC"])
    stat_redt.pack(fill=tk.BOTH, side=tk.TOP, padx=5, pady=5)
    stat_liq = CTkFrame(frame_stati2, fg_color=color_map["PC"])
    stat_liq.pack(fill=tk.BOTH, side=tk.TOP, padx=5, pady=5)
    stat_den = CTkFrame(frame_stati2, fg_color=color_map["PC"])
    stat_den.pack(fill=tk.BOTH, side=tk.TOP, padx=5, pady=5)
    stat_auth = CTkFrame(frame_stati2, fg_color=color_map["PC"])
    stat_auth.pack(fill=tk.BOTH, side=tk.TOP, padx=5, pady=5)
    stat_ver = CTkFrame(frame_stati2, fg_color=color_map["PC"])
    stat_ver.pack(fill=tk.BOTH, side=tk.TOP, padx=5, pady=5)
    stat_desc = CTkFrame(frame_stati2, fg_color=color_map["PC"])
    stat_desc.pack(fill=tk.BOTH, side=tk.TOP, padx=5, pady=5)
    tk.Label(stat_red, text="红石偏度", font=(DefaultFont, int(DefaultFontSize*1.6), "bold"), bg=color_map["PC"],fg=color_map["BG"]).pack(fill=tk.X, side=tk.LEFT, padx=5, pady=5)
    tk.Label(stat_redt, text="材质", font=(DefaultFont, int(DefaultFontSize*1.6), "bold"), bg=color_map["PC"], fg=color_map["BG"]).pack(fill=tk.X, side=tk.LEFT, padx=5, pady=5)
    tk.Label(stat_liq, text="液体偏度", font=(DefaultFont, int(DefaultFontSize*1.6), "bold"), bg=color_map["PC"],fg=color_map["BG"]).pack(fill=tk.X, side=tk.LEFT, padx=5, pady=5)
    tk.Label(stat_den, text="密度", font=(DefaultFont, int(DefaultFontSize*1.6), "bold"), bg=color_map["PC"], fg=color_map["BG"]).pack(fill=tk.X, side=tk.LEFT, padx=5, pady=5)
    tk.Label(stat_auth, text="作者", font=(DefaultFont, int(DefaultFontSize * 1.6), "bold"), bg=color_map["PC"],fg=color_map["BG"]).pack(fill=tk.X, side=tk.LEFT, padx=5, pady=5)
    tk.Label(stat_ver, text="版本", font=(DefaultFont, int(DefaultFontSize * 1.6), "bold"), bg=color_map["PC"],fg=color_map["BG"]).pack(fill=tk.X, side=tk.LEFT, padx=5, pady=5)
    tk.Label(stat_desc, text="简介", font=(DefaultFont, int(DefaultFontSize * 1.6), "bold"), bg=color_map["PC"],fg=color_map["BG"]).pack(fill=tk.X, side=tk.LEFT, padx=5, pady=5)
    a_red = tk.Label(stat_red, text="", font=(DefaultFont, int(DefaultFontSize*1.6)), bg=color_map["PC"], fg=color_map["MC"])
    a_red.pack(fill=tk.X, side=tk.RIGHT, padx=5, pady=5)
    a_redt = tk.Label(stat_redt, text="", font=(DefaultFont, int(DefaultFontSize*1.6)), bg=color_map["PC"], fg=color_map["MC"])
    a_redt.pack(fill=tk.X, side=tk.RIGHT, padx=5, pady=5)
    a_liq = tk.Label(stat_liq, text="", font=(DefaultFont, int(DefaultFontSize*1.6)), bg=color_map["PC"], fg=color_map["MC"])
    a_liq.pack(fill=tk.X, side=tk.RIGHT, padx=5, pady=5)
    a_den = tk.Label(stat_den, text="", font=(DefaultFont, int(DefaultFontSize*1.6)), bg=color_map["PC"], fg=color_map["MC"])
    a_den.pack(fill=tk.X, side=tk.RIGHT, padx=5, pady=5)
    a_auth = tk.Label(stat_auth, text="", font=(DefaultFont, int(DefaultFontSize*1.6)), bg=color_map["PC"], fg=color_map["MC"])
    a_auth.pack(fill=tk.X, side=tk.RIGHT, padx=5, pady=5)
    a_ver = tk.Label(stat_ver, text="", font=(DefaultFont, int(DefaultFontSize * 1.6)), bg=color_map["PC"],fg=color_map["MC"])
    a_ver.pack(fill=tk.X, side=tk.RIGHT, padx=5, pady=5)
    a_desc = tk.Label(stat_desc, font=(DefaultFont, int(DefaultFontSize * 1.6)), bg=color_map["PC"],fg=color_map["MC"], justify="left", wraplength=200)
    a_desc.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)


    litem.mainloop()



