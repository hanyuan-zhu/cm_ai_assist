## API目录

| 分类               | 方法 | 路径                     | 描述                     |
|-------------------|------|--------------------------|--------------------------|
| 用户认证相关       | POST | /api/auth/login          | 登录接口，返回token和用户信息。 |
| 用户认证相关       | POST | /api/auth/register       | 注册接口，返回成功消息。     |
| 用户认证相关       | POST | /api/auth/logout         | 登出接口，返回成功消息。     |
| 人员列表相关       | GET  | /api/active-employees    | 获取在岗（及待岗）人员名单。 |
| 人员列表相关       | GET  | /api/pending-changes     | 获取待确认变动名单。         |
| 员工管理相关       | POST | /api/employees           | 添加新员工，设置初始状态为待岗。 |
| 员工管理相关       | PUT  | /api/employees/{id}/transfer | 提交员工调岗申请。         |
| 员工管理相关       | PUT  | /api/employees/{id}/resign  | 提交员工离职申请。         |
| 变动管理相关       | PUT  | /api/pending-changes/{id}/approve | 确认变动申请。         |
| 变动管理相关       | PUT  | /api/pending-changes/{id}/reject | 拒绝变动申请。         |
| 公司和项目相关     | GET  | /api/companies           | 获取公司列表。             |
| 公司和项目相关     | GET  | /api/projects            | 获取项目列表。             |
| 用户信息相关       | GET  | /api/users/me            | 获取当前登录用户的信息。     |



## API详情（参数和返回）
### 1. 用户认证相关

- **POST /api/auth/login**
  - **描述:** 用户登录，返回token和用户信息。
  - **参数:** `username` (string), `password` (string)
  - **返回:** `token` (string), `user` (object)

- **POST /api/auth/register**
  - **描述:** 用户注册，返回成功消息。
  - **参数:** `username` (string), `password` (string)
  - **返回:** `success` (boolean), `message` (string)

- **POST /api/auth/logout**
  - **描述:** 用户登出，返回成功消息。
  - **参数:** 无（需在header中包含认证token）
  - **返回:** `success` (boolean), `message` (string)

### 2. 人员列表相关

- **GET /api/active-employees**
  - **描述:** 获取在岗（及待岗）人员名单。
  - **参数:** 无
  - **返回:** `employees` (array)
    - 每个员工对象包含以下字段：
      - `id` (string)
      - `name` (string)
      - `position` (string)
      - `company_id` (int)
      - `company_name` (string)
      - `project_id` (int)
      - `project_name` (string)
      - `status` (string): `'在岗'`, `'待岗'`, `'离职'`
      - `hireDate` (string): 格式 `YYYY-MM-DD`

- **GET /api/pending-changes**
  - **描述:** 获取待确认变动名单。
  - **参数:** 无
  - **返回:** `changes` (array)
    - 每个变动对象包含以下字段：
      - `id` (int)
      - `type` (string): `'入职'`, `'离职'`, `'调岗'`
      - `employee_id` (int)
      - `employee_name` (string)
      - `from_company_id` (int | null)
      - `from_company_name` (string | null)
      - `to_company_id` (int | null)
      - `to_company_name` (string | null)
      - `from_project_id` (int | null)
      - `from_project_name` (string | null)
      - `to_project_id` (int | null)
      - `to_project_name` (string | null)
      - `effective_date` (string): 格式 `YYYY-MM-DD`
      - `status` (string): `'待确认'`, `'已确认'`, `'已拒绝'`

### 3. 员工管理相关

- **POST /api/employees**
  - **描述:** 添加新员工，设置初始状态为待岗。
  - **参数:** `name` (string), `position` (string), `hireDate` (string): 格式 `YYYY-MM-DD`
  - **返回:** `success` (boolean), `employee` (object): 与GET /api/active-employees返回的员工对象相同

- **PUT /api/employees/{id}/transfer**
  - **描述:** 提交员工调岗申请。
  - **参数:** `newCompany` (string), `newProject` (string), `effectiveDate` (string): 格式 `YYYY-MM-DD`
  - **返回:** `success` (boolean), `message` (string)

- **PUT /api/employees/{id}/resign**
  - **描述:** 提交员工离职申请。
  - **参数:** `resignDate` (string): 格式 `YYYY-MM-DD`
  - **返回:** `success` (boolean), `message` (string)

### 4. 变动管理相关

- **PUT /api/pending-changes/{id}/approve**
  - **描述:** 确认变动申请。
  - **参数:** 无
  - **返回:** `success` (boolean), `message` (string)

- **PUT /api/pending-changes/{id}/reject**
  - **描述:** 拒绝变动申请。
  - **参数:** 无
  - **返回:** `success` (boolean), `message` (string)

### 5. 公司和项目相关

- **GET /api/companies**
  - **描述:** 获取公司列表。
  - **参数:** 无
  - **返回:** `companies` (array)

- **GET /api/companies/{id}/projects**

  - **描述:** 获取（公司所属的）项目列表。
  - **参数:** 无
  - **返回:** `projects` (array)

### 6. 用户信息相关

- **GET /api/users/me**
  - **描述:** 获取当前登录用户的信息。
  - **参数:** 无（需在header中包含认证token）
  - **返回:** `user` (object)
