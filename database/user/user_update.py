from database.db import get_connection

def reset_or_create_user(chat_id):
    conn = get_connection()
    if not conn:
        print("[Error] not connection database (reset_or_create_user)")
        return False
    try:
        with conn.cursor() as cursor:
            sql = """
                INSERT INTO `user` (
                    chat_id, state, code, message, `pass`, 
                    api_id, api_hash, deviceModel, systemVersion, lang, phone, step, selected
                ) 
                VALUES (%s, 'None', NULL, NULL, NULL, NULL, NULL, NULL, NULL, '', '0', 'none', false)
                ON DUPLICATE KEY UPDATE 
                    state = 'None',
                    code = NULL,
                    message = NULL,
                    `pass` = NULL,
                    api_id = NULL,
                    is_closed = true,
                    phone = '0',
                    api_hash = NULL,
                    deviceModel = NULL,
                    systemVersion = NULL,
                    step = 'none',
                    selected = false,
                    updatedAt = CURRENT_TIMESTAMP;
            """
            
            # مقدار chat_id را برای بخش INSERT ارسال می‌کنیم
            cursor.execute(sql, (chat_id,))
            conn.commit()
            
            return True

    except Exception as e:
        print(f"[DB ERROR] reset_or_create_user: {e}")
        return False

    finally:
        if conn:
            conn.close()


def update_state(chat_id, state, step='none'):
    conn = get_connection()
    if not conn:
        print("[Error] not connection database (update_state)")
        return False
    try:
        with conn.cursor() as cursor:
            sql = """
                UPDATE user SET state = %s, step = %s WHERE chat_id = %s
            """
            
            cursor.execute(sql, (state, step, chat_id))
            conn.commit()
            
            return True

    except Exception as e:
        print(f"[DB ERROR] update_state: {e}")
        return False

    finally:
        if conn:
            conn.close()

def update_phone(chat_id, phone, state, isRunApp, worker_id):
    conn = get_connection()
    if not conn:
        print("[Error] not connection database (update_phone)")
        return False
    try:
        with conn.cursor() as cursor:
            if isRunApp:
                sql = """
                    UPDATE user SET state = %s, phone = %s, isRunApp = %s, updatedAt = NOW(), worker_id = %s WHERE chat_id = %s
                """
                cursor.execute(sql, (state, phone, isRunApp, worker_id, chat_id))
                conn.commit()
                return True
            else:
                sql = """
                    UPDATE user SET state = %s, phone = %s, updatedAt = NOW() WHERE chat_id = %s
                """
                cursor.execute(sql, (state, phone, chat_id))
                conn.commit()
            
                return True

    except Exception as e:
        print(f"[DB ERROR] update_phone: {e}")
        return False

    finally:
        if conn:
            conn.close()


def updateCode(chat_id:str, code:str):
    conn = get_connection()
    if not conn:
        print("[Error] not connection database (updateCode)")
        return False
    try:
        with conn.cursor() as cursor:
            sql = """
                UPDATE user SET code = %s WHERE chat_id = %s
            """
            cursor.execute(sql, (code, chat_id))
            conn.commit()
        
            return True

    except Exception as e:
        print(f"[DB ERROR] updateCode: {e}")
        return False

def updatePassword(chat_id:str, password:str):
    conn = get_connection()
    if not conn:
        print("[Error] not connection database (updatePassword)")
        return False
    try:
        with conn.cursor() as cursor:
            sql = """
                UPDATE user SET pass = %s WHERE chat_id = %s
            """
            cursor.execute(sql, (password, chat_id))
            conn.commit()
        
            return True

    except Exception as e:
        print(f"[DB ERROR] updatePassword: {e}")
        return False

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
    selected = None
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



