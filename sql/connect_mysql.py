
import mysql.connector
from mysql.connector import Error
import datetime
import time

def create_connection():
    """建立与 MySQL 数据库的连接"""
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',  # 数据库主机
            database='communicate_sql',  # 数据库名称
            user='root',  # 用户名
            password='lx102326',  # 密码
            buffered=True,  # 关键参数
            use_pure = True  # 强制使用纯 Python，避免 C 扩展
        )
        if connection.is_connected():
            # print("Successfully connected to the database.")
            return connection
    except Error as e:
        print("Error while connecting to MySQL:", e)
        return None

def insert_data(connection, table_name, data):
    """插入数据到指定的表"""
    try:
        cursor = connection.cursor()

        # 获取列名和占位符
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))

        # 创建插入语句
        insert_query = f"INSERT INTO `{table_name}` ({columns}) VALUES ({placeholders});"

        # 执行插入
        cursor.execute(insert_query, tuple(data.values()))
        connection.commit()  # 提交更改

        # print(f"{cursor.rowcount} record inserted successfully into {table_name} table.")

    except Error as e:
        print("Error while inserting data:", e)

    finally:
        cursor.close()  # 确保游标关闭

def select_data(connection, tableName, column, data):
    cursor = connection.cursor()
    # 查询是否存在 admin 用户
    try:
        # 查询是否存在指定用户
        cursor.execute(f"SELECT * FROM {tableName} WHERE {column} = %s", (data,))
        result = cursor.fetchone()  # 获取查询结果
        # print('result =', result)
        if result:
            # print(f"用户 {data} 存在。")
            return True
        else:
            print(f"用户 {data} 不存在。")
            return False
    finally:
        # 确保游标总是被关闭
        cursor.close()

def select_column_data(connection, tableName, selectColumn, column, data):
    cursor = connection.cursor()
    # 查询是否存在 admin 用户
    cursor.execute(f"SELECT {selectColumn} FROM {tableName} WHERE {column} = %s", (data,))
    result = cursor.fetchall()  # 获取查询结果
    # print('result=', result)
    cursor.close()
    return result

def connect_sql_insert(database, data):
    conn = create_connection()
    if conn is not None:
        insert_data(conn, database, data)

        # 关闭连接
        if conn.is_connected():
            conn.close()
            # print("MySQL connection is closed.")


current_time = datetime.datetime.now()
# 格式化时间
formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

def connect_sql_update(database, updateColumn, updateData, fromColum, fromData):
    max_retries = 5
    attempt = 0

    while attempt < max_retries:
        conn = None
        cursor = None
        try:
            conn = create_connection()
            if conn is None:
                print("Failed to connect to the database.")
                return

            cursor = conn.cursor()
            cursor.execute("""
                UPDATE {database} 
                SET {updateColumn} = %s, UPDT_TIME = %s, UPDT_USER_NO = 'sys' 
                WHERE {fromColum} = %s""".format(
                    database=database,
                    updateColumn=updateColumn,
                    fromColum=fromColum
                ), (updateData, formatted_time, fromData))

            conn.commit()
            # print("Update successful.")
            break  # 成功时退出循环
        except Error as err:
            if err.errno == 1205:  # Lock wait timeout exceeded
                attempt += 1
                print(f"Lock wait timeout exceeded. Attempt {attempt} of {max_retries}. Retrying...")
                time.sleep(1)  # 等待一段时间再重试
            else:
                print(f"Error: {err}")
                break  # 遇到其他错误时退出循环
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

def connect_sql_select(database, column, data):
    conn = create_connection()
    if conn is not None:
        select_data(conn, database, column, data)
        # 关闭连接
        if conn.is_connected():
            conn.close()
            # print("MySQL connection is closed.")

def select_idiom_count(connection, tableName, column, data):
    cursor = connection.cursor()
    # 查询是否存在 admin 用户
    try:
        # 查询是否存在指定用户
        cursor.execute(f"SELECT count(*) FROM {tableName} WHERE {column} = %s", (data,))
        result = cursor.fetchone()  # 获取查询结果
        # print('result =', result)
        return result[0]

    finally:
        # 确保游标总是被关闭
        cursor.close()

def select_two_conditions(connection, tableName, selectColumn, column1, data1, column2, data2):
    cursor = connection.cursor()
    try:
        query = f"SELECT {selectColumn} FROM {tableName} WHERE {column1} = %s and {column2} = %s"
        params = (data1, data2)

        # 打印完整查询语句（实际执行的SQL）
        cursor.execute(query, params)
        # print("Executed sql:", cursor.statement)  # MySQL Connector/Python
        # 或使用 cursor._executed（PyMySQL 或某些驱动）

        result = cursor.fetchall()
        if result:
            return result
        return None
    finally:
        cursor.fetchall()  # 消费剩余结果
        cursor.close()

def select_one_column_data(connection, tableName, column):
    cursor = connection.cursor()
    # 查询是否存在 admin 用户
    try:
        # 查询是否存在指定用户
        cursor.execute(f"SELECT {column} FROM {tableName}")
        result = cursor.fetchall()  # 获取查询结果
        # print('result =', result)
        return result
    finally:
        # 确保游标总是被关闭
        cursor.close()

def select_all_data(connection, tableName, column, data):
    cursor = connection.cursor()
    # 查询是否存在 admin 用户
    try:
        # 查询是否存在指定用户
        cursor.execute(f"SELECT * FROM {tableName} WHERE {column} = %s order by inst_time desc", (data,))
        result = cursor.fetchall()  # 获取查询结果
        # print('result =', result)
        return result
    finally:
        # 确保游标总是被关闭
        cursor.close()


# 主程序逻辑
if __name__ == "__main__":
    conn = create_connection()
    # current_time = datetime.now()
    co_user_info_data = {
            'USER_NAME': 'Amy',
            'ROLE_CODE': '003',
            'ROLE_NAME': 'rabbit03',
            'ON_LINE': '10000001',
            'IS_USE': '10000001',
            'REMARK': None,
            'INST_TIME': current_time,  # 可以在执行时处理时间
            'INST_USER_NO': 'sys',
            'UPDT_TIME': None,  # 可以在执行时处理时间
            'UPDT_USER_NO': None
        }
    # connect_sql_insert('co_user_info', co_user_info_data)
    # is_user = select_data(conn, 'auth_user', 'USER_NAME', 'Anna')
    # idiom_count = select_idiom_count(conn, 'co_user_play_dtl', 'BATTLE_SITUATION', '3564')
    # start_time = select_two_conditions(conn, 'co_ai_play_dtl', 'inst_time', 'BATTLE_SITUATION', '3564', 'SORT', '1')
    # Situation_db = select_one_column_data(conn, 'co_ai_play_dtl', 'BATTLE_SITUATION')
    records = select_all_data(conn, 'co_user_play_record', 'USER_NAME', 'ANNA')

    print('records=', records)
