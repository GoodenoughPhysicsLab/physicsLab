# 通过`physicsLab`使用物实网络API

## class User
`User`类是对一个真实的物实用户的封装

* 匿名用户登录:
```python
from physicsLab import web
user = web.User()
```

* 通过邮箱密码登录:
```python
from physicsLab import web
user = web.User(YOUR_EMAIL, YOUR_PASSWORD)
```

* 通过`Token`, `AuthCode`登录:
```python
from physicsLab import *
user = web.User(
    token=YOUR_TOKEN,
    auth_code=YOUR_AUTH_CODE,
)
```

一个`User`的对象有以下属性:
* avatar_region
* decoration
* nickname: 用户昵称
* signature
* avatar: 当前头像的索引
* avatar_region
* decoration
* verification
<del>为什么有些属性没写是什么意思呢? 因为我也不知道()</del>

`User`类也提供了一些方法, 这些方法是对物实网络api的封装:
> 注: 以`async_`开头的方法为协程风格的api
