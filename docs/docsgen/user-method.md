
## 封禁用户
```Python
def ban(self, target_id: str, reason: str, length: int) -> physicsLab.web._api._api_result
```

Args:
*  target_id: 要封禁的用户的id
*  reason: 封禁理由
*  length: 封禁天数

Returns:
*  _api_result: 物实api返回体结构

对应的协程风格的api:
```Python
async def async_ban(self, target_id: str, reason: str, length: int) -> Awaitable[physicsLab.web._api._api_result]
```

## 确认发布实验
```Python
def confirm_experiment(self, summary_id: str, category: physicsLab.enums.Category, image_counter: int) -> physicsLab.web._api._api_result
```

Args:
*  summary_id: 摘要ID
*  category: 实验区还是黑洞区
*  image_counter: 图片计数器

Returns:
*  _api_result: 物实api返回体结构

Notes:
*  低级API, 请勿直接使用
*  使用Experiment.update()与Experiment.upload()方法来发布实验

对应的协程风格的api:
```Python
async def async_confirm_experiment(self, summary_id: str, category: physicsLab.enums.Category, image_counter: int) -> Awaitable[physicsLab.web._api._api_result]
```

## 关注用户
```Python
def follow(self, target_id: str, action: bool = True) -> physicsLab.web._api._api_result
```

Args:
*  target_id: 被关注的用户的id
*  action: true为关注, false为取消关注

Returns:
*  _api_result: 物实api返回体结构

对应的协程风格的api:
```Python
async def async_follow(self, target_id: str, action: bool = True) -> Awaitable[physicsLab.web._api._api_result]
```

## 获取评论板信息
```Python
def get_comments(self, target_id: str, target_type: str, take: int = 16, skip: int = 0, comment_id: Optional[str] = None) -> physicsLab.web._api._api_result
```

Args:
*  target_id: 物实用户的ID/实验的id
*  target_type: User, Discussion, Experiment
*  take: 获取留言的数量
*  skip: 跳过的留言数量, 为(unix时间戳 * 1000)
*  comment_id: 从comment_id开始获取take条消息 (另一种skip的规则)

Returns:
*  _api_result: 物实api返回体结构

对应的协程风格的api:
```Python
async def async_get_comments(self, target_id: str, target_type: str, take: int = 16, skip: int = 0, comment_id: Optional[str] = None) -> Awaitable[physicsLab.web._api._api_result]
```

## 获取作品的详细信息, 物实第一次读取作品会使用此接口
```Python
def get_derivatives(self, content_id: str, category: physicsLab.enums.Category) -> physicsLab.web._api._api_result
```

Args:
*  content_id: 实验ID
*  category: 实验区还是黑洞区

Returns:
*  _api_result: 物实api返回体结构

对应的协程风格的api:
```Python
async def async_get_derivatives(self, content_id: str, category: physicsLab.enums.Category) -> Awaitable[physicsLab.web._api._api_result]
```

## 获取实验
```Python
def get_experiment(self, content_id: str, category: Optional[physicsLab.enums.Category] = None) -> physicsLab.web._api._api_result
```

Args:
*  content_id: 当category不为None时, content_id为实验ID,
*  否则会被识别为get_summary()["Data"]["ContentID"]的结果
*  category: 实验区还是黑洞区

Returns:
*  _api_result: 物实api返回体结构

对应的协程风格的api:
```Python
async def async_get_experiment(self, content_id: str, category: Optional[physicsLab.enums.Category] = None) -> Awaitable[physicsLab.web._api._api_result]
```

## 获取社区作品列表
```Python
def get_library(self) -> physicsLab.web._api._api_result
```

Returns:
*  _api_result: 物实api返回体结构

对应的协程风格的api:
```Python
async def async_get_library(self) -> Awaitable[physicsLab.web._api._api_result]
```

## 读取系统邮件消息
```Python
def get_message(self, message_id: str) -> physicsLab.web._api._api_result
```

Args:
*  message_id: 消息的id

Returns:
*  _api_result: 物实api返回体结构

对应的协程风格的api:
```Python
async def async_get_message(self, message_id: str) -> Awaitable[physicsLab.web._api._api_result]
```

## 获取用户收到的消息
```Python
def get_messages(self, category_id: int, skip: int = 0, take: int = 16, no_templates: bool = True) -> physicsLab.web._api._api_result
```

Args:
*  category_id: 消息类型:
*  0: 全部, 1: 系统邮件, 2: 关注和粉丝, 3: 评论和回复, 4: 作品通知, 5: 管理记录
*  skip: 跳过skip条消息
*  take: 取take条消息
*  no_templates: 是否不返回消息种类的模板消息

