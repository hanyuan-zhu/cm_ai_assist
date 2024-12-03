
清晰的api文档除了route外，还需要：
1. 示例响应：为每个API添加一个示例响应，展示实际返回的数据结构。
2. 字段说明：详细说明每个字段的含义和可能的值。
3. 错误响应：列出可能的错误响应及其含义。


可以让AI来协助完成，主要提供：
1. models文件
2. resources文件/route文件
3. schemas文件

然后要求输出为markdown格式，包含api说明、示例响应、字段说明和错误响应。

以下是一个示例：

用户认证API
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
