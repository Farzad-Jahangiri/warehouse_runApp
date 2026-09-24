import subprocess, time, os, json
from subprocess import Popen
from typing import List, TypedDict
import random
from datetime import datetime
# import logging
import psutil
import threading, time
#database
#config
#utils
from utils.fileHandler import delete_catch
#database
#--------------file-----------------
from utils.fileHandler import save_json_file
#--------------service-----------------
# from service.update_data import updateState
#--------------utils-----------------
from utils.phone import split_phone_number
#--------------config----------------
from bot.config.states import intro_phone
from bot.config.deviseAndsystemVertion import deviceModel, systemVersion
from config import TDATA_FOLDER_NAME, DEFAULT_PATH_TDATA
# from database import workscript
from customType.userTypes import UserData
#=================kill app==============
from database.oneScriptDb import get_connection

import hashlib

worker_id = int(input("Worker number: "))

#==============================================
# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s | %(levelname)s | %(message)s",
#     handlers=[
#         logging.FileHandler("runAppBot.log", encoding="utf-8"),
#         logging.StreamHandler()
#     ]
# )
#===============================================



def update_workscript_by_chat_id(
    chat_id,
    callbackquery_id=None,
    pid=None, 
    message_id=None,
    is_closed=None,
    isRunApp=None,
    state=None,
    updateAt=False,
    app_verssion = None,
    appversionStr= None,
    deviceModel = None,
    systemVersion = None,
    api_id = None,
    api_hash= None,
    selected = None,
    _worker_id = None
):
    conn = get_connection()
    if not conn:
        return False

    try:
        fields = []
        values = []

        if callbackquery_id is not None:
            fields.append("callbackquery_id = %s")
            values.append(callbackquery_id)


        if pid is not None:
            fields.append("pid = %s")
            values.append(pid)
        if message_id is not None:
            fields.append("message_id = %s")
            values.append(message_id)

        if is_closed is not None:
            fields.append("is_closed = %s")
            values.append(is_closed)
        if isRunApp is not None:
            fields.append("isRunApp = %s")
            values.append(isRunApp)
        if selected is not None:
            fields.append("selected = %s")
            values.append(isRunApp)
        if state is not None:
            fields.append("state = %s")
            values.append(state)
        if updateAt:
            fields.append("updatedAt = NOW()")
        if app_verssion:
            fields.append("appVersion = %s")
            values.append(app_verssion)
        if appversionStr:
            fields.append("appVersionStr = %s")
            values.append(appversionStr)
        if deviceModel:
            fields.append("deviceModel = %s")
            values.append(deviceModel)
        if systemVersion:
            fields.append("systemVersion = %s")
            values.append(systemVersion)
        if api_id:
            fields.append("api_id = %s")
            values.append(api_id)
        if api_hash:
            fields.append("api_hash = %s")
            values.append(api_hash)
        if _worker_id:
            fields.append("worker_id = %s")
            values.append(0)

        # اگر هیچ فیلدی برای آپدیت نبود
        if not fields:
            return False

        values.append(chat_id)

        query = f"""
            UPDATE user
            SET {', '.join(fields)}
            WHERE chat_id = %s;
        """

        with conn.cursor() as cursor:
            cursor.execute(query, values)
            return cursor.rowcount > 0  # آیا واقعاً آپدیت شد؟

    except Exception as e:
        print(f"[DB ERROR] update_workscript_by_chat_id: {e}")
        return False

    finally:
        conn.close()


def fetch_record_by_runApp(runApp=True):
    conn = get_connection()
    if not conn:
        print("[Error] not connection database (fetch_record_by_state)")
        return None
    try:
        with conn.cursor() as cursor:
            sql = """
                SELECT id, chat_id, `pass` AS password, api_id, api_hash, state, code, message, deviceModel, systemVersion,
                 lang, createdAt, updatedAt, isRunApp FROM user WHERE isRunApp = %s
            """
            
            cursor.execute(sql, (runApp,))
            record: List[UserData] | None = cursor.fetchall()
            if not record:
                return None
            return record

    except Exception as e:
        print(f"[DB ERROR] fetch_record_by_state: {e}")
        return None

    finally:
        if conn:
            conn.close()