Returns:
*  _api_result: 物实api返回体结构

对应的协程风格的api:
```Python
async def async_get_messages(self, category_id: int, skip: int = 0, take: int = 16, no_templates: bool = True) -> Awaitable[physicsLab.web._api._api_result]
```

## 获取用户主页信息
```Python
def get_profile(self) -> physicsLab.web._api._api_result
```

Returns:
*  _api_result: 物实api返回体结构

对应的协程风格的api:
```Python
async def async_get_profile(self) -> Awaitable[physicsLab.web._api._api_result]
```

## 获取用户的关注/粉丝列表
```Python
def get_relations(self, user_id: str, display_type: str = 'Follower', skip: int = 0, take: int = 20, query: str = '') -> physicsLab.web._api._api_result
```

Args:
*  user_id: 用户ID
*  display_type: 只能为 Follower: 粉丝, Following: 关注
*  skip: 跳过skip个用户
*  take: 取take个用户
*  query: 为用户id或昵称

Returns:
*  _api_result: 物实api返回体结构

对应的协程风格的api:
```Python
async def async_get_relations(self, user_id: str, display_type: str = 'Follower', skip: int = 0, take: int = 20, query: str = '') -> Awaitable[physicsLab.web._api._api_result]
```

## 获取实验介绍
```Python
def get_summary(self, content_id: str, category: physicsLab.enums.Category) -> physicsLab.web._api._api_result
```

Args:
*  content_id: 实验ID
*  category: 实验区还是黑洞区

Returns:
*  _api_result: 物实api返回体结构

对应的协程风格的api:
```Python
async def async_get_summary(self, content_id: str, category: physicsLab.enums.Category) -> Awaitable[physicsLab.web._api._api_result]
```

## 获取支持列表
```Python
def get_supporters(self, content_id: str, category: physicsLab.enums.Category, skip: int = 0, take: int = 16) -> physicsLab.web._api._api_result
```

Args:
*  content_id: 内容ID
*  category: .Experiment 或 .Discussion
*  skip: 传入一个时间戳, 跳过skip条消息
*  take: 取take条消息

Returns:
*  _api_result: 物实api返回体结构

对应的协程风格的api:
```Python
async def async_get_supporters(self, content_id: str, category: physicsLab.enums.Category, skip: int = 0, take: int = 16) -> Awaitable[physicsLab.web._api._api_result]
```

## 获取用户信息
```Python
def get_user(self, msg: str, get_user_mode: physicsLab.enums.GetUserMode) -> physicsLab.web._api._api_result
```

Args:
*  msg: 用户ID/用户名
*  get_user_mode: 根据ID/用户名获取用户信息

Returns:
*  _api_result: 物实api返回体结构

对应的协程风格的api:
```Python
async def async_get_user(self, msg: str, get_user_mode: physicsLab.enums.GetUserMode) -> Awaitable[physicsLab.web._api._api_result]
```

## 修改用户签名
```Python
def modify_information(self, target: str) -> physicsLab.web._api._api_result
```

Args:
*  target: 新签名

Returns:
*  _api_result: 物实api返回体结构

对应的协程风格的api:
```Python
async def async_modify_information(self, target: str) -> Awaitable[physicsLab.web._api._api_result]
```

## 发表评论
```Python
def post_comment(self, target_id: str, target_type: str, content: str, reply_id: Optional[str] = None, special: Optional[str] = None) -> physicsLab.web._api._api_result
```

Args:
*  target_id: 目标用户/实验的ID
*  target_type: User, Discussion, Experiment
*  content: 评论内容
*  reply_id: 被回复的user的ID (可被自动推导)
*  special: 为 "Reminder" 的话则是发送警告, 为None则是普通的评论

Returns:
*  _api_result: 物实api返回体结构

对应的协程风格的api:
```Python
async def async_post_comment(self, target_id: str, target_type: str, content: str, reply_id: Optional[str] = None, special: Optional[str] = None) -> Awaitable[physicsLab.web._api._api_result]
```

## 查询实验
```Python
def query_experiments(self, category: physicsLab.enums.Category, tags: Optional[List[physicsLab.enums.Tag]] = None, exclude_tags: Optional[List[physicsLab.enums.Tag]] = None, languages: Optional[List[str]] = None, exclude_languages: Optional[List[str]] = None, user_id: Optional[str] = None, take: int = 20, skip: int = 0, from_skip: Optional[str] = None) -> physicsLab.web._api._api_result
```

