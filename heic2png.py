import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image
import pillow_heif

def select_folder():
    root = tk.Tk()
    root.withdraw()  # ซ่อนหน้าต่างหลัก
    folder_selected = filedialog.askdirectory(title="เลือกโฟลเดอร์ที่มีไฟล์ HEIC",initialdir="./BeachGarbageDataset")
    return folder_selected

def convert_heic_to_png(folder_path):
    if not folder_path:
        print("ไม่ได้เลือกโฟลเดอร์")
        return
    
    #output_folder = os.path.join(folder_path, "converted_png")
    output_folder = folder_path # save to the same folder
    os.makedirs(output_folder, exist_ok=True)
    count_heic=0
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".heic"):
            heic_path = os.path.join(folder_path, filename)
            png_path = os.path.join(output_folder, os.path.splitext(filename)[0] + ".png")
            
            try:
                heif_file = pillow_heif.open_heif(heic_path)
                img = Image.frombytes(heif_file.mode, heif_file.size, heif_file.data, "raw", heif_file.mode, 0, 1)
                img.save(png_path, "PNG")
                print(f"แปลงไฟล์: {filename} -> {png_path}")
                count_heic += 1
            except Exception as e:
                print(f"เกิดข้อผิดพลาดในการแปลงไฟล์ {filename}: {e}")
    
    print(f'แปลงไฟล์สำเร็จ {count_heic} ภาพ')
    print("แปลงไฟล์เสร็จสิ้น!")

if __name__ == "__main__":
    folder = select_folder()
    convert_heic_to_png(folder)
