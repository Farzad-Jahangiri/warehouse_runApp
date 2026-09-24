from database.db import get_connection



def getAllAccount():
    conn = get_connection()
    if not conn:
        return []

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT phone FROM account"
            )
            rows = cursor.fetchall()
           
            return rows

    except Exception as e:
        print(f"[DB ERROR] phone_exists: {e}")
        return []

    finally:
        conn.close()

def count_account(chat_id: int) -> int:
    conn = get_connection()
    if not conn:
        return 0

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT COUNT(*) AS total FROM account WHERE chat_id = %s",
                (chat_id,)
            )
            row = cursor.fetchone()
            return row["total"] if row else 0


    except Exception as e:
        print(f"[DB ERROR] count_account_by_chat_id: {e}")
        return 0

    finally:
        conn.close()

