import litemapy as litema
import tkinter as tk


def create_structure(file_name, block_id, start_coords, dimensions, hollow, wall_thickness, faces):
    schematic = litema.Schematic(shape=dimensions)

    cx, cy, cz = start_coords
    length, width, height = dimensions

    for x in range(cx,length):
        for y in range(int(cy),height):
            for z in range(int(cz),width):
                if ((faces[0] and z < wall_thickness)or
                    (faces[1] and z >= width - wall_thickness)or
                    (faces[2] and x < wall_thickness)or
                    (faces[3] and x >= length - wall_thickness)or
                    (faces[4] and y < wall_thickness)or
                    (faces[5] and y >= height - wall_thickness)):  # 前面
                    is_on_face = True
                else:
                    is_on_face = False

                if hollow:
                    if is_on_face:
                        schematic.setblock(x, y, z, block_id)
                else:
                    # 如果不是空心，直接放置方块
                    schematic.setblock(x, y, z, block_id)

    file_path = tk.filedialog.asksaveasfilename(defaultextension=".litematic", filetypes=[("Litematic File","*.litematic"),("All File","*.")],
                                                       title="Litematica Structure File Save As",
                                                       initialfile=f"{file_name}.litematic")
    print(file_path)
    if not file_path:
        return schematic
    schematic.save(file_path)
    return schematic
