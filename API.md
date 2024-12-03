## API目录

| 分类               | 方法 | 路径                     | 描述                     |
|-------------------|------|--------------------------|--------------------------|
| 用户认证相关       | POST | /api/auth/login          | 登录接口，返回token和用户信息。 |
| 用户认证相关       | POST | /api/auth/register       | 注册接口，返回成功消息。     |
| 用户认证相关       | POST | /api/auth/logout         | 登出接口，返回成功消息。     |
| 用户信息相关       | GET  | /api/users/me            | 获取当前登录用户的信息。     |
| 人员列表相关       | GET  | /api/active-employees    | 获取在岗（及待岗）人员名单。 |
| 人员列表相关       | GET  | /api/pending-changes     | 获取待确认变动名单。         |
| 员工管理相关       | POST | /api/employees           | 添加新员工，设置初始状态为待岗。 |
| 员工管理相关       | PUT  | /api/pending-changes/{id}/transfer | 提交员工调岗申请。         |
| 员工管理相关       | PUT  | /api/pending-changes/{id}/resign  | 提交员工离职申请。         |
| 变动管理相关       | PUT  | /api/pending-changes/{id}/approve | 确认变动申请。         |
| 变动管理相关       | PUT  | /api/pending-changes/{id}/reject | 拒绝变动申请。         |
| 公司和项目相关     | GET  | /api/companies           | 获取公司列表。             |
| 公司和项目相关     | GET  | /api/projects            | 获取项目列表。             |



## API详情（参数和返回）
### 1. 用户认证相关

- **POST /api/auth/login**
  - **描述:** 用户登录，返回token和用户信息。
  - **参数:** 
    - `username` (string): 用户名
    - `password` (string): 密码
  - **返回:**
    - 成功响应:
      ```json
      {
        "token": "<JWT token>",
        "user": {
          "id": 1,
          "username": "zhang_san"
        }
      }
      ```
    - 错误响应:
      - 401 Unauthorized:
        ```json
        {
          "message": "无效的凭据 (Invalid credentials)"
        }
        ```

- **POST /api/auth/register**
  - **描述:** 用户注册，返回成功消息。
  - **参数:** 
    - `username` (string): 用户名
    - `password` (string): 密码
  - **返回:**
    - 成功响应:
      ```json
      {
        "success": true,
        "message": "用户注册成功 (User registered successfully)",
        "user": {
          "id": 1,
          "username": "zhang_san"
        }
      }
      ```
    - 错误响应:
      - 400 Bad Request:
        ```json
        {
          "success": false,
          "message": "用户名已存在 (Username already exists)"
        }
        ```
      - 500 Internal Server Error:
        ```json
        {
          "success": false,
          "message": "注册过程中出错 (Error during registration): <error_message>"
        }
        ```

- **POST /api/auth/logout**
  - **描述:** 用户登出，返回成功消息。
  - **参数:** 无（需在header中包含认证token）
  - **返回:**
    - 成功响应:
      ```json
      {
        "success": true,
        "message": "Logged out successfully"
      }
      ```

- **GET /api/users/me**
  - **描述:** 获取当前登录用户的信息。
  - **参数:** 无（需在header中包含认证token）
  - **返回:**
    - 成功响应:
      ```json
      {
        "id": 1,
        "username": "zhang_san"
      }
      ```
    - 错误响应:
      - 404 Not Found:
        ```json
        {
          "message": "未找到用户 (User not found)"
        }
        ```

### 2. 人员列表相关

