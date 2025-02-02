import tkinter as tk
from tkinter import filedialog, ttk
from litemapy import Schematic, Region, BlockState
from PIL import Image, ImageTk
from Litmatool import *
from Structure import *
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import importlib, webbrowser, os, codecs


your_module = importlib.import_module('litemapy')
YourClass = getattr(your_module, 'Region')
plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

APP_VERSION = '0.3.2'
file_path = ""
file_name = "litematica"
Block = {}
Cla_Block = {"实体": [], "羊毛": [], "陶瓦": [], "混凝土": [], "玻璃": [], "木制": [], "石质": [],
                     "其他岩石": [], "石英": [], "矿类": [], "砂土类": [], "末地类": [], "地狱类": [], "海晶类": [],
                     "粘土类": [], "红石":[], "铁类":[], "其他": []}
images = {}
color_map = [
    '#3399ff',  # 主色 浅蓝
    '#0066cc',  # 副色 深蓝
    '#f8f9fa',  # 背景
    '#343a40',  # 文字
]

def import_file():
    global file_path, file_name
    file_path = filedialog.askopenfilename(filetypes=[("Litematic File","*.litematic"),("All File","*.")])
    file_path = file_path.replace("\\", "/")
    file_name = file_path.split("/")[-1]
    label_middle.config(text=f"{file_name}")
    print(f"Imported file: {file_path}")

def hide(root):
    if root.winfo_ismapped():
        root.pack_forget()
    else:
        root.pack(side=tk.LEFT, fill=tk.Y)
        litem.update_idletasks()

def load_image(block_name):
    try:
        img_path = f"block/{block_name}.png"
        img = Image.open(img_path)
        img = img.resize((20, 20), Image.LANCZOS)
        img = ImageTk.PhotoImage(img)
        images[block_name] = img
        return img
    except:
        img_path = f"block/info_update.png"
        img = Image.open(img_path)
        img = img.resize((20, 20), Image.LANCZOS)
        img = ImageTk.PhotoImage(img)
        images[block_name] = img
        return img

def insert_table(block_state, count, simple_type):
    if isinstance(block_state, BlockState):
        block_id = block_state._BlockState__block_id
        properties = block_state._BlockState__properties
        block_name = block_id.split(":")[-1]
        if properties:
            properties_str = ", ".join([f"{k}={v}" for k, v in properties.items()])  # 格式化属性
        else:
            properties_str = ""
    else:
        block_id = block_state
        block_name = block_id.split(":")[-1]
        properties_str = block_name
    block_id_display = cn_translate(block_name) if simple_type else block_id
    img = load_image(block_name)
    count_table.insert('', 'end', image=img, values=(block_id_display, str(count), convert_units(count), properties_str))
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
    os.startfile(output_file_path)

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
            cla_bl[category]=total
    cat_other = sum(int(it[0]) for it in Cla_Block["其他"])
    Cla_Block.pop("其他")
    sorted_block = sorted(cla_bl.items(), key=lambda x: x[1], reverse=True)
    top_5 = sorted_block[:5]
    other_count = sum(count for _, count in sorted_block[5:])+cat_other
    labels2 = [cate for cate, _ in top_5]
    sizes2 = [count for _, count in top_5]
    if other_count > 0:
        labels2.append("其他")
        sizes2.append(other_count)
    ax2.pie(sizes2, labels=labels2, autopct='%1.1f%%', startangle=90)
    ax2.set_title("分类统计")

    canvas1.draw()
    canvas2.draw()