def generate_version(hash_value: str):
    # تبدیل هش به عدد
    num = int(hashlib.sha256(hash_value.encode()).hexdigest(), 16)

    # ساخت version parts
    major = (num % 9) + 1
    minor = (num // 10 % 9) + 1
    patch = (num // 100 % 9) + 1

    # version number مثل 6006002
    version_number = major * 1000000 + minor * 1000 + patch

    # version string مثل "6.6.2"
    version_string = f"{major}.{minor}.{patch}"

    return version_number, version_string


class appType(TypedDict):
    name:int
    status:bool
    created:datetime
    process:Popen
    pid:int
    phone: str

appData:List[appType] = []
baseFolder = TDATA_FOLDER_NAME

# def run_telegram(index: int) -> subprocess.Popen:
#     path = fr"baseApp\login-app-{index}\Telegram.exe"
#     process = subprocess.Popen(path)
#     return process

def run_telegram(workpath: str) -> subprocess.Popen:
    process = subprocess.Popen([
        fr".\baseApps\login\Telegram.exe",
        "-workdir",
        workpath
    ])
    return process


def get_free_index(appData, max_index=20):
    used = {app['name'] for app in appData}
    for i in range(1, max_index + 1):
        if i not in used:
            return i
    return None

def fetch_record_by_state(state, worker_id):
    conn = get_connection()
    if not conn:
        print("[Error] not connection database (fetch_record_by_state)")
        return None
    try:
        with conn.cursor() as cursor:
            sql = """
                SELECT id, phone, chat_id, `pass` AS password, api_id, api_hash, state, code, message, deviceModel, systemVersion,
                 lang, createdAt, updatedAt FROM user WHERE state = %s AND worker_id = %s
            """
            
            cursor.execute(sql, (state, worker_id))
            record = cursor.fetchall()
            if not record:
                conn.commit()
                return None
            # ids = [row['id'] for row in record]

            # # 2️⃣ آپدیت همان ردیف‌ها
            # placeholders = ",".join(["%s"] * len(ids))
            # cursor.execute(f"""
            #     UPDATE user
            #     SET selected = true
            #     WHERE id IN ({placeholders})
            # """, ids)
            # conn.commit()

            return record

    except Exception as e:
        print(f"[DB ERROR] fetch_record_by_state: {e}")
        return None

    finally:
        if conn:
            conn.close()




def kill_telegram(pid: int, phone, chat_id, worker_id=0) -> None:
    try:
        print(f"Killing PID {pid}")
        if pid != 0 and psutil.pid_exists(pid):
            psutil.Process(pid).kill()
            delete_catch(fr'{DEFAULT_PATH_TDATA}\{phone}')
            conn = get_connection()
            if conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                                    UPDATE workers
                                    SET count = CASE 
                                        WHEN count > 0 THEN count - 1
                                        ELSE 0
                                    END
                                    WHERE id = %s
                            """,(worker_id))
                conn.close()
        update_workscript_by_chat_id(chat_id, is_closed=False, isRunApp=False, selected = False)
        
    except Exception as e:
        print("Error to kill app: ", e)

def get_all_workscripts(worker_id):
    conn = get_connection()
    if not conn:
        return []

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT *
                FROM user
                WHERE (is_closed = TRUE
                OR updatedAt <= NOW() - INTERVAL 2 MINUTE) AND worker_id = %s;
            """, (worker_id,))
            records = cursor.fetchall()
            return records  # لیست دیکشنری‌ها

    except Exception as e:
        print(f"[DB ERROR] get_all_workscripts: {e}")
        return []

    finally:
        conn.close()

def kill_app(worker_id, max_age_seconds: int = 120):
    try:
        appList = get_all_workscripts(worker_id)
        killIndex = 0
        runIndex = 0
        for app in appList:
            chat_id = app.get("chat_id")
            pid = app.get('pId')
            is_closed = app.get('is_closed')
            isRunApp = app.get('isRunApp')
            phone = app.get('phone')
            if is_closed:
                if pid:
                    threading.Thread(target=kill_telegram, args=(int(pid), phone, chat_id, worker_id), daemon=True).start()
                    # kill_telegram(int(pid), phone, chat_id)
                else:
                    update_workscript_by_chat_id(chat_id, is_closed=False, isRunApp=False)
            elif isRunApp:
                if pid:
                    threading.Thread(target=kill_telegram, args=(int(pid), phone, chat_id,worker_id), daemon=True).start()
                    # kill_telegram(int(pid), phone, chat_id)
                else:
                    update_workscript_by_chat_id(chat_id, is_closed=False, isRunApp=False)
            
            killIndex += 1
        works = fetch_record_by_runApp(True)
        if works:
            runIndex = len(works)

        allIndex = runIndex - killIndex
        return allIndex if allIndex > 0 else 0
            
    except Exception as e:
        print("Error on Kill app:", e)
        return 0


def main():
    global appData
    
    
 

    while True:
        try:
            countList = kill_app(worker_id=worker_id)
            if countList >= 20:
                print("⚠️ Reached max apps, waiting for cleanup")
                continue
            records = fetch_record_by_state(intro_phone, worker_id)
            
            if records:
                conn = get_connection()
                apiData = {}
                isSetProxy = False
                proxyData = {}
                # import pdb;pdb.set_trace()
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM runscript WHERE id = 1")
                    runscriptData = cursor.fetchone()
                    isSetProxy = bool(int(runscriptData['proxy']))
                
                for record in records:
                    code, phone = split_phone_number(f'+{record.get('phone')}')
                    
                    with conn.cursor() as cursor:
                        if isSetProxy:
                            cursor.execute("SELECT * FROM proxy ORDER BY updated_at ASC LIMIT 1 FOR UPDATE")
                            proxyData = cursor.fetchone()
                            cursor.execute("""
                                    UPDATE proxy
                                    SET updated_at = NOW()
                                    WHERE id = %s
                                """, (proxyData['id'],))
                        cursor.execute("""
                            SELECT *
                            FROM telegram_accounts_hash 
                            WHERE login_count < 300 
                            AND selected = 0
                            AND api_id != 2040
                            AND os_hash = %s
                            ORDER BY login_count ASC
                            LIMIT 1
                            FOR UPDATE
                        """,("Desktop",))
                        apiData = cursor.fetchone()
                        
                        cursor.execute("""
                            UPDATE telegram_accounts_hash
                            SET selected = 1
                            WHERE id = %s
                        """, (apiData['id'],))
                        conn.commit()
                    
                    
                    path = fr"{DEFAULT_PATH_TDATA}\{str(code)+str(phone)}"
                    dmList = deviceModel.copy()
                    smList = systemVersion.copy()
                    proxyIp = ''
                    proxyPort = 0
                    proxyUsername = ''
                    proxyPassword = ''
                    if isSetProxy:
                        myProxy = proxyData
                        proxyIp = myProxy['ip']
                        proxyPort = int(myProxy['port'])
                        proxyUsername = myProxy['username'] if bool(myProxy['username']) else ""
                        proxyPassword = myProxy['password'] if bool(myProxy['password']) else ""
                        # with conn.cursor() as cursor:
                        #     cursor.execute("SELECT code FROM proxy_country WHERE code = %s", (int(code),))
                        #     rw = cursor.fetchone()
                        #     if bool(rw):
                        #         myProxy = random.choice(proxyData)
                        #         proxyIp = myProxy['ip']
                        #         proxyPort = int(myProxy['port'])
                        #         proxyUsername = myProxy['username'] if bool(myProxy['username']) else ""
                        #         proxyPassword = myProxy['password'] if bool(myProxy['password']) else ""
                    # for not proxy
                    if code in ['880']:
                        isSetProxy = False
                        proxyIp = ""
                        proxyPort = 0
                        proxyUsername = ""
                        proxyPassword = ""

                    random.shuffle(dmList)
                    random.shuffle(smList)
                    dm = random.choice(dmList)
                    sv = random.choice(smList)
                    apiId = int(apiData['api_id'])
                    apiHash = apiData["api_hash"]
                    appVersion, appVersionStr = generate_version(apiHash)
                    # if code in ['880', '20', '84', '244', '254', '213', '227', '232', '977', '62']:
                    if code in ['']:
                        apiId = 2040
                        apiHash = 'b18441a1ff607e10a989891a5462e627'
                        appVersion = 6006002
                        appVersionStr = '6.6.2'

                    # if code in ['91', '62', '63', '98']:
                    #     apis = [
                    #         {'id': 32453292, 'hash': '9c273745e1652b330ca57acfbad78f14'},
                    #         {'id': 23156505, 'hash': 'cbdff065c83914d5beea9b4b711ba31e'},
                    #         {'id': 38189779, 'hash': '5bb8e3d54b7e314299e1f8ff95b14034'},
                    #         {'id': 25995819, 'hash': 'a29ce871cf33ba96b46d2db80500a6fe'},
                    #         {'id': 35224834, 'hash': 'aab77549f017fd7023ca280e12a84cf0'},
                    #         {'id': 29578308, 'hash': '436e751ff1fdd320eb94e16f969fdea3'},
                    #         {'id': 36169979, 'hash': '032601b4845a6c4a2ad532539a5a931f'},
                    #         {'id': 33159952, 'hash': 'a12cdb8e3201435f7b7b40929a0dea39'},
                    #         {'id': 32053838, 'hash': '8702a468c600acab4b4a4f91fb2dc1df'},
                    #         {'id': 34385640, 'hash': '689ecea2ac7f7c8ad57472c65b2abe7c'}
                    #     ]
                    #     models = [
                    #         "Samsung SM-S918B",        # Galaxy S23 Ultra
                    #         "Samsung SM-S911B",        # Galaxy S23
                    #         "Samsung SM-S921B",        # Galaxy S24
                    #         "Samsung SM-G998B",        # Galaxy S21 Ultra
                    #         "Google Pixel 8 Pro",
                    #         "Google Pixel 7 Pro",
                    #         "Xiaomi 13 Pro",
                    #         "Xiaomi 14",
                    #         "OnePlus 12",
                    #         "Huawei P60 Pro"
                    #     ]
                    #     system = [
                    #         "SDK 21",  # Android 5.0
                    #         "SDK 22",  # Android 5.1
                    #         "SDK 23",  # Android 6.0
                    #         "SDK 24",  # Android 7.0
                    #         "SDK 25",  # Android 7.1
                    #         "SDK 26",  # Android 8.0
                    #         "SDK 27",  # Android 8.1
                    #         "SDK 28",  # Android 9
                    #         "SDK 29",  # Android 10
                    #         "SDK 30",  # Android 11
                    #         "SDK 31",  # Android 12
                    #         "SDK 32",  # Android 12L
                    #         "SDK 33",  # Android 13
                    #         "SDK 34",  # Android 14
                    #         "SDK 35",  # Android 15
                    #         "SDK 36",  # Android 16
                    #     ]
                    #     dm = random.choice(models)
                    #     sv = random.choice(system)
                    #     apisSelected = random.choice(apis)
                    #     apiId = apisSelected['id']
                    #     apiHash = apisSelected['hash']
                    
                    loginConfig = {
                        "phoneNumber": str(phone),
                        "chatId": str(record.get('chat_id')),
                        "prefix": str(code),
                        "isSetProxy": isSetProxy,
                        "proxyIp": proxyIp,
                        "proxyPassword": proxyPassword,
                        "proxyPort": proxyPort,
                        "proxyUsername": proxyUsername,
                        "deviceModel": dm,
                        "systemVersion": sv,
                        "errorUrl": "http://127.0.0.1:9000/tg/intro_error/",
                        "introCodeUrl": "http://127.0.0.1:9000/tg/intro_code/",
                        "introPasswordUrl": "http://127.0.0.1:9000/tg/intro_password/",
                        "passwordSetUrl": "http://127.0.0.1:9000/tg/new_password_set/",
                        "frozenAccountUrl": "http://127.0.0.1:9000/tg/frozen_account/",
                        "pass": "",
                        "tdataPath": baseFolder,
                        "isDefaultPassword": True,
                        "apiId": apiId,
                        "apiHash": apiHash,
                    }
                    apiConfig = {
                        "apiId": apiId,
                        "apiHash": apiHash,
                        "deviceModel": dm,
                        "systemVersion": sv,
                        "tdataPath": baseFolder,
                        "appVersion": appVersion,
                        "appVersionStr": appVersionStr,
                        "lang": "en"
                        }
                    _file_path = os.path.join(path, "loginConfig.json")
                    if os.path.exists(_file_path):
                        try:
                            with open(_file_path, "r", encoding="utf-8") as f:
                                old_data = json.load(f)
                            if "pass" in old_data:
                                loginConfig["deviceModel"] = str(old_data["deviceModel"])
                                loginConfig["systemVersion"] = str(old_data["systemVersion"])
                                loginConfig["pass"] = str(old_data["pass"])
                        except Exception as e:
                            print(f"Warning: Could not read old file: {e}")
                    _file_path = os.path.join(path, "apiConfig.json")
                    if os.path.exists(_file_path):
                        try:
                            with open(_file_path, "r", encoding="utf-8") as f:
                                old_data = json.load(f)
                            if "apiId" in old_data:
                                loginConfig["deviceModel"] = str(old_data["deviceModel"])
                                loginConfig["systemVersion"] = str(old_data["systemVersion"])
                                loginConfig["apiId"] = str(old_data["apiId"])
                                loginConfig["apiHash"] = str(old_data["apiHash"])
                        except Exception as e:
                            print(f"Warning: Could not read old file: {e}")

                    save_json_file("loginConfig", loginConfig, path)
                    save_json_file("apiConfig", apiConfig, path)
                    process = run_telegram(path)
                    update_workscript_by_chat_id(
                        chat_id=record.get('chat_id'),
                        pid=process.pid,
                        is_closed=False,
                        state='runApp',
                        deviceModel=dm,
                        systemVersion=sv,
                        api_hash=apiHash,
                        api_id=apiId,
                        app_verssion=appVersion,
                        appversionStr=appVersionStr
                    )
                    # print("\n===== LOGIN CONFIG")
                    # logging.info("\nLOGIN CONFIG")
                    for key, value in loginConfig.items():
                        # print(f"{key:20} : {value}")
                        print(f"{key:20} : {value}")
                        

                    # print("\n===== API CONFIG")
                    # logging.info("\nAPI CONFIG")
                    for key, value in apiConfig.items():
                        # print(f"{key:20} : {value}")
                        print(f"{key:20} : {value}")
                    
                    # print(f"{'pid':20} : {process.pid}\n\n")
                    print(f"{'pid':20} : {process.pid}\n\n{'-' * 50}")
                    


                conn.close()
            else:
                print("Empty record......")
                
        except Exception as e:
            print("Error on loop:", e)
        print('*'*50)
        time.sleep(0.8)



if __name__ == "__main__":
    main()