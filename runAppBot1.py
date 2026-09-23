import subprocess, time, os, json
from subprocess import Popen
from typing import List, TypedDict
import random
from datetime import datetime
from database.oneScriptDb import get_connection
from utils.fileHandler import save_json_file
from utils.phone import split_phone_number
from myConfig.states import intro_phone
from myConfig.deviseAndsystemVertion import deviceModel, systemVersion
from config import TDATA_FOLDER_NAME
from killApp import kill_app
from utils.fileHandler import delete_catch
import psutil
import hashlib
import threading
from customType.userTypes import UserData


def get_all_workscripts():
    conn = get_connection()
    if not conn:
        return []

    try:
        with conn.cursor() as cursor:
            # cursor.execute("SELECT * FROM workscript;")
            cursor.execute("""
                SELECT *
                FROM user
                WHERE is_closed = TRUE
                OR updatedAt <= NOW() - INTERVAL 2 MINUTE;
            """)
            records = cursor.fetchall()
            return records  # لیست دیکشنری‌ها

    except Exception as e:
        print(f"[DB ERROR] get_all_workscripts: {e}")
        return []

    finally:
        conn.close()

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
    api_hash= None
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

def fetch_record_by_state(state):
    conn = get_connection()
    if not conn:
        print("[Error] not connection database (fetch_record_by_state)")
        return None
    try:
        with conn.cursor() as cursor:
            sql = """
                SELECT id, phone, chat_id, `pass` AS password, api_id, api_hash, state, code, message, deviceModel, systemVersion,
                 lang, createdAt, updatedAt FROM user WHERE state = %s
            """
            
            cursor.execute(sql, (state,))
            record = cursor.fetchall()
            if not record:
                return None
            return record

    except Exception as e:
        print(f"[DB ERROR] fetch_record_by_state: {e}")
        return None

    finally:
        if conn:
            conn.close()

def kill_telegram(pid: int, phone, chat_id) -> None:
    try:
        print(f"Killing PID {pid}")
        if pid != 0 and psutil.pid_exists(pid):
            psutil.Process(pid).kill()
            delete_catch(fr'C:\Shared\{TDATA_FOLDER_NAME}\{phone}')
        update_workscript_by_chat_id(chat_id, is_closed=False, isRunApp=False)
    except Exception as e:
        print("Error to kill app: ", e)

def kill_app(max_age_seconds: int = 120):
    try:
        appList = get_all_workscripts()
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
                    threading.Thread(target=kill_telegram, args=(int(pid), phone, chat_id), daemon=True).start()
                    # kill_telegram(int(pid), phone, chat_id)
                else:
                    update_workscript_by_chat_id(chat_id, is_closed=False, isRunApp=False)
            elif isRunApp:
                if pid:
                    threading.Thread(target=kill_telegram, args=(int(pid), phone, chat_id), daemon=True).start()
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







defaultVersion = [
    {'vstr':'5.1.4', 'vint':5001004},
    {'vstr':'5.1.5', 'vint':5001005},
    {'vstr':'5.1.6', 'vint':5001006},
    {'vstr':'5.1.7', 'vint':5001007},
    {'vstr':'5.1.8', 'vint':5001008},
    {'vstr':'5.2.1', 'vint':5002001},
    {'vstr':'5.2.2', 'vint':5002002},
    {'vstr':'5.2.3', 'vint':5002003},
    {'vstr':'5.2.4', 'vint':5002004},
    {'vstr':'5.2.5', 'vint':5002005},
    {'vstr':'5.2.6', 'vint':5002006},
    {'vstr':'5.3.1', 'vint':5003001},
    {'vstr':'5.3.2', 'vint':5003002},
    {'vstr':'5.4.1', 'vint':5004001},
    {'vstr':'5.4.2', 'vint':5004002},
    {'vstr':'5.4.3', 'vint':5004003},
    {'vstr':'5.4.4', 'vint':5004004},
    {'vstr':'5.4.5', 'vint':5004005},
    {'vstr':'5.4.6', 'vint':5004006},
    {'vstr':'5.5.1', 'vint':5005001},
    {'vstr':'5.5.2', 'vint':5005002},
    {'vstr':'5.5.3', 'vint':5005003},
    {'vstr':'5.5.4', 'vint':5005004},
    {'vstr':'5.5.5', 'vint':5005005},
    {'vstr':'5.5.6', 'vint':5005006},
    {'vstr':'5.5.7', 'vint':5005007},
    {'vstr':'5.5.8', 'vint':5005008},
    {'vstr':'5.6.1', 'vint':5006001},
    {'vstr':'5.6.2', 'vint':5006002},
    {'vstr':'5.6.3', 'vint':5006003},
    {'vstr':'5.6.4', 'vint':5006004},
    {'vstr':'5.7.1', 'vint':5007001},
    {'vstr':'5.7.2', 'vint':5007002},
    {'vstr':'5.7.3', 'vint':5007003},
    {'vstr':'5.7.4', 'vint':5007004},
    {'vstr':'5.8.1', 'vint':5008008},
    {'vstr':'5.8.2', 'vint':5008002},
    {'vstr':'5.8.3', 'vint':5008003},
    {'vstr':'5.8.4', 'vint':5008004},
    {'vstr':'5.8.5', 'vint':5008005},
    {'vstr':'5.9.1', 'vint':5009001},
    {'vstr':'5.9.2', 'vint':5009002},
    {'vstr':'6.1.1', 'vint':6001001},
    {'vstr':'6.1.2', 'vint':6001002},
    {'vstr':'6.1.3', 'vint':6001003},
    {'vstr':'6.1.4', 'vint':6001004},
    {'vstr':'6.2.2', 'vint':6002002},
    {'vstr':'6.2.3', 'vint':6002003},
    {'vstr':'6.2.4', 'vint':6002004},
    {'vstr':'6.2.5', 'vint':6002005},
    {'vstr':'6.2.6', 'vint':6002006},
    {'vstr':'6.3.1', 'vint':6003001},
    {'vstr':'6.3.2', 'vint':6003002},
    {'vstr':'6.3.3', 'vint':6003003},
    {'vstr':'6.3.4', 'vint':6003004},
    {'vstr':'6.3.6', 'vint':6003006},
    {'vstr':'6.3.7', 'vint':6003007},
    {'vstr':'6.3.8', 'vint':6003008},
    {'vstr':'6.3.9', 'vint':6003009},
    {'vstr':'6.4.1', 'vint':6004001},
    {'vstr':'6.4.3', 'vint':6004003},
    {'vstr':'6.4.4', 'vint':6004004},
    {'vstr':'6.5.1', 'vint':6005001},
    {'vstr':'6.6.1', 'vint':6006001},
    {'vstr':'6.6.2', 'vint':6006002},
]

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

