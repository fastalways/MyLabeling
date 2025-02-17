import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image

def select_folder():
    root = tk.Tk()
    root.withdraw()  # ซ่อนหน้าต่างหลัก
    folder_selected = filedialog.askdirectory(title="เลือกโฟลเดอร์ที่มีไฟล์ WebP",initialdir="./BeachGarbageDataset")
    return folder_selected

def convert_webp_to_png(folder_path):
    if not folder_path:
        print("ไม่ได้เลือกโฟลเดอร์")
        return
    print(f'Processing in:{folder_path}')
    #output_folder = os.path.join(folder_path, "converted_png")
    output_folder = folder_path # save to the same folder
    os.makedirs(output_folder, exist_ok=True)
    count_webp = 0
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".webp"):
            webp_path = os.path.join(folder_path, filename)
            png_path = os.path.join(output_folder, os.path.splitext(filename)[0] + ".png")
            print(f'{webp_path}')
            try:
                with Image.open(webp_path) as img:
                    img.save(png_path, "PNG")
                    count_webp+=1
                print(f"แปลงไฟล์: {filename} -> {png_path}")
            except Exception as e:
                print(f"เกิดข้อผิดพลาดในการแปลงไฟล์ {filename}: {e}")
            

    print(f'แปลงไฟล์สำเร็จ {count_webp} ภาพ')
    print("โปรแกรมทำการแปลงไฟล์WEBPเป็นPNGเสร็จสิ้น!")

if __name__ == "__main__":
    folder = select_folder()
    convert_webp_to_png(folder)
