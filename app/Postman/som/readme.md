Cách lấy token từ OAuth2.0 cho SOM 

    1. Add Request
    2. Choose Authorization
    3. Choose Type OAuth2
    4. Như hình 2 và cấu hình những thông số như:
        + Grant type: Password Credentials
        + Access Token URL: https://identity-beta.fptshop.com.vn/connect/token
        + Client ID: crm_web
        + Username
        + Password
        + Scope: openid profile role som onehub-identity-api
        + Client Authentication: Send as Basic Auth header
        + Get Access New Token (hình 3)
    