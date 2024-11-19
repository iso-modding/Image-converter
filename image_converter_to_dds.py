import subprocess
import os
import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES
from tkinter import ttk  # For comboboxes
import webbrowser  # For opening URLs in the browser

IMAGEMAGICK_PATH = r"D:/Games/Modding/Software/conv_textures/convert.exe"
ALLOWED_SIZES = [64, 128, 256, 512, 1024, 2048]
ALLOWED_EXTENSIONS = ['.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.webp']  # Supported image formats

def convert_image_to_dds(input_image, output_dds, compression_type, mipmaps, width, height):
    if not os.path.isfile(input_image):
        print(f"Error: '{input_image}' does not exist.")
        return
    convert_command = [
        IMAGEMAGICK_PATH,
        input_image,
        "-resize", f"{width}x{height}!",
        "-define", f"dds:compression={compression_type}",
    ]
    if mipmaps:
        convert_command.extend(["-define", f"dds:mipmaps={mipmaps}"])
    convert_command.append(output_dds)
    try:
        subprocess.run(convert_command, check=True)
        print(f"Converted {input_image} to {output_dds}")
        status_label.config(text=f"Converted to {output_dds}")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        status_label.config(text="Error")

def on_drop(event, compression_type):
    input_file = event.data.strip('{}')
    file_extension = os.path.splitext(input_file)[1].lower()

    if file_extension in ALLOWED_EXTENSIONS:
        try:
            mipmaps = int(mipmap_entry.get())
        except ValueError:
            mipmaps = 0
        width = int(size_combobox_horizontal.get())
        height = int(size_combobox_vertical.get())
        output_dds = os.path.splitext(input_file)[0] + '.dds'
        convert_image_to_dds(input_file, output_dds, compression_type, mipmaps, width, height)
    else:
        status_label.config(text="Image file type not supported, see title.")

# Function to open the URL when clicked
def open_link(event):
    webbrowser.open("https://imagemagick.org/script/download.php")

root = TkinterDnD.Tk()
root.title("png / jpg / jpeg / bmp / gif / tiff / webp to DDS [isotonic on Discord]")
root.geometry("600x240")
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_columnconfigure(3, weight=1)
root.grid_columnconfigure(4, weight=1)
root.grid_columnconfigure(5, weight=1)

drag_frame = tk.Frame(root)
drag_frame.grid(row=0, column=0, columnspan=6, padx=10, pady=10)

drag_and_drop_area_a8r8g8b8 = tk.Label(drag_frame, text="A8R8G8B8 (large)", relief="solid", anchor="center", justify="center", bg="lightgray")
drag_and_drop_area_a8r8g8b8.grid(row=0, column=0, padx=10, pady=4)
drag_and_drop_area_bc1 = tk.Label(drag_frame, text="BC1", relief="solid", anchor="center", justify="center", bg="lightgray")
drag_and_drop_area_bc1.grid(row=0, column=1, padx=10, pady=4)
drag_and_drop_area_dxt5 = tk.Label(drag_frame, text="DXT5 (with Alpha)", relief="solid", anchor="center", justify="center", bg="lightgray")
drag_and_drop_area_dxt5.grid(row=0, column=2, padx=10, pady=4)
drag_and_drop_area_dxt1 = tk.Label(drag_frame, text="DXT1 (common)", relief="solid", anchor="center", justify="center", bg="lightyellow")
drag_and_drop_area_dxt1.grid(row=0, column=3, padx=10, pady=4)

window_width = root.winfo_width()
label_width = 20
for label in [drag_and_drop_area_a8r8g8b8, drag_and_drop_area_bc1, drag_and_drop_area_dxt1, drag_and_drop_area_dxt5]:
    label.config(width=16)
    label.config(height=2)

settings_frame = tk.Frame(root)
settings_frame.grid(row=1, column=0, columnspan=6, padx=10, pady=10)

mipmap_label = tk.Label(settings_frame, text="Mipmaps - Max 8", width=16)
mipmap_entry = tk.Entry(settings_frame, width=5)
mipmap_label.grid(row=0, column=0, padx=5, pady=5)
mipmap_entry.grid(row=0, column=1, padx=5, pady=5)

size_label_horizontal = tk.Label(settings_frame, text="Size X:", width=6)
size_combobox_horizontal = ttk.Combobox(settings_frame, values=ALLOWED_SIZES, state="readonly", width=8)
size_label_horizontal.grid(row=0, column=2, padx=5, pady=5)
size_combobox_horizontal.grid(row=0, column=3, padx=5, pady=5)
size_combobox_horizontal.set(512)  # Default to 512px

size_label_vertical = tk.Label(settings_frame, text="Size Y:", width=6)
size_combobox_vertical = ttk.Combobox(settings_frame, values=ALLOWED_SIZES, state="readonly", width=8)
size_label_vertical.grid(row=0, column=4, padx=5, pady=5)
size_combobox_vertical.grid(row=0, column=5, padx=5, pady=5)
size_combobox_vertical.set(512)

# Bind drag-and-drop for each compression format
drag_and_drop_area_a8r8g8b8.drop_target_register(DND_FILES)
drag_and_drop_area_a8r8g8b8.dnd_bind('<<Drop>>', lambda event: on_drop(event, "a8r8g8b8"))
drag_and_drop_area_bc1.drop_target_register(DND_FILES)
drag_and_drop_area_bc1.dnd_bind('<<Drop>>', lambda event: on_drop(event, "bc1"))
drag_and_drop_area_dxt5.drop_target_register(DND_FILES)
drag_and_drop_area_dxt5.dnd_bind('<<Drop>>', lambda event: on_drop(event, "dxt5"))
drag_and_drop_area_dxt1.drop_target_register(DND_FILES)
drag_and_drop_area_dxt1.dnd_bind('<<Drop>>', lambda event: on_drop(event, "dxt1"))

# Status label
status_label = tk.Label(root, text="Set mipmaps/size, default is 0 - 512x512, drag/drop one image at a time", width=80, height=2)
status_label.grid(row=2, column=0, columnspan=6, padx=20, pady=10)

# Add a clickable label to open the ImageMagick download page
link_label = tk.Label(root, text="ImageMagick/converter.exe is open source", fg="blue", cursor="hand2")
link_label.grid(row=3, column=0, columnspan=6, pady=10)
link_label.bind("<Button-1>", open_link)

root.mainloop()