def start_analysis(simple_type):
    count_table.delete(*count_table.get_children())
    Block.clear()
    if not file_path:
        import_file()
    schematic = Schematic.load(file_path)
    print(f"Schematic loaded: {schematic}")
    for region_index, region in enumerate(schematic.regions.values()):
        print(f"Analyzing region {region_index + 1}")
        size_x = region.maxx() - region.minx() + 1
        size_y = region.maxy() - region.miny() + 1
        size_z = region.maxz() - region.minz() + 1
        num = 0
        for x in range(size_x):
            for y in range(size_y):
                for z in range(size_z):
                    block_state = region._Region__palette[region._Region__blocks[x, y, z]]
                    block_id = block_state._BlockState__block_id
                    if block_id not in ["minecraft:air", "minecraft:cave_air", "minecraft:void_air"]:
                        num += 1
                        if block_id not in ["minecraft:piston_head", "minecraft:bubble_column",
                                            "minecraft:nether_portal", "minecraft:moving_piston",
                                            "minecraft:bedrock"]:
                            output = block_id if simple_type else block_state
                            if output not in Block:
                                Block[output] = 1
                            else:
                                Block[output] += 1
        if DoEntity.get():
            for entity in region._Region__entities:
                entity_type = "E/" + str(entity.id)
                if entity_type not in ["E/minecraft:item", "E/minecraft:bat", "E/minecraft:experience_orb",
                                       "E/minecraft:shulker_bullet"]:
                    if entity_type not in Block:
                        Block[entity_type] = 1
                    else:
                        Block[entity_type] += 1
        time = 1 if entry_times.get() == "" else int(entry_times.get())
        for val in Block:
            id = val.split("[")[0].split(":")[-1]
            type = Category_Tran(id)
            if val.split("/")[0]=="E":
                Cla_Block["实体"].append((Block[val], val))
            elif type != "":
                Cla_Block[type].append((Block[val], val))
            else:
                Cla_Block["其他"].append((Block[val], val))
        Draw_Chart()
        label_bottom.config(
            text=f"Size体积: {size_x}x{size_y}x{size_z} | Number数量: {num} | Density密度: {num / (size_x * size_y * size_z) * 100:.2f}% | Times倍数: {time} | Types种类: {len(Block)}")
        numbers = [item[1] for item in list(Block.items())]
        print(numbers)
        stat=statistics(numbers)
        a_mean.config(text="{:.1f}".format(stat[0]))
        a_median.config(text=stat[1])
        a_mode.config(text=stat[2])
        a_range.config(text=stat[3])
        a_stddev.config(text="{:.2f}".format(stat[4]))
        a_stderr.config(text="{:.2f}".format(stat[5]))
        a_iqr.config(text="{:.2f}".format(stat[6]))
        a_ske.config(text="{:.2f}".format(stat[7]))
        a_ci.config(text=f"[{"{:.0f}".format(stat[8])},{"{:.0f}".format(stat[9])}]")


    sorted_block = sorted(Block.items(), key=lambda x: x[1], reverse=True)
    for index, (block_state, count) in enumerate(sorted_block):
        try:
            count = count * int(entry_times.get())
        except:
            count = count * 1
        insert_table(block_state, count, simple_type)

# Tkinter Setting
litem = tk.Tk()
litem.title(f"Litematica Viewer投影查看器 v{APP_VERSION}")
litem.geometry("1280x720")
litem.iconbitmap("icon.ico")
litem.configure(bg=color_map[2])
litem.attributes("-alpha", 0.9)

# MENU
menu = tk.Menu(litem)
DoEntity = tk.IntVar(value=1)
DoLifr = tk.IntVar(value=1)
DoStat = tk.IntVar(value=1)

