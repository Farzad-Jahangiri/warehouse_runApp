from database.db import get_connection
import aiomysql
#type
from customType.userTypes import UserData
from typing import List

async def get_user_by_chat_id(chat_id):
    pool:aiomysql.Pool = await get_connection()
    if not pool:
        print("[Error] not connection database (get_user_by_chat_id)")
        return None
    try:
        async with pool.acquire() as conn:
            conn:aiomysql.Connection
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                cursor:aiomysql.DictCursor
                sql = """
                    SELECT * FROM user WHERE chat_id = %s
                """
                
                await cursor.execute(sql, (chat_id,))
                record: UserData | None = await cursor.fetchone()
                if not record:
                    return None
                return record

    except Exception as e:
        print(f"[DB ERROR] get_user_by_chat_id: {e}")
        return None


async def get_user_by_state(chat_id) -> List[UserData] | None:
    pool:aiomysql.Pool = await get_connection()
    if not pool:
        print("[Error] not connection database (get_user_by_chat_id)")
        return None
    try:
        async with pool.acquire() as conn:
            conn:aiomysql.Connection
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                cursor:aiomysql.DictCursor
                sql = """
                    SELECT * FROM user WHERE state = %s
                """
                
                await cursor.execute(sql, (chat_id,))
                record: List[UserData] | None = await cursor.fetchall()
                if not record:
                    return None
                return record

    except Exception as e:
        print(f"[DB ERROR] get_user_by_chat_id: {e}")
        return None




async def fetch_record_by_state(state):
    pool:aiomysql.Pool = await get_connection()
    if not pool:
        print("[Error] not connection database (fetch_record_by_state)")
        return None
    try:
        async with pool.acquire() as conn:
            conn:aiomysql.Connection
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                cursor:aiomysql.DictCursor
                sql = """
                    SELECT id, phone, chat_id, `pass` AS password, api_id, api_hash, state, code, message, deviceModel, systemVersion,
                    lang, createdAt, updatedAt FROM user WHERE state = %s
                """
                
                await cursor.execute(sql, (state,))
                record = await cursor.fetchall()
                if not record:
                    return None
                return record

    except Exception as e:
        print(f"[DB ERROR] fetch_record_by_state: {e}")
        return None




async def get_all_workscripts():
    pool:aiomysql.Pool = await get_connection()
    if not pool:
        return []

    try:
        async with pool.acquire() as conn:
            conn:aiomysql.Connection
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                cursor:aiomysql.DictCursor
            # cursor.execute("SELECT * FROM workscript;")
                await cursor.execute("""
                    SELECT *
                    FROM user
                    WHERE is_closed = TRUE
                    OR updatedAt <= NOW() - INTERVAL 2 MINUTE;
                """)
                records = await cursor.fetchall()
                return records  # لیست دیکشنری‌ها

    except Exception as e:
        print(f"[DB ERROR] get_all_workscripts: {e}")
        return []

  
async def fetch_record_by_runApp(runApp=True):
    pool:aiomysql.Pool = await get_connection()
    if not pool:
        print("[Error] not connection database (fetch_record_by_state)")
        return None
    try:
        async with pool.acquire() as conn:
            conn:aiomysql.Connection
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                cursor:aiomysql.DictCursor
                sql = """
                    SELECT id, chat_id, `pass` AS password, api_id, api_hash, state, code, message, deviceModel, systemVersion,
                    lang, createdAt, updatedAt, isRunApp FROM user WHERE isRunApp = %s
                """
                
                await cursor.execute(sql, (runApp,))
                record: List[UserData] | None = await cursor.fetchall()
                if not record:
                    return None
                return record

    except Exception as e:
        print(f"[DB ERROR] fetch_record_by_state: {e}")
        return None



