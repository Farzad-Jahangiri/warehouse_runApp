import psutil
import threading, time
#database
from database.user import user_get, user_update
#config
from myConfig.states import empty_state
from config import TDATA_FOLDER_NAME
#utils
from utils.fileHandler import delete_catch

def kill_telegram(pid: int, phone, chat_id) -> None:
    try:
        print(f"Killing PID {pid}")
        if pid != 0 and psutil.pid_exists(pid):
            psutil.Process(pid).kill()
            delete_catch(fr'C:\Shared\{TDATA_FOLDER_NAME}\{phone}')
        user_update.update_workscript_by_chat_id(chat_id, is_closed=False, isRunApp=False)
    except Exception as e:
        print("Error to kill app: ", e)

def kill_app(max_age_seconds: int = 120):
    try:
        appList = user_get.get_all_workscripts()
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
                    user_update.update_workscript_by_chat_id(chat_id, is_closed=False, isRunApp=False)
            elif isRunApp:
                if pid:
                    threading.Thread(target=kill_telegram, args=(int(pid), phone, chat_id), daemon=True).start()
                    # kill_telegram(int(pid), phone, chat_id)
                else:
                    user_update.update_workscript_by_chat_id(chat_id, is_closed=False, isRunApp=False)
            
            killIndex += 1
        works = user_get.fetch_record_by_runApp(True)
        if works:
            runIndex = len(works)

        allIndex = runIndex - killIndex
        return allIndex if allIndex > 0 else 0
            
    except Exception as e:
        print("Error on Kill app:", e)
        return 0