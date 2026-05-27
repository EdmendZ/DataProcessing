# -*- coding: utf-8 -*-
"""
    @Author  : Zephyr
    @Date    : 2026/5/23 11:33
    @Project  : NumpyAndPandas
    @File     : mysql.py
    @IDE      : PyCharm
    @Description: 
"""
import pymysql

# 连接MySQL（参数与启动容器时一致）
conn = pymysql.connect(
    host='localhost',  # 本地地址，端口已映射
    port=9999,         # 映射后的端口
    user='root',       # MySQL默认用户名
    password='abcd0123', # 启动容器时设置的密码
    database='mysql',  # MySQL默认数据库
    charset='utf8mb4', # 避免中文乱码
    cursorclass=pymysql.cursors.DictCursor  # 可选，让查询结果更易读
)

cursor = conn.cursor()
# 测试连接：查询MySQL版本
cursor.execute("SELECT VERSION()")
print(f"MySQL版本：{cursor.fetchone()['VERSION()']}")

# 关闭连接
cursor.close()
conn.close()
print("基础版：Python连接MySQL（8.0.45）成功！")
