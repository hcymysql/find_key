import pymysql
from concurrent.futures import ThreadPoolExecutor, as_completed

config = {
    "host": "192.168.198.239",
    "port": 6666,
    "user": "admin",
    "password": "hechunyang"
}

# 函数用于在给定列中搜索关键字
def search_column(database_name, table_name, column_name):
    query = f"SELECT * FROM `{database_name}`.`{table_name}` WHERE `{column_name}` LIKE '%NBA%'"
    with pymysql.connect(**config) as conn:
        with conn.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            if len(result) > 0:
                with open("result.txt", "a", encoding="utf-8") as result_file:
                    result_file.write(f"库名: {database_name}，表名: {table_name}，列名: {column_name}\n")
                    for row in result:
                        result_file.write(str(row))
                        result_file.write("\n")
                        result_file.write("-" * 55)
                        result_file.write("\n")

try:
    # 获取数据库名称列表
    with pymysql.connect(**config) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SHOW DATABASES")
            databases = cursor.fetchall()
 
    # 迭代所有数据库、表和列名称，并在每个列中搜索关键字
    with ThreadPoolExecutor(max_workers=10) as executor: # 根据要求更改 max_workers
        all_tasks = []
        for database in databases:
            database_name = database[0]
            if database_name in ("information_schema", "mysql", "performance_schema", "sys"):
                continue
            with pymysql.connect(database=database_name, **config) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SHOW TABLES")
                    tables = cursor.fetchall()
                    for table in tables:
                        table_name = table[0]
                        cursor.execute(f"select COLUMN_NAME from information_schema.COLUMNS where TABLE_NAME = '{table_name}' and DATA_TYPE in ('char','varchar','text','tinytext','mediumtext','longtext') ")
                        columns = cursor.fetchall()
                        for column in columns:
                            column_name = column[0]
                            # 调度一个任务来在此列中搜索关键字
                            task = executor.submit(search_column, database_name, table_name, column_name)
                            all_tasks.append(task)

        # 等待所有任务完成
        for task in as_completed(all_tasks):
            pass

except (pymysql.err.OperationalError, TypeError, FileNotFoundError) as e:
    print(f"错误信息：{str(e)}")

print("程序运行结束。")

