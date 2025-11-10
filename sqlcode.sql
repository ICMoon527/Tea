-- 彻底删除旧数据库（确保彻底清理）
IF DB_ID(N'Supermarket') IS NOT NULL
BEGIN
    ALTER DATABASE Supermarket SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
    DROP DATABASE Supermarket;
END
GO

-- 创建数据库
CREATE DATABASE Supermarket;
GO

-- 切换到数据库（必须用GO分隔，否则后续表创建会在master库）
USE Supermarket;
GO

-- 创建商品表
CREATE TABLE Commodity(
    commodity_no varchar(10) primary key,/*商品编号*/
    commodity_company nvarchar(20),/*货源公司*/
    commodity_location nvarchar(10),/*商品产地*/
    commodity_name nvarchar(20),/*商品名称*/
    commodity_type1 nvarchar(10),/*商品类型*/
    commodity_size nvarchar(10),/*商品计量单位*/
    commodity_bprice float,/*成本/斤*/
    commodity_sprice float,/*零售/斤*/
    commodity_mdate datetime,/*生产日期*/
    commodity_edate int,/*保质期*/
    commodity_quantity float,/*库存数量*/
    commodity_description NVARCHAR(500) /*品质特征*/
);
GO

INSERT INTO Commodity
VALUES
    ('001', '孤芳不自赏', '神牛授首', '神牛', '肉桂', '斤', 3600.0, 21000.0, '2025-11-03', 5, 2.8, '盖香上花香更显，叶底香枞韵更显，有桂皮香、有木质香、有森林感，带奶香，香气的持久度超绝，富有张力。滋味上厚度超绝，层次非常丰富，很有冲击力，直击天灵盖！市场价600/泡，此刻语言很苍白…总之顶配岩茶就是这样啦！'),
    ('002', '孤芳不自赏', '慧苑坑', '百年老枞', '水仙', '斤', 800.0, 7800.0, '2025-11-03', 5, 3.0, '岩韵和枞韵非常显，香气浑厚饱满，浑厚中又带着明显的清雅花香。一入口就是正岩的高级感，舌面上有花相继绽开的感觉，非常典型的岩骨花香！茶汤稠滑且活，醇厚饱满。是让人很爽的一个水仙！');
GO

-- 创建收银员表
CREATE TABLE Cashier(
    cashier_no varchar(10) primary key,/*员工编号*/
    cashier_name nvarchar(10),
    cashier_pwd varchar(10),
    cashier_sex char(2),
    cashier_age int,
    cashier_hourse float,
    cashier_salary float,
    cashier_phone varchar(11)
);
GO

INSERT INTO Cashier
VALUES
    ('000', '超级管理员', '559397', 'M', 100, 0, 0, '17816872650');
GO

-- 创建采购员表
CREATE TABLE Purchaser(
    purchaser_no varchar(10) primary key,/*员工编号*/
    purchaser_name nvarchar(10),
    purchaser_pwd varchar(10),
    purchaser_sex char(2),
    purchaser_age int,
    purchaser_salary float,
    purchaser_phone varchar(11)
    -- purchaser_entrytime datetime
);
GO

INSERT INTO Purchaser
VALUES
    ('000', '超级管理员', '559397', 'M', 100, 0, '17816872650');
GO

-- 创建库存表
CREATE TABLE Stock(
    purchaser_no varchar(10),
    commodity_no varchar(10),
    stock_no varchar(20),
    stock_sprice float,
    stock_quantity float,
    stock_date datetime,
    primary key(stock_no),
    foreign key(purchaser_no) references Purchaser(purchaser_no) on delete set null,
    foreign key(commodity_no) references Commodity(commodity_no) on delete set null
);
GO

-- 创建销售表
CREATE TABLE Sell(
    cashier_no varchar(10),
    commodity_no varchar(10),
    sell_no varchar(20),
    buyer_name NVARCHAR(10),
    sell_quantity float,
    sell_price float,/*应收金额*/
    sell_rmoney float,/*实收金额*/
    sell_date datetime,
    primary key(sell_no),
    foreign key(cashier_no) references Cashier(cashier_no) on delete set null,/*修正：删除多余空格*/
    foreign key(commodity_no) references Commodity(commodity_no) on delete set null/*修正：删除多余空格和逗号*/
);
GO

-- 创建管理员表（修正手机号长度、中文存储）
CREATE TABLE Administrator(
    admin_no varchar(10),
    admin_pwd varchar(10),
    admin_name nvarchar(10),
    admin_phone varchar(11),
    admin_addres nvarchar(20),
    primary key (admin_no)
);
GO

INSERT INTO Administrator
VALUES
    ('000', '559397', '超级管理员', '17816872650', '紫金西苑'),
    ('001', 'Lang0527', '郎君伟', '17816872650', '紫金西苑');
GO

-- 创建触发器（确保表已存在，用GO分隔）
/*Sell表级联删除触发器*/
CREATE TRIGGER Delete_sellcommodity
ON Commodity
FOR DELETE
AS
DELETE Sell
FROM deleted
WHERE Sell.commodity_no=deleted.commodity_no;
GO

/*Sell表级联删除触发器*/
CREATE TRIGGER Delete_sellcashier
ON Cashier
FOR DELETE
AS
DELETE Sell
FROM deleted
WHERE Sell.cashier_no=deleted.cashier_no;
GO

/*Stock表级联删除触发器*/
CREATE TRIGGER Delete_stockCommodity
ON Commodity
FOR DELETE
AS
DELETE Stock
FROM deleted
WHERE Stock.commodity_no=deleted.commodity_no;
GO

/*Stock表级联删除触发器*/
CREATE TRIGGER Delete_stockpurchaser
ON Purchaser
FOR DELETE
AS
DELETE Stock
FROM deleted
WHERE Stock.purchaser_no=deleted.purchaser_no;
GO