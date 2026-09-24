from database.db import get_connection


def create_account_user(
    chat_id,
    phone=None,
    apiHash='',
    password=None,
    api_id=0,
    deviceModel='',
    systemVersion='',
    app_verssion='6.6.2'
):
    conn = get_connection()
    if not conn:
        return False

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                    "SELECT id FROM accountuser WHERE number = %s LIMIT 1;",
                    (phone,)
                )
            exists = cursor.fetchone()

            if exists:
                print("exist number: ", phone)
                return False
         
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO accountuser (id, number, pass, apiId, apiHash, deviceModel, systemVersion, lang, app_verssion)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
            """, (
                chat_id,
                phone,
                password,
                str(api_id),
                apiHash,
                deviceModel,
                systemVersion,
                'en',
                app_verssion
            ))
            return True

    except Exception as e:
        print(f"[DB ERROR] create_account_user: {e}")
        return False

    finally:
        conn.close()

# create_account_user(chat_id=1635752625,
#                info=False,
#                password="21372",
#                phone="989934621366",
#                profile=False)




def count_account_user(chat_id: int) -> int:
    conn = get_connection()
    if not conn:
        return 0

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT COUNT(*) AS total FROM account_user WHERE chat_id = %s",
                (chat_id,)
            )
            row = cursor.fetchone()
            return row["total"] if row else 0


    except Exception as e:
        print(f"[DB ERROR] count_account_user_by_chat_id: {e}")
        return 0

    finally:
        conn.close()

