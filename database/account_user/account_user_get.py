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
