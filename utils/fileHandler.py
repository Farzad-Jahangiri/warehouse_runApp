from pathlib import Path
import time
import os, stat,shutil, psutil
import subprocess
from subprocess import Popen
import json                 

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