menu_analysis = tk.Menu(menu, tearoff=0)
menu_analysis.add_command(label="Import导入", command=import_file, font=("Arial", 10))
menu_analysis.add_command(label="Output导出", command=lambda:output_data(False), font=("Arial", 10))
menu_analysis.add_command(label="ClassifiedOutput分类导出", command=lambda:output_data(True), font=("Arial", 10))
menu_analysis.add_command(label="SimpleAnalysis简洁分析", command=lambda:start_analysis(True), font=("Arial", 10))
menu_analysis.add_command(label="FullAnalysis全面分析", command=lambda:start_analysis(False), font=("Arial", 10))
menu.add_cascade(label="DataAnalysis数据分析", menu=menu_analysis, font=("Arial", 20))
menu_AnaSet = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Setting设置",menu=menu_AnaSet, font=("Arial", 20))
menu_AnaSet.add_checkbutton(label="DoAnalysisEntity是否分析实体",variable=DoEntity, font=("Arial", 10))
menu_AnaSet.add_checkbutton(label="ShowLithemPannel是否显示投影面板",variable=DoLifr,command=lambda:hide(frame_spawn), font=("Arial", 10))
menu_AnaSet.add_checkbutton(label="ShowStatisticsPannel是否显示统计面板",variable=DoStat,command=lambda:hide(frame_data), font=("Arial", 10))
menu_Help = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Help帮助",menu=menu_Help, font=("Arial", 20))
menu_Help.add_command(label="About关于", command=lambda:webbrowser.open("https://github.com/albertchen857/LitematicaViewer"), font=("Arial", 10))
menu_Help.add_command(label="AboutCreater关于作者", command=lambda:webbrowser.open("https://space.bilibili.com/3494373232741268"), font=("Arial", 10))
menu_Help.add_command(label="ManualInstallPackages手动更新软件库", command=manual_install_pk, font=("Arial", 10))

litem.config(menu=menu, padx=10, pady=10)
# 上容器
frame_top = tk.Frame(litem)
frame_top.configure(bg=color_map[1], bd=5)
frame_top.pack(side=tk.TOP, fill=tk.X)

btn_import = tk.Button(frame_top, text="Import导入", command=import_file, font=("Arial", 10))
btn_import.configure(bg=color_map[0],fg=color_map[3],relief='ridge')
btn_import.pack(side=tk.LEFT, padx=5, pady=5)
btn_simstart = tk.Button(frame_top, text="SIMPLE Analysis简洁分析", command=lambda:start_analysis(True), font=("Arial", 10))
btn_simstart.configure(bg=color_map[0],fg=color_map[3],relief='ridge')
btn_simstart.pack(side=tk.LEFT, padx=5, pady=5)

btn_github = tk.Button(frame_top, text="GitHub", command=lambda:webbrowser.open("https://github.com/albertchen857/LitematicaViewer"), font=("Arial", 10))
btn_github.configure(bg="black",fg=color_map[2],relief='groove')
btn_github.pack(side=tk.RIGHT, padx=5, pady=5)
btn_bilibili = tk.Button(frame_top, text="Bilibili", command=lambda:webbrowser.open("https://space.bilibili.com/3494373232741268"), font=("Arial", 10))
btn_bilibili.configure(bg="#FF6699", fg=color_map[2],relief='groove')
btn_bilibili.pack(side=tk.RIGHT, padx=5, pady=5)

# 中容器
frame_middle = tk.Frame(litem, bg=color_map[0])
frame_middle.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
# - 中容器顶部
frame_middle_top = tk.Frame(frame_middle, bg=color_map[0])
frame_middle_top.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

label_middle = tk.Label(frame_middle_top, text="LitematicaViewer投影查看器", font=("Helvetica", 30, 'bold'))
label_middle.configure(bg=color_map[0], fg=color_map[3], bd=5)
label_middle.pack(fill=tk.Y)

label_bottom = tk.Label(frame_middle_top, text="Size体积 | Number数量 | Density密度 | Times倍数 | Types种类", font=("Helvetica", 14, "bold"))
label_bottom.configure(bg=color_map[0], fg=color_map[2], bd=5)
label_bottom.pack(side=tk.LEFT, fill=tk.X, padx=20, pady=10)

frame_Times = tk.Frame(frame_middle_top, bg=color_map[0])
frame_Times.pack(side=tk.RIGHT, fill=tk.Y, padx=40)

