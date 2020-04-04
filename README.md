# covid-19-data
Provide COVID-19 data by the RESTful API

### 接口调用方式
1. 使用邮箱 [获取Token](https://covid-19.adapay.tech/docs#/authentication/authentication_register_api_v1_authentication_register_post) 认证信息
2. 将 Token 添加到 Request Header 中
3. 调用相关接口进行数据请求


### 接口文档信息
https://covid-19.adapay.tech/redoc

### 接口调试地址
https://covid-19.adapay.tech/docs

### 使用注意事项
1. Token 信息将发往您填写的邮箱当中
2. 时间区间默认值范围为前一周
3. 可通过调用[接口](https://covid-19.adapay.tech/docs#/infection/infection_area_api_v1_infection_area_get)获取支持的 country 和 city 信息
4. 数据更新使用的是美国时间，所以更新时间可能会有延后