- **GET /api/active-employees**
  - **描述:** 获取在岗（及待岗）人员名单。
  - **参数:** 无
  - **返回:** 
    - 成功响应:
      ```json
      {
        "employees": [
          {
            "id": 1,
            "name": "张三",
            "position": "开发工程师",
            "hire_date": "2023-10-01",
            "status": "在岗",
            "company_id": 1,
            "company_name": "Company A",
            "project_id": 1,
            "project_name": "Project A",
            "creator_id": 1
          },
          {
            "id": 2,
            "name": "李四",
            "position": "测试工程师",
            "hire_date": "2023-09-15",
            "status": "待岗",
            "company_id": null,
            "company_name": null,
            "project_id": null,
            "project_name": null,
            "creator_id": 1
          }
        ]
      }
      ```
    - 错误响应:
      - 500 Internal Server Error:
        ```json
        {
          "message": "获取在岗员工列表时出错 (Error retrieving active employees list): <error_message>"
        }
      ```
    -  **字段说明**
      - `id` (int): 员工ID
      - `name` (string): 员工姓名
      - `position` (string): 员工职位
      - `hire_date` (string): 到岗生效日期，格式 `YYYY-MM-DD`
      - `status` (string): 员工状态，可能的值为 `'在岗'`, `'待岗'`, `'离职'`
      - `company_id` (int | null): 所属公司ID
      - `company_name` (string | null): 所属公司名称
      - `project_id` (int | null): 所属项目ID
      - `project_name` (string | null): 所属项目名称
      - `creator_id` (int): 创建者ID

- **GET /api/pending-changes**
  - **描述:** 获取待确认变动名单。
  - **参数:** 无
  - **返回:** 
    - 成功响应:
      ```json
      {
        "changes": [
          {
            "id": 1,
            "type": "调岗",
            "employee_id": 1,
            "employee_name": "张三",
            "from_company_id": 1,
            "from_company_name": "Company A",
            "to_company_id": 2,
            "to_company_name": "Company B",
            "from_project_id": 1,
            "from_project_name": "Project A",
            "to_project_id": 2,
            "to_project_name": "Project B",
            "effective_date": "2023-10-01",
            "status": "待确认",
            "creator_id": 1
          },
          {
            "id": 2,
            "type": "离职",
            "employee_id": 2,
            "employee_name": "李四",
            "from_company_id": 1,
            "from_company_name": "Company A",
            "to_company_id": null,
            "to_company_name": null,
            "from_project_id": 1,
            "from_project_name": "Project A",
            "to_project_id": null,
            "to_project_name": null,
            "effective_date": "2023-11-01",
            "status": "待确认",
            "creator_id": 1
          }
        ]
      }
      ```
    - 错误响应:
      - 500 Internal Server Error:
        ```json
        {
          "message": "获取待确认变动名单时出错: <error_message>"
        }
        ```
    - 字段说明:
      - `id` (int): 变动请求ID
      - `type` (string): 变动类型（入职/调岗/离职）
      - `employee_id` (int): 员工ID
      - `employee_name` (string): 员工姓名
      - `from_company_id` (int | null): 原公司ID
      - `from_company_name` (string | null): 原公司名称
      - `to_company_id` (int | null): 目标公司ID
      - `to_company_name` (string | null): 目标公司名称
      - `from_project_id` (int | null): 原项目ID
      - `from_project_name` (string | null): 原项目名称
      - `to_project_id` (int | null): 目标项目ID
      - `to_project_name` (string | null): 目标项目名称
      - `effective_date` (string): 生效日期，格式 `YYYY-MM-DD`
      - `status` (string): 状态（待确认/已确认/已拒绝）
      - `creator_id` (int): 创建者ID

### 3. 员工管理相关

- **POST /api/employees**
  - **描述:** 添加新员工，设置初始状态为待岗。
  - **参数:** 
    - `name` (string): 员工姓名
    - `position` (string): 员工职位
    - `hireDate` (string): 入职日期，格式 `YYYY-MM-DD`
  - **返回:**
    - 成功响应:
      ```json
      {
        "employee": {
          "id": 1,
          "name": "张三",
          "position": "开发工程师",
          "hire_date": "2023-10-01",
          "status": "待岗",
          "company_id": null,
          "company_name": null,
          "project_id": null,
          "project_name": null,
          "creator_id": 1
        }
      }
      ```
    - 错误响应:
      - 400 Bad Request:
        ```json
        {
          "message": "Name is required."
        }
        ```
      - 500 Internal Server Error:
        ```json
        {
          "message": "添加员工时出错 (Error adding employee): <error_message>"
        }
        ```


### 4. 变动管理相关

