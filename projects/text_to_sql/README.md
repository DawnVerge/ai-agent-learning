# Text-to-SQL

将自然语言问题转为数据库查询：先发现表名和结构，再生成一条只读 SQL，最后根据真实结果回答。入口为 db_tools.py，数据库封装为 db_manager.py。

在仓库根目录准备环境：配置 DASHSCOPE_API_KEY，以及 MYSQL_HOST、MYSQL_PORT、MYSQL_USER、MYSQL_PASSWORD、MYSQL_DATABASE。数据库用户、密码和数据库名没有默认值；密码从本机环境读取，连接 URL 使用 SQLAlchemy URL.create 构造。

## 手动准备示例数据

使用 MySQL 8，并由有建表权限的账户在专用空数据库中执行 db_init.sql。程序不会自动创建数据库、建表或插入数据。

先在仓库根目录打开 MySQL 客户端：

~~~powershell
mysql -u setup_user -p
~~~

随后在 MySQL 客户端中执行：

~~~sql
CREATE DATABASE ai_learning_demo CHARACTER SET utf8mb4;
USE ai_learning_demo;
SOURCE projects/text_to_sql/db_init.sql;
~~~

setup_user 为你自己的建库账户。db_init.sql 创建 products、orders 并插入固定演示数据；不要在已有同名表的业务数据库中执行。初始化后，为查询程序配置只能读取该数据库的独立账户，并将 MYSQL_DATABASE 设为 ai_learning_demo。初始化使用的账户与查询账户可不同。

## 运行

~~~powershell
python -m ai_learning run project.text-to-sql
~~~

程序询问“销量排名前 5 的商品是哪些？”。你可以在 main 中替换问题。执行需要模型 API 和本地 MySQL，会调用模型服务。

查询层只接受单条 SELECT 或 WITH…SELECT；拒绝多语句、修改类操作、INTO、锁定子句、可执行注释和部分有副作用的函数。执行前设置 MySQL READ ONLY 事务，结束时回滚，最多读取 200 行。词法检查采用保守的教学规则，不是完整 SQL 解析器，可能拒绝部分合法写法；生产使用仍应依靠数据库只读账户及额外访问控制。表结构不包含外键详情。

离线验证不会连接模型或数据库：

~~~powershell
python -m unittest discover -s tests -p test_database.py
~~~