Args:
*  category: 实验区还是黑洞区
*  tags: 根据列表内的物实实验的标签进行对应的搜索
*  exclude_tags: 除了列表内的标签的实验都会被搜索到
*  languages: 根据列表内的语言进行对应的搜索
*  exclude_languages: 除了列表内的语言的实验都会被搜索到
*  user_id: 指定搜索的作品的发布者
*  take: 搜索数量
*  skip: 跳过搜索数量
*  from_skip: 起始位置标识符

Returns:
*  _api_result: 物实api返回体结构

对应的协程风格的api:
```Python
async def async_query_experiments(self, category: physicsLab.enums.Category, tags: Optional[List[physicsLab.enums.Tag]] = None, exclude_tags: Optional[List[physicsLab.enums.Tag]] = None, languages: Optional[List[str]] = None, exclude_languages: Optional[List[str]] = None, user_id: Optional[str] = None, take: int = 20, skip: int = 0, from_skip: Optional[str] = None) -> Awaitable[physicsLab.web._api._api_result]
```

## 领取每日签到奖励
```Python
def receive_bonus(self, activity_id: str, index: int) -> physicsLab.web._api._api_result
```

Args:
*  activity_id: 活动id
*  index: 该活动的第几次奖励

Returns:
*  _api_result: 物实api返回体结构

对应的协程风格的api:
```Python
async def async_receive_bonus(self, activity_id: str, index: int) -> Awaitable[physicsLab.web._api._api_result]
```

## 删除评论
```Python
def remove_comment(self, comment_id: str, target_type: str) -> physicsLab.web._api._api_result
```

Args:
*  comment_id: 评论ID, 可以通过`get_comments`获取
*  target_type: User, Discussion, Experiment

Returns:
*  _api_result: 物实api返回体结构

对应的协程风格的api:
```Python
async def async_remove_comment(self, comment_id: str, target_type: str) -> Awaitable[physicsLab.web._api._api_result]
```

## 隐藏实验
```Python
def remove_experiment(self, summary_id: str, category: physicsLab.enums.Category, reason: Optional[str] = None) -> physicsLab.web._api._api_result
```

Args:
*  summary_id: 实验ID
*  category: 实验区还是黑洞区
*  reason: 隐藏原因

Returns:
*  _api_result: 物实api返回体结构

对应的协程风格的api:
```Python
async def async_remove_experiment(self, summary_id: str, category: physicsLab.enums.Category, reason: Optional[str] = None) -> Awaitable[physicsLab.web._api._api_result]
```

## 修改用户昵称
```Python
def rename(self, nickname: str) -> physicsLab.web._api._api_result
```

Args:
*  nickname: 新昵称

Returns:
*  _api_result: 物实api返回体结构

对应的协程风格的api:
```Python
async def async_rename(self, nickname: str) -> Awaitable[physicsLab.web._api._api_result]
```

## 收藏/支持 某个实验
```Python
def star_content(self, content_id: str, category: physicsLab.enums.Category, star_type: int, status: bool = True) -> physicsLab.web._api._api_result
```

Args:
*  content_id: 实验ID
*  category: 实验区, 黑洞区
*  star_type: 0: 收藏, 1: 使用金币支持实验
*  status: True: 收藏, False: 取消收藏 (对支持无作用)

Returns:
*  _api_result: 物实api返回体结构

对应的协程风格的api:
```Python
async def async_star_content(self, content_id: str, category: physicsLab.enums.Category, star_type: int, status: bool = True) -> Awaitable[physicsLab.web._api._api_result]
```

## 解除封禁
```Python
def unban(self, target_id: str, reason: str) -> physicsLab.web._api._api_result
```

Args:
*  target_id: 要解除封禁的用户的id
*  reason: 解封理由

Returns:
*  _api_result: 物实api返回体结构

对应的协程风格的api:
```Python
async def async_unban(self, target_id: str, reason: str) -> Awaitable[physicsLab.web._api._api_result]
```

## 上传实验图片
```Python
def upload_image(self, policy: str, authorization: str, image_path: str) -> physicsLab.web._api._api_result
```

Args:
*  authorization: 可通过/Contents/SubmitExperiment["Data"]["Token"]["Policy"]获取
*  policy: 可通过/Contents/SubmitExperiment的["Data"]["Token"]["Policy"]获取
*  image_path: 待上传的图片在本地的路径

Returns:
*  _api_result: 物实api返回体结构

Notes:
*  该API为低级API, 上传图片推荐使用封装得更加完善的Experiment.upload()与Experiment.update()方法

对应的协程风格的api:
```Python
async def async_upload_image(self, policy: str, authorization: str, image_path: str) -> Awaitable[physicsLab.web._api._api_result]
```
