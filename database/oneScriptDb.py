import pymysql
from dbutils.pooled_db import PooledDB
DB_CONFIG = {
    "host":"127.0.0.1",
    "user":"root",
    "password":"4356910872Gty#",
    "database":"warehouse",
    "port":3306,
    "charset":"utf8mb4",
    "cursorclass":pymysql.cursors.DictCursor,
    "autocommit":True,
}

pool = PooledDB(
    creator=pymysql,      # کتابخانه اتصال
    maxconnections=5,    # حداکثر کانکشن
    mincached=5,          # حداقل کانکشن آماده
    maxcached=2,          # حداکثر کانکشن idle
    blocking=True,        # اگر پر شد صبر کند
    maxusage= 5000,
    ping=1,               # قبل استفاده connection چک شود
    **DB_CONFIG
)

def get_connection():
    try:
        conn = pool.connection()
        return conn
    except Exception as e:
        print(f"[DB ERROR] Connection failed {e}")
        return None





