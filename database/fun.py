from .db import get_connection

def fetchApiHash(api_id):
    conn = get_connection()
    if not conn:
        print("[Error] not connection database (get_user_by_chat_id)")
        return None
    try:
        with conn.cursor() as cursor:
            sql = """
                SELECT * FROM telegram_accounts_hash WHERE api_id = %s
            """
            
            cursor.execute(sql, (api_id,))
            record = cursor.fetchone()
            if not record:
                return None
            return record

    except Exception as e:
        print(f"[DB ERROR] get_user_by_chat_id: {e}")
        return None

    finally:
        if conn:
            conn.close()
def get_user_by_chat_id(chat_id:str):
    conn = get_connection()
    if not conn:
        return None
    
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM account WHERE chat_id")


def phone_exists(phone: str) -> bool:
    conn = get_connection()
    if not conn:
        return False

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM accountuser WHERE number = %s",
                (phone,)
            )
            row = cursor.fetchone()
           
            return row is not None

    except Exception as e:
        print(f"[DB ERROR] phone_exists: {e}")
        return False

    finally:
        conn.close()


#=====================================


def create_tables():
    conn = get_connection()
    if not conn:
        return False

    try:
        with conn.cursor() as cursor:
            # cursor.execute("""
            # CREATE TABLE IF NOT EXISTS account (
            #     id INT UNSIGNED NOT NULL AUTO_INCREMENT,
            #     chat_id BIGINT NOT NULL,
            #     phone VARCHAR(20) DEFAULT NULL,
            #     profile TINYINT(1) NOT NULL DEFAULT 0,
            #     info TINYINT(1) NOT NULL DEFAULT 0,
            #     PRIMARY KEY (id),
            #     UNIQUE KEY uniq_chat_id (chat_id)
            # ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            # """)

            # cursor.execute("""
            # CREATE TABLE IF NOT EXISTS account_user (
            #     id INT UNSIGNED NOT NULL AUTO_INCREMENT,
            #     chat_id BIGINT NOT NULL,
            #     phone VARCHAR(20) DEFAULT NULL,
            #     profile TINYINT(1) NOT NULL DEFAULT 0,
            #     info TINYINT(1) NOT NULL DEFAULT 0,
            #     PRIMARY KEY (id),
            #     UNIQUE KEY uniq_chat_id (chat_id)
            # ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            # """)

            # cursor.execute("""
            # CREATE TABLE IF NOT EXISTS workscript (
            #     id INT UNSIGNED NOT NULL AUTO_INCREMENT,
            #     chat_id BIGINT NOT NULL,
            #     callbackquery_id VARCHAR(255) NOT NULL,
            #     pid INT NOT NULL,
            #     PRIMARY KEY (id),
            #     KEY idx_chat_id (chat_id)
            # ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            # """)
            cursor.execute("""
           CREATE TABLE IF NOT EXISTS tdversion_count (
                id INT UNSIGNED NOT NULL AUTO_INCREMENT,
                api_id BIGINT NOT NULL,
                count BIGINT NOT NULL DEFAULT 0,
                PRIMARY KEY (id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """)

        print("✅ Tables created successfully")
        return True

    except Exception as e:
        print(f"[DB ERROR] Create tables failed: {e}")
        return False

    finally:
        conn.close()




def show_tables_and_columns():
    conn = get_connection()
    if not conn:
        return False

    try:
        with conn.cursor() as cursor:
            # گرفتن لیست جدول‌ها
            cursor.execute("SHOW TABLES;")
            tables = cursor.fetchall()

            if not tables:
                print("⚠️ هیچ جدولی پیدا نشد")
                return True

            print("📦 Tables & Columns:\n")

            for table in tables:
                table_name = list(table.values())[0]
                print(f"🟦 Table: {table_name}")

                # گرفتن ستون‌های هر جدول
                cursor.execute(f"DESCRIBE `{table_name}`;")
                columns = cursor.fetchall()

                for col in columns:
                    print(f"   ├─ {col['Field']} ({col['Type']})")

                print()  # خط خالی بین جدول‌ها

        return True

    except Exception as e:
        print(f"[DB ERROR] Show tables failed: {e}")
        return False

    finally:
        conn.close()