def getProxy():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM proxy ORDER BY updated_at ASC LIMIT 1 FOR UPDATE")
            proxyData = cursor.fetchone()
            cursor.execute("""
                    UPDATE proxy
                    SET updated_at = NOW()
                    WHERE id = %s
                """, (proxyData['id'],))
            return proxyData
    except Exception as e:
        print("[ERROR GET PROXY] ",e)
        return None
    finally:
        if conn:
            conn.close()

def main():
    global appData
    
    
 

    while True:
        try:
            countList = kill_app()
            print("count of running app: ",countList)
            if countList >= 20:
                print("⚠️ Reached max apps, waiting for cleanup")
                continue
            records = fetch_record_by_state(intro_phone)
            
            if records:
                conn = get_connection()
                apiData = {}
                
                for record in records:
                    code, phone = split_phone_number(f'+{record.get('phone')}')
                    # if code not in ['998']:
                    with conn.cursor() as cursor:
                        cursor.execute("""
                            SELECT *
                            FROM telegram_accounts_hash 
                            WHERE login_count < 300 
                            AND api_id != 2040
                            AND selected = 0
                            ORDER BY login_count ASC
                            LIMIT 1
                            FOR UPDATE
                        """)
                        apiData = cursor.fetchone()
                        cursor.execute("""
                        UPDATE telegram_accounts_hash
                        SET selected = 1
                        WHERE api_id = %s
                    """, (apiData['api_id'],))
                        conn.commit()
                            
                    
                    path = fr"F:\warehouseTdata\{baseFolder}\{str(code)+str(phone)}"
                    print(f"Phone: {str(code)+str(phone)}")
                    print(f"Chat id: {record.get('chat_id')}")
                    print("Path: ", path)
                    print("apiData:", apiData)
                    dmList = deviceModel.copy()
                    smList = systemVersion.copy()
                    random.shuffle(dmList)
                    random.shuffle(smList)
                    dm = random.choice(dmList)
                    sv = random.choice(smList)
                    
                    # apiId = 2040
                    # apiHash = 'b18441a1ff607e10a989891a5462e627'
                    # appVersion = 6006002
                    # appVersionStr = '6.6.2'
                    # if code in ['']:
                    #     random.shuffle(defaultVersion)
                    #     vDic = random.choice(defaultVersion)
                    #     apiId = 2040
                    #     apiHash = 'b18441a1ff607e10a989891a5462e627'
                    #     appVersion = vDic['vint']
                    #     appVersionStr = vDic['vstr']
                    # else:
                    apiId = int(apiData['api_id'])
                    apiHash = apiData["api_hash"]
                    appVersion, appVersionStr = generate_version(apiHash)
                    
                    proxy = getProxy()
                    loginConfig = {
                        "phoneNumber": str(phone),
                        "chatId": str(record.get('chat_id')),
                        "prefix": str(code),
                        "isSetProxy": True,
                        "proxyIp": proxy['ip'],
                        "proxyPassword": proxy['password'],
                        "proxyPort": proxy['port'],
                        "proxyUsername": proxy['username'],
                        "deviceModel": dm,
                        "systemVersion": sv,
                        "errorUrl": "http://127.0.0.1:8008/tg/intro_error/",
                        "introCodeUrl": "http://127.0.0.1:8008/tg/intro_code/",
                        "introPasswordUrl": "http://127.0.0.1:8008/tg/intro_password/",
                        "passwordSetUrl": "http://127.0.0.1:8008/tg/new_password_set/",
                        "frozenAccountUrl": "http://127.0.0.1:8008/tg/frozen_account/",
                        "pass": "",
                        "tdataPath": baseFolder,
                        "isDefaultPassword": True,
                        "apiId": apiId,
                        "apiHash": apiHash,
                    }
                    print(appVersion)
                    print(appVersionStr)
                    apiConfig = {
                        "apiId": apiId,
                        "apiHash": apiHash,
                        "deviceModel": dm,
                        "systemVersion": sv,
                        "tdataPath": baseFolder,
                        "appVersion": appVersion,
                        "appVersionStr": appVersionStr,
                        "lang": "en",
                        "resetUrl":"http://127.0.0.1:8008/tg/reset_account/",
                        "frozenUrl":"http://127.0.0.1:8008/tg/frozen_account/"
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
                    print("pid:", process.pid)
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

                conn.close()
            else:
                print("Empty record......")
                
        except Exception as e:
            print("Error on loop:", e)
        print('*'*50)
        time.sleep(0.8)



if __name__ == "__main__":
    main()