/*
SQLyog Ultimate v13.1.1 (64 bit)
MySQL - 8.0.41 : Database - supermarket_db
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`supermarket_db` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `supermarket_db`;

/*Table structure for table `members` */

DROP TABLE IF EXISTS `members`;

CREATE TABLE `members` (
  `member_id` int NOT NULL AUTO_INCREMENT COMMENT '会员ID（主键）',
  `name` varchar(50) COLLATE utf8mb4_general_ci NOT NULL COMMENT '会员姓名',
  `phone` char(11) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '手机号（唯一）',
  `points` decimal(10,2) DEFAULT '0.00' COMMENT '积分余额',
  `reg_date` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '注册时间',
  `level` varchar(20) COLLATE utf8mb4_general_ci DEFAULT '普通' COMMENT '会员等级',
  PRIMARY KEY (`member_id`),
  UNIQUE KEY `phone` (`phone`),
  KEY `idx_member_phone` (`phone`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='会员信息表';

/*Data for the table `members` */

insert  into `members`(`member_id`,`name`,`phone`,`points`,`reg_date`,`level`) values 
(1,'张三','13812345678',500.00,'2025-06-10 15:14:56','普通'),
(2,'李四','13987654321',0.00,'2025-06-10 15:14:56','普通');

/*Table structure for table `products` */

DROP TABLE IF EXISTS `products`;

CREATE TABLE `products` (
  `sku` varchar(30) COLLATE utf8mb4_general_ci NOT NULL COMMENT '商品SKU（主键）',
  `name` varchar(100) COLLATE utf8mb4_general_ci NOT NULL COMMENT '商品名称',
  `spec` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '规格（如500ml/瓶）',
  `price` decimal(8,2) NOT NULL COMMENT '单价',
  `stock` int DEFAULT '0' COMMENT '库存量',
  `supplier_id` int DEFAULT NULL COMMENT '供应商ID（外键）',
  `status` enum('在售','下架') COLLATE utf8mb4_general_ci DEFAULT '在售' COMMENT '上架状态',
  PRIMARY KEY (`sku`),
  KEY `idx_supplier_id` (`supplier_id`),
  KEY `idx_product_name` (`name`),
  CONSTRAINT `fk_supplier_id` FOREIGN KEY (`supplier_id`) REFERENCES `suppliers` (`supplier_id`),
  CONSTRAINT `ck_stock_non_negative` CHECK ((`stock` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='商品信息表';

/*Data for the table `products` */

insert  into `products`(`sku`,`name`,`spec`,`price`,`stock`,`supplier_id`,`status`) values 
('SP001','可乐500ml','瓶装',3.50,90,1,'在售'),
('SP002','纯牛奶250ml','盒装',2.80,200,2,'在售');

/*Table structure for table `sales` */

DROP TABLE IF EXISTS `sales`;

CREATE TABLE `sales` (
  `sale_no` varchar(20) COLLATE utf8mb4_general_ci NOT NULL COMMENT '销售单号（主键）',
  `member_id` int DEFAULT NULL COMMENT '会员ID（外键）',
  `cashier_id` int NOT NULL COMMENT '收银员ID',
  `total_amount` decimal(10,2) NOT NULL COMMENT '总金额',
  `sale_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '销售时间',
  PRIMARY KEY (`sale_no`),
  KEY `idx_member_id` (`member_id`),
  KEY `idx_sale_time` (`sale_time`),
  KEY `idx_sale_member_time` (`member_id`,`sale_time`),
  CONSTRAINT `fk_sales_member_id` FOREIGN KEY (`member_id`) REFERENCES `members` (`member_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='销售记录表';

/*Data for the table `sales` */

insert  into `sales`(`sale_no`,`member_id`,`cashier_id`,`total_amount`,`sale_time`) values 
('S-20250601-001',1,101,35.00,'2025-06-01 10:00:00');

/*Table structure for table `sales_weekly_summary` */

DROP TABLE IF EXISTS `sales_weekly_summary`;

CREATE TABLE `sales_weekly_summary` (
  `summary_id` int NOT NULL AUTO_INCREMENT,
  `week_start` date NOT NULL,
  `total_sales` decimal(15,2) DEFAULT '0.00',
  `total_orders` int DEFAULT '0',
  `top_product_sku` varchar(30) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '销量最高商品SKU',
  PRIMARY KEY (`summary_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='每周销售汇总表';

/*Data for the table `sales_weekly_summary` */

/*Table structure for table `stock_changes` */

DROP TABLE IF EXISTS `stock_changes`;

CREATE TABLE `stock_changes` (
  `change_id` int NOT NULL AUTO_INCREMENT COMMENT '变动ID（主键）',
  `sku` varchar(30) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '商品SKU（外键）',
  `change_type` enum('入库','出库') COLLATE utf8mb4_general_ci NOT NULL COMMENT '变动类型',
  `quantity` int NOT NULL COMMENT '变动数量（正数为入库，负数为出库）',
  `change_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '变动时间',
  PRIMARY KEY (`change_id`),
  KEY `idx_sku` (`sku`),
  CONSTRAINT `fk_sku` FOREIGN KEY (`sku`) REFERENCES `products` (`sku`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='库存变动表';

/*Data for the table `stock_changes` */

insert  into `stock_changes`(`change_id`,`sku`,`change_type`,`quantity`,`change_time`) values 
(2,'SP001','出库',10,'2025-06-10 15:14:56');

/*Table structure for table `stock_warnings` */

DROP TABLE IF EXISTS `stock_warnings`;

CREATE TABLE `stock_warnings` (
  `warning_id` int NOT NULL AUTO_INCREMENT,
  `sku` varchar(30) COLLATE utf8mb4_general_ci NOT NULL,
  `current_stock` int NOT NULL,
  `warning_time` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`warning_id`),
  KEY `idx_sku_warning` (`sku`,`warning_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='库存预警日志表';

/*Data for the table `stock_warnings` */

/*Table structure for table `suppliers` */

DROP TABLE IF EXISTS `suppliers`;

CREATE TABLE `suppliers` (
  `supplier_id` int NOT NULL AUTO_INCREMENT COMMENT '供应商ID（主键）',
  `name` varchar(100) COLLATE utf8mb4_general_ci NOT NULL COMMENT '供应商名称',
  `contact` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '联系人',
  `phone` char(11) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '联系电话',
  `address` varchar(200) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '地址',
  PRIMARY KEY (`supplier_id`),
  UNIQUE KEY `phone` (`phone`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='供应商信息表';

/*Data for the table `suppliers` */

insert  into `suppliers`(`supplier_id`,`name`,`contact`,`phone`,`address`) values 
(1,'可口可乐供应商','王经理','13800138001','上海市浦东新区'),
(2,'蒙牛供应商','李经理','13900139001','北京市朝阳区');

/* Trigger structure for table `products` */

DELIMITER $$

/*!50003 DROP TRIGGER*//*!50032 IF EXISTS */ /*!50003 `trg_products_before_update` */$$

/*!50003 CREATE */ /*!50017 DEFINER = 'root'@'localhost' */ /*!50003 TRIGGER `trg_products_before_update` BEFORE UPDATE ON `products` FOR EACH ROW BEGIN
    -- 预设库存下限（可改为从商品表字段读取，如`min_stock`）
    DECLARE stock_threshold INT DEFAULT 50;
    
    -- 仅在库存变动时触发检查
    IF OLD.stock <> NEW.stock THEN
        -- 库存低于下限时，记录警告信息（示例：插入日志表，实际可对接消息系统）
        IF NEW.stock < stock_threshold THEN
            INSERT INTO `stock_warnings` (`sku`, `current_stock`, `warning_time`)
            VALUES (NEW.sku, NEW.stock, NOW());
        END IF;
    END IF;
END */$$


DELIMITER ;

/* Trigger structure for table `sales` */

DELIMITER $$

/*!50003 DROP TRIGGER*//*!50032 IF EXISTS */ /*!50003 `trg_sales_after_insert` */$$

/*!50003 CREATE */ /*!50017 DEFINER = 'root'@'localhost' */ /*!50003 TRIGGER `trg_sales_after_insert` AFTER INSERT ON `sales` FOR EACH ROW BEGIN
    -- 定义积分系数（可改为从配置表读取）
    DECLARE points_coefficient DECIMAL(10,2) DEFAULT 1.00;
    DECLARE points_delta DECIMAL(10,2);

    -- 计算积分变动值（总金额 × 积分系数）
    SET points_delta = NEW.total_amount * points_coefficient;
    
    -- 调用积分更新存储过程（仅当会员ID存在时执行）
    IF NEW.member_id IS NOT NULL THEN
        CALL `usp_update_member_points`(NEW.member_id, points_delta, @new_points);
    END IF;
END */$$


DELIMITER ;

/* Trigger structure for table `sales` */

DELIMITER $$

/*!50003 DROP TRIGGER*//*!50032 IF EXISTS */ /*!50003 `trg_sales_before_delete` */$$

/*!50003 CREATE */ /*!50017 DEFINER = 'root'@'localhost' */ /*!50003 TRIGGER `trg_sales_before_delete` BEFORE DELETE ON `sales` FOR EACH ROW BEGIN
    DECLARE old_member_id INT;
    DECLARE old_total_amount DECIMAL(10,2);
    DECLARE sku_list VARCHAR(1000); -- 需结合销售明细表获取具体商品SKU和数量
    
    -- 获取原始销售记录的会员ID和总金额
    SET old_member_id = OLD.member_id;
    SET old_total_amount = OLD.total_amount;
    
    -- 1. 回滚积分（调用存储过程扣除积分）
    IF old_member_id IS NOT NULL THEN
        CALL `usp_update_member_points`(old_member_id, -old_total_amount, @new_points);
    END IF;
    
    -- 2. 回滚库存（需根据销售单关联的商品明细恢复库存，此处假设销售单直接关联商品SKU和数量）
    -- 实际场景中需通过销售明细表（sales_details）获取商品SKU和数量，示例如下：
    -- SELECT GROUP_CONCAT(CONCAT(sku, ':', quantity)) INTO sku_list FROM sales_details WHERE sale_no = OLD.sale_no;
    -- 解析sku_list并调用库存入库存储过程
    -- CALL `usp_manage_stock`(sku, quantity, '入库', @current_stock);
    
    -- 注：若销售单与商品明细通过中间表关联，需先删除中间表记录再处理库存
END */$$


DELIMITER ;

/*!50106 set global event_scheduler = 1*/;

/* Event structure for event `evt_clean_stock_changes_log` */

/*!50106 DROP EVENT IF EXISTS `evt_clean_stock_changes_log`*/;

DELIMITER $$

/*!50106 CREATE DEFINER=`root`@`localhost` EVENT `evt_clean_stock_changes_log` ON SCHEDULE EVERY 1 DAY STARTS '2025-06-10 00:00:00' ON COMPLETION NOT PRESERVE ENABLE DO BEGIN
    DELETE FROM `stock_changes`
    WHERE `change_time` < DATE_SUB(NOW(), INTERVAL 3 MONTH);
END */$$
DELIMITER ;

/* Event structure for event `evt_generate_weekly_sales_report` */

/*!50106 DROP EVENT IF EXISTS `evt_generate_weekly_sales_report`*/;

DELIMITER $$

/*!50106 CREATE DEFINER=`root`@`localhost` EVENT `evt_generate_weekly_sales_report` ON SCHEDULE EVERY 1 WEEK STARTS '2025-06-09 23:59:59' ON COMPLETION NOT PRESERVE ENABLE DO BEGIN
    DECLARE current_week_start DATE;
    DECLARE current_week_end DATE;
    DECLARE top_sku VARCHAR(30);
    
    -- 计算当前周范围（假设周一为周起始日）
    SET current_week_start = DATE_SUB(NOW(), INTERVAL WEEKDAY(NOW()) DAY);
    SET current_week_end = DATE_ADD(current_week_start, INTERVAL 6 DAY); -- 周日
    
    -- 获取本周销量最高商品SKU
    SELECT sku INTO top_sku
    FROM (
        SELECT sku, SUM(quantity) AS total_sold
        FROM stock_changes
        WHERE change_type = '出库' AND change_time BETWEEN current_week_start AND current_week_end
        GROUP BY sku
        ORDER BY total_sold DESC
        LIMIT 1
    ) AS sub;
    
    -- 插入汇总数据
    INSERT INTO `sales_weekly_summary` (`week_start`, `total_sales`, `total_orders`, `top_product_sku`)
    VALUES (
        current_week_start,
        (SELECT SUM(total_amount) FROM sales WHERE sale_time BETWEEN current_week_start AND current_week_end),
        (SELECT COUNT(sale_no) FROM sales WHERE sale_time BETWEEN current_week_start AND current_week_end),
        top_sku
    );
END */$$
DELIMITER ;

/* Function  structure for function  `fn_calc_member_discount` */

/*!50003 DROP FUNCTION IF EXISTS `fn_calc_member_discount` */;
DELIMITER $$

/*!50003 CREATE DEFINER=`root`@`localhost` FUNCTION `fn_calc_member_discount`(p_points DECIMAL(10,2)) RETURNS decimal(3,2)
    DETERMINISTIC
BEGIN
    DECLARE discount DECIMAL(3,2);
    -- 积分越高，折扣越大
    IF p_points >= 5000 THEN
        SET discount = 0.8;
    ELSEIF p_points >= 2000 THEN
        SET discount = 0.9;
    ELSE
        SET discount = 1.0;
    END IF;
    RETURN discount;
END */$$
DELIMITER ;

/* Function  structure for function  `fn_count_products_by_name` */

/*!50003 DROP FUNCTION IF EXISTS `fn_count_products_by_name` */;
DELIMITER $$

/*!50003 CREATE DEFINER=`root`@`localhost` FUNCTION `fn_count_products_by_name`(p_keyword VARCHAR(50)) RETURNS int
    DETERMINISTIC
BEGIN
    DECLARE product_count INT;
    -- 模糊查询商品名称
    SELECT COUNT(*) INTO product_count 
    FROM `products` 
    WHERE `name` LIKE CONCAT('%', p_keyword, '%');
    RETURN product_count;
END */$$
DELIMITER ;

/* Procedure structure for procedure `usp_get_member_total_spent` */

/*!50003 DROP PROCEDURE IF EXISTS  `usp_get_member_total_spent` */;

DELIMITER $$

/*!50003 CREATE DEFINER=`root`@`localhost` PROCEDURE `usp_get_member_total_spent`(
    IN p_member_id INT,  -- 输入：会员ID
    OUT p_total_spent DECIMAL(10,2)  -- 输出：总消费金额
)
BEGIN
    -- 直接关联 sales 表求和
    SELECT COALESCE(SUM(`total_amount`), 0) 
    INTO p_total_spent  -- 将查询结果存入输出变量
    FROM `sales`
    WHERE `member_id` = p_member_id;
END */$$
DELIMITER ;

/* Procedure structure for procedure `usp_manage_stock` */

/*!50003 DROP PROCEDURE IF EXISTS  `usp_manage_stock` */;

DELIMITER $$

/*!50003 CREATE DEFINER=`root`@`localhost` PROCEDURE `usp_manage_stock`(
    IN `p_sku` VARCHAR(30),
    IN `p_quantity` INT,
    IN `p_change_type` ENUM('入库', '出库'),
    OUT `p_current_stock` INT
)
BEGIN
    -- 检查变动类型合法性
    IF `p_change_type` NOT IN ('入库', '出库') THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '变动类型错误，必须为"入库"或"出库"';
    END IF;
    
    -- 执行库存变动
    IF `p_change_type` = '入库' THEN
        UPDATE `products` SET `stock` = `stock` + `p_quantity` WHERE `sku` = `p_sku`;
    ELSE
        -- 出库时检查库存是否足够
        IF (SELECT `stock` FROM `products` WHERE `sku` = `p_sku`) < `p_quantity` THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '库存不足，无法出库';
        END IF;
        UPDATE `products` SET `stock` = `stock` - `p_quantity` WHERE `sku` = `p_sku`;
    END IF;
    
    -- 记录库存变动日志
    INSERT INTO `stock_changes` (`sku`, `change_type`, `quantity`)
    VALUES (`p_sku`, `p_change_type`, `p_quantity`);
    
    -- 返回当前库存
    SELECT `stock` INTO `p_current_stock` FROM `products` WHERE `sku` = `p_sku`;
END */$$
DELIMITER ;

/* Procedure structure for procedure `usp_update_member_points` */

/*!50003 DROP PROCEDURE IF EXISTS  `usp_update_member_points` */;

DELIMITER $$

/*!50003 CREATE DEFINER=`root`@`localhost` PROCEDURE `usp_update_member_points`(
    IN `p_member_id` INT,
    IN `p_points_delta` DECIMAL(10,2), -- 积分变动值（正数为增加，负数为扣除）
    OUT `p_new_points` DECIMAL(10,2)
)
BEGIN
    UPDATE `members`
    SET `points` = `points` + `p_points_delta`
    WHERE `member_id` = `p_member_id`;
    
    SELECT `points` INTO `p_new_points`
    FROM `members`
    WHERE `member_id` = `p_member_id`;
END */$$
DELIMITER ;

/*Table structure for table `v_member_consumption` */

DROP TABLE IF EXISTS `v_member_consumption`;

/*!50001 DROP VIEW IF EXISTS `v_member_consumption` */;
/*!50001 DROP TABLE IF EXISTS `v_member_consumption` */;

/*!50001 CREATE TABLE  `v_member_consumption`(
 `member_id` int ,
 `name` varchar(50) ,
 `total_orders` bigint ,
 `total_spent` decimal(32,2) 
)*/;

/*Table structure for table `v_product_sales_summary` */

DROP TABLE IF EXISTS `v_product_sales_summary`;

/*!50001 DROP VIEW IF EXISTS `v_product_sales_summary` */;
/*!50001 DROP TABLE IF EXISTS `v_product_sales_summary` */;

/*!50001 CREATE TABLE  `v_product_sales_summary`(
 `sku` varchar(30) ,
 `name` varchar(100) ,
 `total_sold` decimal(32,0) ,
 `total_amount` decimal(40,2) 
)*/;

/*View structure for view v_member_consumption */

/*!50001 DROP TABLE IF EXISTS `v_member_consumption` */;
/*!50001 DROP VIEW IF EXISTS `v_member_consumption` */;

/*!50001 CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `v_member_consumption` AS select `m`.`member_id` AS `member_id`,`m`.`name` AS `name`,count(`s`.`sale_no`) AS `total_orders`,sum(`s`.`total_amount`) AS `total_spent` from (`members` `m` left join `sales` `s` on((`m`.`member_id` = `s`.`member_id`))) group by `m`.`member_id`,`m`.`name` */;

/*View structure for view v_product_sales_summary */

/*!50001 DROP TABLE IF EXISTS `v_product_sales_summary` */;
/*!50001 DROP VIEW IF EXISTS `v_product_sales_summary` */;

/*!50001 CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `v_product_sales_summary` AS select `p`.`sku` AS `sku`,`p`.`name` AS `name`,sum(`sc`.`quantity`) AS `total_sold`,sum((`p`.`price` * `sc`.`quantity`)) AS `total_amount` from (`products` `p` left join `stock_changes` `sc` on(((`p`.`sku` = `sc`.`sku`) and (`sc`.`change_type` = '出库')))) group by `p`.`sku`,`p`.`name` */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