label_times = tk.Label(frame_Times, text="Times倍数", font=("microsoft yahei ui", 16, "bold"))
label_times.configure(bg=color_map[0], fg=color_map[3])
label_times.pack(side=tk.LEFT, padx=5)

entry_times = tk.Entry(frame_Times, width=10, bg=color_map[2], fg=color_map[1], font=("Helvetica", 10))
entry_times.pack(side=tk.RIGHT, padx=5)
# - 中容器DEC
#frame_middle_dec = tk.Frame(frame_middle)
#frame_middle_dec.pack()
underscore1 = tk.Frame(frame_middle, bg=color_map[2])
underscore1.pack( padx=40, pady=10)

table_sty = ttk.Style()
table_sty.configure("Treeview", font=("Arial", 12), rowheight=25, background=color_map[1], foreground=color_map[2])
table_sty.configure("Treeview.Heading", font=("Helvetica", 14, "bold"), background=color_map[1], foreground=color_map[3])
table_sty.map('Treeview', background=[('selected', color_map[0])])
# 中容器表格
frame_chart = tk.Frame(frame_middle, bg=color_map[3])
frame_chart.configure(background=color_map[0])
frame_chart.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=5)

sroll = tk.Scrollbar(frame_chart, orient="vertical")
sroll.pack(side=tk.RIGHT, fill=tk.Y, padx=10)
count_table = ttk.Treeview(frame_chart, column=('blockID', 'num', 'unit', 'properties'), height=7, yscrollcommand=sroll.set)
sroll.config(command=count_table.yview)
count_table.heading('blockID', text='ID/名字', anchor="center")
count_table.heading('num', text='Num数量', anchor="center")
count_table.heading('unit', text='Unit单位数', anchor="center")
count_table.heading('properties', text='Prop属性', anchor="center")
count_table.column("#0", width=2, anchor="e")
count_table.column("blockID", width=150)
count_table.column("num", width=50)
count_table.column("unit", width=50)
count_table.column("properties", width=200)
count_table.config(height=20)
count_table.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=10)
#统计容器
frame_data = tk.Frame(frame_chart, bg=color_map[1])
frame_data.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

frame_pie1 = tk.Frame(frame_data, bg=color_map[1])
frame_pie1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=5)
frame_pie2 = tk.Frame(frame_data, bg=color_map[1])
frame_pie2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=5)
frame_stati = tk.Frame(frame_data, bg=color_map[1])
frame_stati.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=5)

fig1 = Figure(figsize=(4, 3), dpi=100)
ax1 = fig1.add_subplot(111)
canvas1 = FigureCanvasTkAgg(fig1, master=frame_pie1)
canvas1.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

fig2 = Figure(figsize=(4, 3), dpi=100)
ax2 = fig2.add_subplot(111)
canvas2 = FigureCanvasTkAgg(fig2, master=frame_pie2)
canvas2.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

l_st = tk.Label(frame_stati, text="数据统计", font=("Arial", 16, "bold"), bg=color_map[0], fg=color_map[3])
l_st.grid(row=0, column=0, padx=2, pady=5, columnspan=6)
l_mean = tk.Label(frame_stati, text="均值", font=("Arial", 12, "bold"), bg=color_map[0], fg=color_map[3])
l_mean.grid(row=1, column=0, padx=2, pady=5)
l_median = tk.Label(frame_stati, text="中位数", font=("Arial", 12, "bold"), bg=color_map[0], fg=color_map[3])
l_median.grid(row=1, column=2, padx=2, pady=5)
l_mode = tk.Label(frame_stati, text="众数", font=("Arial", 12, "bold"), bg=color_map[0], fg=color_map[3])
l_mode.grid(row=1, column=4, padx=2, pady=5)
l_range = tk.Label(frame_stati, text="极差", font=("Arial", 12, "bold"), bg=color_map[0], fg=color_map[3])
l_range.grid(row=2, column=0, padx=2, pady=5)
l_stddev = tk.Label(frame_stati, text="标准差", font=("Arial", 12, "bold"), bg=color_map[0], fg=color_map[3])
l_stddev.grid(row=2, column=2, padx=2, pady=5)
l_stderr = tk.Label(frame_stati, text="标准误差", font=("Arial", 12, "bold"), bg=color_map[0], fg=color_map[3])
l_stderr.grid(row=2, column=4, padx=2, pady=5)
l_iqr = tk.Label(frame_stati, text="四分位距", font=("Arial", 12, "bold"), bg=color_map[0], fg=color_map[3])
l_iqr.grid(row=3, column=0, padx=2, pady=5)
l_ske = tk.Label(frame_stati, text="偏度", font=("Arial", 12, "bold"), bg=color_map[0], fg=color_map[3])
l_ske.grid(row=3, column=2, padx=2, pady=5)
l_ci = tk.Label(frame_stati, text="置信区间", font=("Arial", 12, "bold"), bg=color_map[0], fg=color_map[3])
l_ci.grid(row=3, column=4, padx=2, pady=5)

