from pathlib import Path
import time
import os, stat,shutil, psutil
import subprocess
from subprocess import Popen
import json                 
from config import TDATA_FOLDER_NAME

def save_file(name: str, value: str, base_path: str) -> None:
    path = Path(base_path)
    path.mkdir(parents=True, exist_ok=True)

    file_path = path / name
    print("file_path:", file_path)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(value)


def remove_readonly(fun, path, excinfo):
    os.chmod(path, stat.S_IWRITE)
    fun(path)

def save_json_file(name: str, data: dict, path: str):
    """
    name  -> اسم فایل (بدون .json)
    data  -> دیکشنری
    path  -> مسیر ذخیره
    """
    
    # اگر مسیر وجود نداشت بساز
    os.makedirs(path, exist_ok=True)
    
    # ساخت مسیر کامل فایل
    file_path = os.path.join(path, f"{name}.json")
    
    # ذخیره به صورت JSON
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    print(f"Saved successfully: {file_path}")



def delete_catch(path:str):
    try:
        emojiPath = path + fr"\tdata\emoji"
        user_dataPath = path + fr"\tdata\user_data"
        DebugLogsPath = path + fr"\DebugLogs"
        if os.path.exists(emojiPath):
            shutil.rmtree(emojiPath)
            print("Deleted.emoji")
        else:
            print(f"Folder does not exist: {emojiPath}")
        if os.path.exists(user_dataPath):
            shutil.rmtree(user_dataPath)
            print("Deleted.user_data")
        else:
            print(f"Folder does not exist: {user_dataPath}")
        if os.path.exists(DebugLogsPath):
            shutil.rmtree(DebugLogsPath)
            print("Deleted.DebugLogs")
        else:
            print(f"Folder does not exist: {DebugLogsPath}")
    except Exception as e:
        print('[Error delete_catch] ', e)


def copyBackupTdata(data):
    try:
        time.sleep(5)
        src = fr"C:\Shared\{TDATA_FOLDER_NAME}\{data.get('phone')}"
        dst = fr"D:\backup-reciver\{data.get('phone')}"
        shutil.copytree(src, dst, dirs_exist_ok=True)
        folder_path_emoji = fr"D:\backup-reciver\{data.get('phone')}\tdata\emoji"
        if os.path.exists(folder_path_emoji):
            shutil.rmtree(folder_path_emoji)
            print("Deleted.emoji")
        else:
            print("Folder does not exist.emoji")
        folder_path_user_data = fr"D:\backup-reciver\{data.get('phone')}\tdata\user_data"
        if os.path.exists(folder_path_user_data):
            shutil.rmtree(folder_path_user_data)
            print("Deleted.emoji")
        else:
            print("Folder does not exist.emoji")
        folder_path_DebugLogs = fr"D:\backup-reciver\{data.get('phone')}\DebugLogs"
        if os.path.exists(folder_path_DebugLogs):
            shutil.rmtree(folder_path_DebugLogs)
            print("Deleted.DebugLogs")
        else:
            print("Folder does not exist.DebugLogs")
        folder_path = fr"D:\backup-reciver\{data.get('phone')}"
        if os.path.exists(folder_path):
            for root, dirs, files in os.walk(folder_path):
                for f in files:
                    file_path = os.path.join(root, f)
                    try:
                        size = os.path.getsize(file_path)
                        if 600*1024 <= size <= 630*1024:
                            os.remove(file_path)
                            print("Deleted.611KB:", file_path)
                    except Exception as e:
                        print("Error:", file_path, e)
        else:
            print("Folder does not exist")
        targets = ["settingss", "countries", "shortcuts-custom.json", "shortcuts-default.json"]
        if os.path.exists(folder_path):
            for root, dirs, files in os.walk(folder_path):
                for f in files:
                    if f in targets:
                        file_path = os.path.join(root, f)
                        os.remove(file_path)
                        print(f"Deleted: {f}")
        else:
            print("Folder does not exist")
    except Exception as e:
        print("[Don't copy tdata to backup folder] ", e)
