from database.db import get_connection
#type
from customType.userTypes import UserData
from typing import List

def get_user_by_chat_id(chat_id):
    conn = get_connection()
    if not conn:
        print("[Error] not connection database (get_user_by_chat_id)")
        return None
    try:
        with conn.cursor() as cursor:
            sql = """
                SELECT * FROM user WHERE chat_id = %s
            """
            
            cursor.execute(sql, (chat_id,))
            record: UserData | None = cursor.fetchone()
            if not record:
                return None
            return record

    except Exception as e:
        print(f"[DB ERROR] get_user_by_chat_id: {e}")
        return None

    finally:
        if conn:
            conn.close()

def get_user_by_state(chat_id) -> List[UserData] | None:
    conn = get_connection()
    if not conn:
        print("[Error] not connection database (get_user_by_chat_id)")
        return None
    try:
        with conn.cursor() as cursor:
            sql = """
                SELECT * FROM user WHERE state = %s
            """
            
            cursor.execute(sql, (chat_id,))
            record: List[UserData] | None = cursor.fetchall()
            if not record:
                return None
            return record

    except Exception as e:
        print(f"[DB ERROR] get_user_by_chat_id: {e}")
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
                 lang, createdAt, updatedAt FROM user WHERE state = %s AND selected = false FOR UPDATE
            """
            
            cursor.execute(sql, (state))
            record = cursor.fetchall()
            if not record:
                conn.commit()
                return None
            ids = [row['id'] for row in record]

            # 2️⃣ آپدیت همان ردیف‌ها
            placeholders = ",".join(["%s"] * len(ids))
            cursor.execute(f"""
                UPDATE user
                SET selected = true
                WHERE id IN ({placeholders})
            """, ids)
            conn.commit()

            return record

    except Exception as e:
        print(f"[DB ERROR] fetch_record_by_state: {e}")
        return None

    finally:
        if conn:
            conn.close()



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