a_mean = tk.Label(frame_stati, text="0", font=("Arial", 12), bg=color_map[1], fg=color_map[2])
a_mean.grid(row=1, column=1, padx=5, pady=5)
a_median = tk.Label(frame_stati, text="0", font=("Arial", 12), bg=color_map[1], fg=color_map[2])
a_median.grid(row=1, column=3, padx=5, pady=5)
a_mode = tk.Label(frame_stati, text="0", font=("Arial", 12), bg=color_map[1], fg=color_map[2])
a_mode.grid(row=1, column=5, padx=5, pady=5)
a_range = tk.Label(frame_stati, text="0", font=("Arial", 12), bg=color_map[1], fg=color_map[2])
a_range.grid(row=2, column=1, padx=5, pady=5)
a_stddev = tk.Label(frame_stati, text="0", font=("Arial", 12), bg=color_map[1], fg=color_map[2])
a_stddev.grid(row=2, column=3, padx=5, pady=5)
a_stderr = tk.Label(frame_stati, text="0", font=("Arial", 12), bg=color_map[1], fg=color_map[2])
a_stderr.grid(row=2, column=5, padx=5, pady=5)
a_iqr = tk.Label(frame_stati, text="0", font=("Arial", 12), bg=color_map[1], fg=color_map[2])
a_iqr.grid(row=3, column=1, padx=5, pady=5)
a_ske = tk.Label(frame_stati, text="0", font=("Arial", 12), bg=color_map[1], fg=color_map[2])
a_ske.grid(row=3, column=3, padx=5, pady=5)
a_ci = tk.Label(frame_stati, text="[0,0]", font=("Arial", 12), bg=color_map[1], fg=color_map[2])
a_ci.grid(row=3, column=5, padx=5, pady=5)

