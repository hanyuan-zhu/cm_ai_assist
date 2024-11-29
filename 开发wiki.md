# 项目目录结构

- 需求文档.md
- API.md
- backend/
  - app.py
  - config.py
  - extensions.py
  - models/
    - __init__.py
    - change_request.py
    - company.py
    - employee.py
    - project.py
    - user.py
  - resources/
    - __init__.py
    - auth.py
    - changes.py
    - companies.py
    - employees.py
    - users.py
  - schemas/
    - __init__.py
    - change_schema.py
    - company_schema.py
    - employee_schema.py
    - project_schema.py
    - user_schema.py
  - tests/
    - test_api.py
- README.md

## 目录说明

### 需求文档.md
项目需求文档，描述了项目的功能需求和开发计划。

### API.md
API文档，详细描述了各个API的路径、请求方法、请求参数和返回值。

### README.md
项目的README文件，通常包含项目简介、安装和运行说明等内容。

### backend 目录
包含Flask应用的主要代码。

#### app.py
Flask应用的入口文件，包含应用的创建和配置。

#### config.py
配置文件，包含数据库URI、密钥等配置信息。

#### extensions.py
扩展文件，初始化Flask扩展（如SQLAlchemy、Flask-RESTful、JWT等）。

### models 目录
模型文件，定义了数据库表结构和ORM模型。

#### __init__.py
初始化文件，导入所有模型。

#### change_request.py
变动请求模型，定义了员工调岗、离职等变动请求的表结构。

#### company.py
公司模型，定义了公司的表结构。

#### employee.py
员工模型，定义了员工的表结构。

#### project.py
项目模型，定义了项目的表结构。

#### user.py
用户模型，定义了用户的表结构。

### resources 目录
资源文件，定义了API的路由和处理逻辑。

#### __init__.py
初始化文件，导入并初始化所有资源。

#### auth.py
认证资源，包含登录、注册和登出功能。

#### changes.py
变动资源，包含获取待确认变动、批准变动、拒绝变动等功能。

#### companies.py
公司资源，包含获取公司列表、获取公司项目列表等功能。

#### employees.py
员工资源，包含获取在岗员工列表、添加新员工等功能。

#### users.py
用户资源，包含获取当前登录用户信息的功能。

### schemas 目录
模式文件，定义了数据序列化和反序列化的模式。

#### __init__.py
初始化文件，导入所有模式。

#### change_schema.py
变动模式，定义了变动请求的序列化和反序列化规则。

#### company_schema.py
公司模式，定义了公司的序列化和反序列化规则。

#### employee_schema.py
员工模式，定义了员工的序列化和反序列化规则。

#### project_schema.py
项目模式，定义了项目的序列化和反序列化规则。

#### user_schema.py
用户模式，定义了用户的序列化和反序列化规则。

### tests 目录
测试文件，包含API的测试用例。

#### test_api.py
API测试文件，包含对各个API的测试用例。