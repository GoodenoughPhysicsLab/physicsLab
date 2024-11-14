# 物理实验室 API 文档

本文档提供了物理实验室 API 的详细说明，包括各个方法的参数、返回值和功能描述。

## 目录

- [物理实验室 API 文档](#物理实验室-api-文档)
  - [目录](#目录)
  - [详细说明](#详细说明)
    - [class User](#class-user)
    - [获取社区作品列表](#获取社区作品列表)
    - [查询实验](#查询实验)
    - [获取实验](#获取实验)
    - [确认发布实验](#确认发布实验)
    - [发表评论](#发表评论)
    - [获取留言板信息](#获取留言板信息)
    - [获取实验介绍](#获取实验介绍)
    - [获取作品的详细信息](#获取作品的详细信息)
    - [获取用户信息](#获取用户信息)
    - [获取用户资料](#获取用户资料)
    - [添加收藏](#添加收藏)
    - [上传实验图片](#上传实验图片)
    - [获取用户收到的消息](#获取用户收到的消息)
    - [获取支持列表](#获取支持列表)
    - [获取用户的关注/粉丝列表](#获取用户的关注粉丝列表)
    - [关注用户](#关注用户)
    - [修改用户昵称](#修改用户昵称)
    - [领取每日签到奖励](#领取每日签到奖励)

---

## 详细说明

### class User
`User`类是对一个真实的物实用户的封装
匿名用户登录:
```python
from physicsLab import web
user = web.User()
```
通过邮箱密码登录:
```python
from physicsLab import web
user = web.User(YOUR_EMAIL, YOUR_PASSWORD)
```
通过`Token`, `AuthCode`登录:
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

`User`还有以下方法, 对应着在物实中的真实的操作:
> 注: 以下方法都有以`async_`开头的, 支持协程风格调用的对应api

### 获取社区作品列表
```python
def get_library(self) -> dict:
    ''' 获取社区作品列表 '''
```

### 查询实验
```python
def query_experiment(self,
                     tags: Optional[List[Tag]] = None,
                     exclude_tags: Optional[List[Tag]] = None,
                     category: Category = Category.Experiment,
                     languages: Optional[List[str]] = None,
                     take: int = 18,
                     skip: int = 0,
                    ) -> dict:
    ''' 查询实验
        @param tags: 根据列表内的物实实验的标签进行对应的搜索
        @param exclude_tags: 除了列表内的标签的实验都会被搜索到
        @param category: 实验区还是黑洞区
        @param languages: 根据列表内的语言进行对应的搜索
        @param take: 搜索数量
    '''
```

### 获取实验
```python
def get_experiment(self, content_id: str) -> dict:
    ''' 获取实验
        @param content_id: 不是实验的id, 可通过get_summary()["Data"]["ContentID"]获取
    '''
```

### 确认发布实验
```python
def confirm_experiment(self, summary_id: str, category: Category, image_counter: int) -> dict:
    ''' 确认发布实验
    '''
```

### 发表评论
```python
def post_comment(self, target_id: str, content: str, target_type: str, reply_id: str = "") -> dict:
    ''' 发表评论
        @param target_id: 目标用户/实验的ID
        @param content: 评论内容
        @param target_type: User, Discussion, Experiment
        @param reply_id: 被回复的user的ID (可被自动推导)
    '''
```

### 获取留言板信息
```python
def get_comments(self,
                 id: str,
                 target_type: str,
                 take: int = 16,
                 skip: int = 0,
                ) -> dict:
    ''' 获取留言板信息
        @param id: 物实用户的ID/实验的id
        @param target_type: User, Discussion, Experiment
        @param take: 获取留言的数量
        @param skip: 跳过的留言数量, 为(unix时间戳 * 1000)
    '''
```

### 获取实验介绍
```python
def get_summary(self, content_id: str, category: Category) -> dict:
    ''' 获取实验介绍
        @param content_id: 实验ID
        @param category: 实验区还是黑洞区
    '''
```

### 获取作品的详细信息
```python
def get_derivatives(self, content_id: str, category: Category) -> dict:
    ''' 获取作品的详细信息, 物实第一次读取作品是会使用此接口
        @param content_id: 实验ID
        @param category: 实验区还是黑洞区
    '''
```

### 获取用户信息
```python
def get_user(self,
             user_id: Optional[str] = None,
             name: Optional[str] = None,
            ) -> dict:
    ''' 获取用户信息
        @param user_id: 用户ID
        @param name: 用户名
    '''
```

### 获取用户资料
```python
def get_profile(self) -> dict:
```

### 添加收藏
```python
def star(self, content_id: str, category: Category, status: bool = True) -> dict:
    ''' 添加收藏
        @param content_id: 实验的ID
        @param category: 实验区, 黑洞区
        @param status: True: 收藏, False: 取消收藏
    '''
```

### 上传实验图片
```python
def upload_image(self, policy: str, authorization: str, image_path: str) -> dict:
    ''' 上传实验图片
        @policy @authorization 可通过/Contents/SubmitExperiment获取
        @param image_path: 待上传的图片在本地的路径
    '''
```

### 获取用户收到的消息
```python
def get_messages(self,
                 category_id: int = 0,
                 skip: int = 0,
                 take: int = 16,
                 no_templates: bool = True,
                ) -> dict:
    ''' 获取用户收到的消息
        @param category_id: 消息类型:
            0: 全部, 1: 系统邮件, 2: 评论和回复, 3: 关注和粉丝, 4: 作品通知, 5: 管理记录
        @param skip: 传入一个时间戳, 跳过skip条消息
        @param take: 取take条消息
    '''
```

### 获取支持列表
```python
def get_supporters(self,
                   content_id: str,
                   category: Category,
                   skip: int = 0,
                   take: int = 16,
                  ) -> dict:
    ''' 获取支持列表
        @param category: .Experiment 或 .Discussion
        @param skip: 传入一个时间戳, 跳过skip条消息
        @param take: 取take条消息
    '''
```

### 获取用户的关注/粉丝列表
```python
def get_relations(self,
                  user_id: str,
                  display_type: str = "Follower",
                  skip: int = 0,
                  take: int = 20,
                  query: str = "",
                 ) -> dict:
    ''' 获取用户的关注/粉丝列表
        @param display_type: 只能为 Follower: 粉丝, Following: 关注
        @param skip: 跳过skip个用户
        @param take: 取take个用户
        @param query: 为用户id或昵称
    '''
```

### 关注用户
```python
def follow(self, target_id: str, action: bool = True) -> dict:
    ''' 关注用户
        @param target_id: 被关注的用户的id
        @param action: true为关注, false为取消关注
    '''
```

### 修改用户昵称
```python
def rename(self, nickname: str) -> dict:
    ''' 修改用户昵称
        @param nickname: 新昵称
    '''
```

### 领取每日签到奖励
```python
def receive_bonus(self) -> dict:
    ''' 领取每日签到奖励
    '''
```
