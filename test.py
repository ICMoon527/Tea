import pymssql
from basic import Basic


if __name__ == '__main__':
    conn = pymssql.connect(host="127.0.0.1\\SQLEXPRESS",  # 连接数据库
                           user="sa",
                           password="559397",
                           database="Supermarket",  # Suppermarket
                           charset="utf8")
    Basic.setConn(conn)
    sql="insert into Sell values('{}', '{}', '{}', '{}', {}, {}, {}, '{}')".format('000', '001', Basic.getSellStockNo(), '人民', 0.1, 3600.0 * 0.1, 400.0, Basic.getNowDateTime())
    Basic.runModify(sql)