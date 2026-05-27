# -*- coding: utf-8 -*-
"""
    @Author  : Zephyr
    @Date    : 2026/5/23 13:54
    @Project  : NumpyAndPandas
    @File     : test_mysql1.py
    @IDE      : PyCharm
    @Description: 
"""
import pymysql
import os
import sys
import time

# 新增：MySQL连接重试函数，解决服务未就绪问题
def get_mysql_conn():
    max_retries = 10  # 最多重试10次
    retry_delay = 2   # 每次重试间隔2秒
    for i in range(max_retries):
        try:
            conn = pymysql.connect(
                host=os.getenv('MYSQL_HOST', 'localhost'),
                port=int(os.getenv('MYSQL_PORT', 3306)),
                user=os.getenv('MYSQL_USER', 'root'),
                password=os.getenv('MYSQL_PASSWORD', 'abcd0123'),
                database=os.getenv('MYSQL_DB', 'test_db'),
                charset='utf8mb4',
                connect_timeout=3
            )
            print(f"✅ 第{i+1}次尝试：MySQL连接成功！")
            return conn
        except pymysql.err.OperationalError as e:
            print(f"❌ 第{i+1}次尝试：MySQL连接失败 - {e}")
            if i < max_retries - 1:
                print(f"⏳ 等待{retry_delay}秒后重试...")
                time.sleep(retry_delay)
            else:
                raise Exception("❌ 重试10次后仍无法连接MySQL，请检查容器配置！") from e

# 主逻辑
if __name__ == "__main__":
    conn = None
    cursor = None
    try:
        # 获取带重试的数据库连接
        conn = get_mysql_conn()
        cursor = conn.cursor()

        # 原测试逻辑不变
        cursor.execute("SELECT DATABASE()")
        db_name = cursor.fetchone()[0]
        print(f"当前连接的数据库：{db_name}")

        cursor.execute("CREATE TABLE IF NOT EXISTS test_table (id INT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(50))")
        cursor.execute("INSERT INTO test_table (name) VALUES ('Docker Compose测试')")
        conn.commit()

        cursor.execute("SELECT * FROM test_table")
        data = cursor.fetchall()
        print("test_table中的测试数据：", data)

        # 输出Python版本
        python_version = sys.version
        print(f"\n当前运行的Python版本：{python_version}")
        print("🎉 Docker Compose环境下，Python连接MySQL（8.0.45）成功！")

    except Exception as e:
        print(f"\n❌ 程序执行失败：{e}")
        if conn:
            conn.rollback()  # 出错回滚事务
    finally:
        # 确保资源关闭
        if cursor:
            cursor.close()
        if conn:
            conn.close()
