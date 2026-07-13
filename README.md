# 中国铁路购票系统（Django 练手项目）

仿 12306 风格的铁路购票 Web 应用，支持用户注册登录、车次查询、购票、订单管理与退票。

## 功能特性

- 用户注册 / 登录 / 登出 / **忘记密码 / 修改密码**
- 按出发地、目的地、日期筛选车次
- 全站搜索（车次 + 公告正文）
- **智能客服**（DeepSeek V4 疑难解答）
- 购票（服务端校验价格 + 并发锁防止超卖）
- 我的订单与退票（POST 提交 + 事务保证一致性）
- Django Admin 管理车次与座位

## 环境要求

- Python 3.10+
- MySQL 5.7+ / 8.0
- pip

## 快速开始

### 1. 克隆并进入项目

```bash
cd E:\django\huoche
```

### 2. 创建虚拟环境并安装依赖

```bash
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

### 3. 配置环境变量

```bash
copy .env.example .env
```

编辑 `.env`，填写 MySQL 账号密码、`SECRET_KEY` 和 `DEEPSEEK_API_KEY`。

### 4. 创建数据库

在 MySQL 中执行：

```sql
CREATE DATABASE huoche CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 5. 迁移并创建管理员

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 6. 启动开发服务器

```bash
python manage.py runserver
```

访问 http://127.0.0.1:8000/

## 智能客服配置

1. 在 [DeepSeek 开放平台](https://platform.deepseek.com/) 注册并创建 API Key
2. 在 `.env` 中设置 `DEEPSEEK_API_KEY=sk-xxx`
3. 访问导航栏 **客服** 或 http://127.0.0.1:8000/support/

## 忘记 / 修改密码

- **忘记密码**：登录页 → 忘记密码 → 输入用户名 + 新密码 → 提示重置成功
- **修改密码**：登录后导航栏 → 修改密码 → 输入新密码 → 提示修改成功
- 全程无需邮箱、无需旧密码

## 后台录入车次

1. 访问 http://127.0.0.1:8000/admin/
2. 使用 superuser 登录
3. 在「列车」中添加车次，并 inline 维护各座位类型、价格与余票

## 运行测试

```bash
python manage.py test
```

## 项目结构

```
huoche/          # 项目配置与首页
ticket/          # 车次、座位、购票
my/              # 用户、订单、密码、退票
support/         # 智能客服（DeepSeek V4）
templates/       # 页面模板
static/          # 静态资源
```

## 安全说明

- 购票价格在服务端从数据库读取，不接受前端传价
- 退票接口仅允许 POST
- 敏感配置通过 `.env` 管理，请勿将 `.env` 提交到版本库