# lith容器
frame_spawn = tk.Frame(litem, bg=color_map[1])
hide(frame_spawn)
# - 右容器上部：frame_spawn_new
frame_spawn_new = tk.Frame(frame_spawn, bg=color_map[0])
frame_spawn_new.pack(side=tk.TOP, fill=tk.X,  padx=20)
frame_new_title = tk.Label(frame_spawn_new, text="生成图形投影", font=("Arial", 18), bg=color_map[0], fg=color_map[3])
frame_new_title.grid(row=0, column=0, padx=5, pady=5, columnspan=4)
# -- ID 输入框
label_id = tk.Label(frame_spawn_new, text="ID", font=("Arial", 12), bg=color_map[0], fg=color_map[3])
label_id.grid(row=1, column=0, padx=5, pady=5)
entry_id = tk.Entry(frame_spawn_new, width=20, bg=color_map[2], fg=color_map[1], font=("Arial", 10))
entry_id.grid(row=1, column=1, padx=5, pady=5, columnspan=3)
# -- XYZ 长宽高输入框
label_xyz = tk.Label(frame_spawn_new, text="X,Y,Z", font=("Arial", 12), bg=color_map[0], fg=color_map[3])
label_xyz.grid(row=2, column=0, padx=5, pady=5)
label_lwh = tk.Label(frame_spawn_new, text="长,宽,高", font=("Arial", 12), bg=color_map[0], fg=color_map[3])
label_lwh.grid(row=3, column=0, padx=5, pady=5)
entry_x = tk.Entry(frame_spawn_new, width=5, bg=color_map[2], fg=color_map[1], font=("Arial", 10))
entry_x.grid(row=2, column=1, padx=2, pady=5)
entry_y = tk.Entry(frame_spawn_new, width=5, bg=color_map[2], fg=color_map[1], font=("Arial", 10))
entry_y.grid(row=2, column=2, padx=2, pady=5)
entry_z = tk.Entry(frame_spawn_new, width=5, bg=color_map[2], fg=color_map[1], font=("Arial", 10))
entry_z.grid(row=2, column=3, padx=2, pady=5)
entry_length = tk.Entry(frame_spawn_new, width=5, bg=color_map[2], fg=color_map[1], font=("Arial", 10))
entry_length.grid(row=3, column=1, padx=2, pady=5)
entry_width = tk.Entry(frame_spawn_new, width=5, bg=color_map[2], fg=color_map[1], font=("Arial", 10))
entry_width.grid(row=3, column=2, padx=2, pady=5)
entry_height = tk.Entry(frame_spawn_new, width=5, bg=color_map[2], fg=color_map[1], font=("Arial", 10))
entry_height.grid(row=3, column=3, padx=2, pady=5)
# -- Hollow 单选框和 Thickness 输入框
chollow = tk.BooleanVar()
lable_thickness = tk.Label(frame_spawn_new, text="Thickness", font=("Arial", 12), bg=color_map[0], fg=color_map[3])
lable_thickness.grid(row=4, column=0, padx=5, pady=5)
entry_thickness = tk.Entry(frame_spawn_new, width=13, bg=color_map[2], fg=color_map[1], font=("Arial", 10))
entry_thickness.grid(row=4, column=1, padx=5, pady=5, columnspan=2)
check_hollow = tk.Checkbutton(frame_spawn_new, text="Hollow", variable=chollow, bg=color_map[0], fg=color_map[3], font=("Arial", 10))
check_hollow.grid(row=5, column=0, padx=5, pady=5)
# -- 上下左右前后复选框
cu = tk.BooleanVar()
cd = tk.BooleanVar()
cl = tk.BooleanVar()
cr = tk.BooleanVar()
cf = tk.BooleanVar()
cb = tk.BooleanVar()
check_up = tk.Checkbutton(frame_spawn_new, text="上", bg=color_map[0], fg=color_map[3], font=("Arial", 10), variable=cu)
check_up.grid(row=5, column=1, padx=2, pady=2)
check_down = tk.Checkbutton(frame_spawn_new, text="下", bg=color_map[0], fg=color_map[3], font=("Arial", 10), variable=cd)
check_down.grid(row=5, column=2, padx=2, pady=2)
check_left = tk.Checkbutton(frame_spawn_new, text="左", bg=color_map[0], fg=color_map[3], font=("Arial", 10), variable=cl)
check_left.grid(row=5, column=3, padx=2, pady=2)
check_right = tk.Checkbutton(frame_spawn_new, text="右", bg=color_map[0], fg=color_map[3], font=("Arial", 10), variable=cr)
check_right.grid(row=6, column=1, padx=2, pady=2)
check_front = tk.Checkbutton(frame_spawn_new, text="前", bg=color_map[0], fg=color_map[3], font=("Arial", 10), variable=cf)
check_front.grid(row=6, column=2, padx=2, pady=2)
check_back = tk.Checkbutton(frame_spawn_new, text="后", bg=color_map[0], fg=color_map[3], font=("Arial", 10), variable=cb)
check_back.grid(row=6, column=3, padx=2, pady=2)

