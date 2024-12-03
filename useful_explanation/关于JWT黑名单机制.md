JWT黑名单机制详解：

1. 用户登录：
    - 用户登录成功后，服务器生成一个JWT并返回给用户。

2. 用户访问受保护资源：
    - 用户在请求头中携带JWT访问受保护的API端点。
    - Flask-JWT-Extended 会自动验证JWT的有效性。

3. 调用黑名单检查回调：
    - 在验证JWT时，Flask-JWT-Extended 会调用通过 @jwt.token_in_blocklist_loader 注册的回调函数 check_if_token_in_blacklist。
    - 该函数检查JWT的唯一标识符（JTI）是否在黑名单中。

4. 处理验证结果：
    - 如果JWT不在黑名单中，验证通过，用户请求被处理。
    - 如果JWT在黑名单中，验证失败，返回相应的错误响应。

5. jwt_blacklist 的存储：
    - jwt_blacklist 保存在 extensions.py 中，用于存储所有已注销的JWT。

6. 用户登出：
    - Logout API（在 auth.py 中）会将JWT的JTI添加到 jwt_blacklist 中，使得该JWT失效。

7. 使用 @jwt_required() 装饰器的资源：
    - 当一个资源使用了 @jwt_required() 装饰器时，Flask-JWT-Extended 会在处理请求时自动进行以下步骤：
        7.1. 验证JWT的有效性：
            - 检查JWT的签名是否正确。
            - 检查JWT是否过期。
        7.2. 调用黑名单检查回调：
            - 调用通过 @jwt.token_in_blocklist_loader 注册的回调函数 check_if_token_in_blacklist。
            - 该回调函数会检查JWT的唯一标识符（JTI）是否在黑名单中。

总结：
- 用户登录后会获得一个JWT，用于访问受保护的资源。
- 每次访问受保护资源时，JWT都会被验证，并调用黑名单检查回调函数。
- 如果JWT在黑名单中，访问请求会被拒绝。
- 用户登出时，JWT的JTI会被添加到黑名单中，确保该JWT无法再使用。
