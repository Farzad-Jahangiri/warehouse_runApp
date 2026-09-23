from database.db import get_connection
import aiomysql

async def reset_or_create_user(chat_id):
    pool:aiomysql.Pool = await get_connection()
    if not pool:
        print("[Error] not connection database (reset_or_create_user)")
        return False
    try:
        async with pool.acquire() as conn:
            conn:aiomysql.Connection
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                cursor:aiomysql.DictCursor
                sql = """
                    INSERT INTO `user` (
                        chat_id, state, code, message, `pass`, 
                        api_id, api_hash, deviceModel, systemVersion, lang, phone, step
                    ) 
                    VALUES (%s, 'None', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'fa', '0', 'none')
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
                        lang = 'fa',
                        updatedAt = CURRENT_TIMESTAMP;
                """
                
                # مقدار chat_id را برای بخش INSERT ارسال می‌کنیم
                await cursor.execute(sql, (chat_id,))
                await conn.commit()
                
                return True

    except Exception as e:
        print(f"[DB ERROR] reset_or_create_user: {e}")
        return False

 


async def update_state(chat_id, state, step='none'):
    pool:aiomysql.Pool = await get_connection()
    if not pool:
        print("[Error] not connection database (update_state)")
        return False
    try:
        async with pool.acquire() as conn:
            conn:aiomysql.Connection
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                cursor:aiomysql.DictCursor
                sql = """
                    UPDATE user SET state = %s, step = %s WHERE chat_id = %s
                """
                
                await cursor.execute(sql, (state, step, chat_id))
                await conn.commit()
                
                return True

    except Exception as e:
        print(f"[DB ERROR] update_state: {e}")
        return False

  
async def update_phone(chat_id, phone, state, isRunApp):
    pool = await get_connection()
    if not pool:
        print("[Error] not connection database (update_phone)")
        return False
    try:
        async with pool.acquire() as conn:
            conn:aiomysql.Connection
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                cursor:aiomysql.DictCursor
                if isRunApp:
                    sql = """
                        UPDATE user SET state = %s, phone = %s, isRunApp = %s, updatedAt = NOW() WHERE chat_id = %s
                    """
                    await cursor.execute(sql, (state, phone, isRunApp, chat_id))
                    await conn.commit()
                    return True
                else:
                    sql = """
                        UPDATE user SET state = %s, phone = %s, updatedAt = NOW() WHERE chat_id = %s
                    """
                    await cursor.execute(sql, (state, phone, chat_id))
                    await conn.commit()
                
                    return True

    except Exception as e:
        print(f"[DB ERROR] update_phone: {e}")
        return False


async def updateCode(chat_id:str, code:str):
    pool:aiomysql.Pool = await get_connection()
    if not pool:
        print("[Error] not connection database (updateCode)")
        return False
    try:
        async with pool.acquire() as conn:
            conn:aiomysql.Connection
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                cursor:aiomysql.DictCursor
                sql = """
                    UPDATE user SET code = %s WHERE chat_id = %s
                """
                await cursor.execute(sql, (code, chat_id))
                await conn.commit()
            
                return True

    except Exception as e:
        print(f"[DB ERROR] updateCode: {e}")
        return False

async def updatePassword(chat_id:str, password:str):
    pool:aiomysql.Pool = await get_connection()
    if not pool:
        print("[Error] not connection database (updatePassword)")
        return False
    try:
        async with pool.acquire() as conn:
            conn:aiomysql.Connection
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                cursor:aiomysql.DictCursor
                sql = """
                    UPDATE user SET pass = %s WHERE chat_id = %s
                """
                await cursor.execute(sql, (password, chat_id))
                await conn.commit()
            
                return True

    except Exception as e:
        print(f"[DB ERROR] updatePassword: {e}")
        return False

async def update_workscript_by_chat_id(
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
    pool:aiomysql.Pool = await get_connection()
    if not pool:
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
        async with pool.acquire() as conn:
            conn:aiomysql.Connection
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                cursor:aiomysql.DictCursor
                await cursor.execute(query, values)
                await conn.commit()
                return cursor.rowcount > 0  # آیا واقعاً آپدیت شد؟

    except Exception as e:
        print(f"[DB ERROR] update_workscript_by_chat_id: {e}")
        return False