label_spawn = tk.Label(frame_spawn_new, text="FileName", font=("Arial", 12), bg=color_map[0], fg=color_map[3])
label_spawn.grid(row=7, column=0, padx=5, pady=5)
entry_spawn = tk.Entry(frame_spawn_new, width=20, bg=color_map[2], fg=color_map[1], font=("Arial", 10))
entry_spawn.grid(row=7, column=1, columnspan=3,padx=2, pady=2)

x,y,z = entry_x.get(),entry_y.get(),entry_z.get()
l,w,h = entry_length.get(),entry_width.get(),entry_height.get()
btn_spawn = tk.Button(frame_spawn_new, text="Spawn生成", font=("Arial", 10, "bold"),
                      command=lambda : create_structure(entry_spawn.get(),entry_id.get(),
                                                        (x,y,z) if x and y and z else (0,0,0),
                                                        (l,w,h) if l and w and h else (0,0,0),
                                                        chollow, entry_thickness.get(),
                                                        [cu,cd,cl,cr,cf,cb]))
btn_spawn.configure(bg=color_map[2], fg=color_map[0], relief='ridge')
btn_spawn.grid(row=8, column=0, padx=2, pady=2, columnspan=2)

# - 右容器下部：frame_spawn_change
frame_spawn_change = tk.Frame(frame_spawn, bg=color_map[0])
frame_spawn_change.pack(side=tk.TOP, fill=tk.X, pady=10, padx=20)
frame_change_title = tk.Label(frame_spawn_change, text="替换特定方块", font=("Arial", 18), bg=color_map[0],fg=color_map[3])
frame_change_title.grid(row=0, column=0, padx=5, pady=20, columnspan=4)

# -- Limit 标签和 XYZ 输入框
label_limit = tk.Label(frame_spawn_change, text="Limit", font=("Arial", 12), bg=color_map[0], fg=color_map[3])
label_limit.grid(row=1, column=0, padx=5, pady=5)
entry_limit_x = tk.Entry(frame_spawn_change, width=5, bg=color_map[2], fg=color_map[1], font=("Arial", 10))
entry_limit_x.grid(row=1, column=1, padx=2, pady=5)
entry_limit_y = tk.Entry(frame_spawn_change, width=5, bg=color_map[2], fg=color_map[1], font=("Arial", 10))
entry_limit_y.grid(row=1, column=2, padx=2, pady=5)
entry_limit_z = tk.Entry(frame_spawn_change, width=5, bg=color_map[2], fg=color_map[1], font=("Arial", 10))
entry_limit_z.grid(row=1, column=3, padx=2, pady=5)

# -- Change 标签和多行输入框
label_change = tk.Label(frame_spawn_change, text="Change", font=("Arial", 12), bg=color_map[0], fg=color_map[3])
label_change.grid(row=2, column=0, padx=5, pady=5)
text_change = tk.Text(frame_spawn_change,width=20, height=5, bg=color_map[2], fg=color_map[1], font=("Arial", 10))
text_change.grid(row=2, column=1, columnspan=3, padx=5, pady=5)

label_spawn2 = tk.Label(frame_spawn_change, text="FileName", font=("Arial", 12), bg=color_map[0], fg=color_map[3])
label_spawn2.grid(row=3, column=0, padx=5, pady=5)
entry_spawn2 = tk.Entry(frame_spawn_change, width=20, bg=color_map[2], fg=color_map[1], font=("Arial", 10))
entry_spawn2.grid(row=3, column=1, columnspan=3,padx=2, pady=2)

btn_spawn2 = tk.Button(frame_spawn_change, text="Spawn生成", font=("Arial", 10, "bold"))
btn_spawn2.configure(bg=color_map[2], fg=color_map[0], relief='ridge')
btn_spawn2.grid(row=4, column=0, padx=2, pady=2, columnspan=2)

litem.mainloop()

