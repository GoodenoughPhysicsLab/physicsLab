# 物实网络api

Functions
---------
```
`get_avatar(id: str, index: int, category: str, size_category: str) ‑> bytes`
:   获取头像/实验封面
    @param id: 用户id或实验id
    @param index: 历史图片的索引
    @param category: 只能为 "experiments" 或 "users"
    @param size_category: 只能为 "small.round" 或 "thumbnail" 或 "full"

`get_start_page() ‑> dict`
:   获取主页数据
```
Classes
-------
```
`User(username: Optional[str] = None, passward: Optional[str] = None, *, token: Optional[str] = None, auth_code: Optional[str] = None)`
:   
```

### Methods

    `confirm_experiment(self, summary_id: str, category: physicsLab.enums.Category, image_counter: int) ‑> dict`
    :   确认发布实验

    `get_comments(self, id: str, target_type: str, take: int = 16, skip: int = 0) ‑> dict`
    :   获取留言板信息
        @param id: 物实用户的ID/实验的id
        @param target_type: User, Discussion, Experiment
        @param take: 获取留言的数量
        @param skip: 跳过的留言数量, 为(unix时间戳 * 1000)

    `get_derivatives(self, content_id: str, category: physicsLab.enums.Category) ‑> dict`
    :   获取作品的详细信息, 物实第一次读取作品是会使用此接口
        @param content_id: 实验ID
        @param category: 实验区还是黑洞区

    `get_experiment(self, content_id: str) ‑> dict`
    :   获取实验
        @param content_id: 不是实验的id, 可通过get_summary()["Data"]["ContentID"]获取

    `get_library(self) ‑> dict`
    :   获取社区作品列表

    `get_messages(self, category_id: int = 0, skip: int = 0, take: int = 16, no_templates: bool = True) ‑> dict`
    :   获取用户收到的消息
        @param category_id: 消息类型:
            0: 全部, 1: 系统邮件, 2: 评论和回复, 3: 关注和粉丝, 4: 作品通知, 5: 管理记录
        @param skip: 传入一个时间戳, 跳过skip条消息
        @param take: 取take条消息

    `get_profile(self) ‑> dict`
    :

    `get_relations(self, user_id: str, display_type: str = 'Follower', skip: int = 0, take: int = 20) ‑> dict`
    :   获取用户的关注/粉丝列表
        @param display_type: 只能为 Follower: 粉丝, Following: 关注
        @param skip: 传入一个时间戳, 跳过skip条消息
        @param take: 取take条消息

    `get_summary(self, content_id: str, category: physicsLab.enums.Category) ‑> dict`
    :   获取实验介绍
        @param content_id: 实验ID
        @param category: 实验区还是黑洞区

    `get_supporters(self, content_id: str, category: physicsLab.enums.Category, skip: int = 0, take: int = 16) ‑> dict`
    :   获取支持列表
        @param category: .Experiment 或 .Discussion
        @param skip: 传入一个时间戳, 跳过skip条消息
        @param take: 取take条消息

    `get_user(self, user_id: Optional[str] = None, name: Optional[str] = None) ‑> dict`
    :   获取用户信息
        @param user_id: 用户ID
        @param name: 用户名

    `post_comment(self, target_id: str, content: str, target_type: str, reply_id: str = '') ‑> dict`
    :   发表评论
        @param target_id: 目标用户/实验的ID
        @param content: 评论内容
        @param target_type: User, Discussion, Experiment
        @param reply_id: 被回复的user的ID

    `query_experiment(self, tags: Optional[List[physicsLab.enums.Tag]] = None, exclude_tags: Optional[List[physicsLab.enums.Tag]] = None, category: physicsLab.enums.Category = Category.Experiment, languages: Optional[List[str]] = None, take: int = 18, skip: int = 0) ‑> dict`
    :   查询实验
        @param tags: 根据列表内的物实实验的标签进行对应的搜索
        @param exclude_tags: 除了列表内的标签的实验都会被搜索到
        @param category: 实验区还是黑洞区
        @param languages: 根据列表内的语言进行对应的搜索
        @param take: 搜索数量

    `star(self, content_id: str, category: physicsLab.enums.Category, status: bool = True) ‑> dict`
    :   添加收藏
        @param content_id: 实验的ID
        @param category: 实验区, 黑洞区
        @param status: True: 收藏, False: 取消收藏

    `upload_image(self, policy: str, authorization: str, image_path: str) ‑> dict`
    :   上传实验图片
        @policy @authorization 可通过/Contents/SubmitExperiment获取
        @param image_path: 待上传的图片在本地的路径