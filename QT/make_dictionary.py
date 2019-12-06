import pymysql
#coding=utf-8
#encoding=utf-8
'''
利用数据库数据
构建jieba分词专用词典
'''
# 用于连接数据库
config = {
    "host": "47.102.223.103",
    "port": 3306,
    'database': 'course_design',
    "charset": "utf8",
    "user": "root",
    "password": "aliyun"
}

if __name__ == '__main__':
    f = open('dictionary.txt', mode='w', encoding='utf-8')
    db = pymysql.connect(**config)
    cur = db.cursor()
    cur.execute("select DISTINCT province.p_name from province")
    for i in cur.fetchall():
        f.write(str(i[0]))  # 省
        f.write(" 200 ns\n")
    cur.execute("select DISTINCT schools.s_name from schools")
    for i in cur.fetchall():
        f.write(str(i[0]))  # 校名
        f.write(" 1000 nt\n")
    cur.execute("select DISTINCT majors.m_name from majors")
    for i in cur.fetchall():
        f.write(str(i[0]))  # 专业名
        f.write("专业 200000 nz\n")
    cur.execute("select DISTINCT majors.batch from majors")
    for i in cur.fetchall():
        f.write(str(i[0]))  # 批次名
        f.write(" 2000 nz\n")

    f.write("文科 1000 nz\n")
    f.write("理科 1000 nz\n")
    f.write("综合 1000 nz\n")
    f.write("2016年 2000 nz\n")
    f.write("2017年 2000 nz\n")
    f.write("2018年 2000 nz\n")

    f.close()