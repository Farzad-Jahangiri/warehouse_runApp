from db import get_connection



def create_account():
    conn = get_connection()
    if not conn:
        return False

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE account_user (
                id INT AUTO_INCREMENT PRIMARY KEY,
                chat_id BIGINT UNIQUE,
                phone VARCHAR(20) UNIQUE DEFAULT NULL,
                `pass` VARCHAR(255) DEFAULT NULL,
                first_name VARCHAR(100),
                last_name VARCHAR(100),
                bio TEXT,
                pic VARCHAR(255),
                apiId VARCHAR(50),
                apiHash VARCHAR(100),
                isSelected TINYINT(1) DEFAULT 0,
                deviceModel VARCHAR(100),
                systemVersion VARCHAR(100),
                lang VARCHAR(10) DEFAULT 'en',
                createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                gender VARCHAR(2) DEFAULT 'm',
                profile TINYINT(1) DEFAULT 0
            );
            """)
            conn.commit() # برای اطمینان از ذخیره تغییرات در برخی درایورها
            print("Table 'account' created successfully.")
            return True

    except Exception as e:
        print(f"[DB ERROR] create_account: {e}")
        return False

    finally:
        conn.close()

def user():
    conn = get_connection()
    if not conn:
        return False

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE user (
                id INT AUTO_INCREMENT PRIMARY KEY,
                chat_id BIGINT UNIQUE,
                `pass` VARCHAR(255) DEFAULT NULL,
                apiId VARCHAR(50),
                state VARCHAR(50),
                code VARCHAR(6),
                message VARCHAR(50),
                apiHash VARCHAR(100),
                deviceModel VARCHAR(100),
                systemVersion VARCHAR(100),
                lang VARCHAR(10) DEFAULT 'en',
                createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            );
            """)
            conn.commit() # برای اطمینان از ذخیره تغییرات در برخی درایورها
            print("Table 'account' created successfully.")
            return True

    except Exception as e:
        print(f"[DB ERROR] create_account: {e}")
        return False

    finally:
        conn.close()

#{"id":"1","phone":"299275474","api_id":"33741982","api_hash":"61211399eee5d33357ec104dffcd6512",
# "os_hash":"Desktop","short_name":"solsticepanelhx9","created_at":"2026-03-17 00:12:10"},

def create_telegram_accounts_hash():
    conn = get_connection()
    if not conn:
        return False

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE telegram_accounts_hash (
                id INT AUTO_INCREMENT PRIMARY KEY,
                phone VARCHAR(20) UNIQUE DEFAULT NULL,
                api_id VARCHAR(50),
                api_hash VARCHAR(100),
                os_hash VARCHAR(100),
                short_name VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                login_count INT DEFAULT 0
            );
            """)
            conn.commit() # برای اطمینان از ذخیره تغییرات در برخی درایورها
            print("Table 'create_telegram_accounts_hash' created successfully.")
            return True

    except Exception as e:
        print(f"[DB ERROR] create_account: {e}")
        return False

    finally:
        conn.close()



def insertHash(row):
    conn = get_connection()
    if not conn:
        return False

    try:
         
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO telegram_accounts_hash (phone, api_id, api_hash, os_hash, short_name)
                VALUES (%s, %s, %s, %s, %s);
            """, (
                row['phone'],
                row['api_id'],
                row['api_hash'],
                row['os_hash'],
                row['short_name']
            ))
            return True

    except Exception as e:
        print(f"[DB ERROR] create_account: {e}")
        return False

    finally:
        conn.close()