- **PUT /api/pending-changes/{id}/transfer**
  - **描述:** 提交员工调岗申请。
  - **参数:** 
    - `new_company` (string): 新公司ID
    - `new_project` (string): 新项目ID
    - `effective_date` (string): 格式 `YYYY-MM-DD`
  - **返回:**
    - 成功响应:
      ```json
      {
        "success": true,
        "message": "调岗申请已提交"
      }
      ```
    - 错误响应:
      - 404 Not Found:
        ```json
        {
          "message": "未找到员工"
        }
        ```
      - 500 Internal Server Error:
        ```json
        {
          "message": "提交调岗申请时出错: <error_message>"
        }
        ```

- **PUT /api/pending-changes/{id}/resign**
  - **描述:** 提交员工离职申请。
  - **参数:** 
    - `resign_date` (string): 格式 `YYYY-MM-DD`
  - **返回:**
    - 成功响应:
      ```json
      {
        "success": true,
        "message": "离职申请已提交"
      }
      ```
    - 错误响应:
      - 404 Not Found:
        ```json
        {
          "message": "未找到员工"
        }
        ```
      - 500 Internal Server Error:
        ```json
        {
          "message": "提交离职申请时出错: <error_message>"
        }
        ```

- **PUT /api/pending-changes/{id}/approve**
  - **描述:** 确认变动申请。
  - **参数:** 无
  - **返回:**
    - 成功响应:
      ```json
      {
        "success": true,
        "message": "变更请求已批准 (Change request approved)"
      }
      ```
    - 错误响应:
      - 404 Not Found:
        ```json
        {
          "message": "未找到变更请求 (Change request not found)"
        }
        ```
      - 400 Bad Request:
        ```json
        {
          "message": "变更请求已处理 (Change request already processed)"
        }
        ```
      - 500 Internal Server Error:
        ```json
        {
          "message": "确认变动申请时出错: <error_message>"
        }
        ```

- **PUT /api/pending-changes/{id}/reject**
  - **描述:** 拒绝变动申请。
  - **参数:** 无
  - **返回:**
    - 成功响应:
      ```json
      {
        "success": true,
        "message": "变更请求已拒绝 (Change request rejected)"
      }
      ```
    - 错误响应:
      - 404 Not Found:
        ```json
        {
          "message": "未找到变更请求 (Change request not found)"
        }
        ```
      - 400 Bad Request:
        ```json
        {
          "message": "变更请求已处理 (Change request already processed)"
        }
        ```
      - 500 Internal Server Error:
        ```json
        {
          "message": "拒绝变动申请时出错: <error_message>"
        }
        ```

### 5. 公司和项目相关

- **GET /api/companies**
  - **描述:** 获取公司列表。
  - **参数:** 无
  - **返回:**
    - 成功响应:
      ```json
      {
        "companies": [
          {
            "id": 1,
            "name": "Company A"
          },
          {
            "id": 2,
            "name": "Company B"
          }
        ]
      }
      ```
      - 字段说明:
        - `id` (int): 公司ID
        - `name` (string): 公司名称
    - 错误响应:
      - 500 Internal Server Error:
        ```json
        {
          "message": "获取公司列表时出错 (Error retrieving company list): <error_message>"
        }
        ```

- **GET /api/companies/{id}/projects**
  - **描述:** 获取（公司所属的）项目列表。
  - **参数:** 无
  - **返回:**
    - 成功响应:
      ```json
      {
        "projects": [
          {
            "id": 1,
            "name": "Project A",
            "company_id": 1
          },
          {
            "id": 2,
            "name": "Project B",
            "company_id": 1
          }
        ]
      }
      ```
      - 字段说明:
        - `id` (int): 项目ID
        - `name` (string): 项目名称
        - `company_id` (int): 所属公司ID
    - 错误响应:
      - 404 Not Found:
        ```json
        {
          "message": "未找到公司 (Company not found)"
        }
        ```
      - 500 Internal Server Error:
        ```json
        {
          "message": "获取项目列表时出错 (Error retrieving project list): <error_message>"
        }
        ```
