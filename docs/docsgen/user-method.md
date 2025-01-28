
## 确认发布实验
```Python
def confirm_experiment(self, summary_id: str, category: physicsLab.enums.Category, image_counter: int) -> dict
```

对应的协程风格的api:
```Python
async def async_confirm_experiment(self, summary_id: str, category: physicsLab.enums.Category, image_counter: int)
```

## 关注用户
```Python
def follow(self, target_id: str, action: bool = True) -> dict
```
@param target_id: 被关注的用户的id  
@param action: true为关注, false为取消关注  

对应的协程风格的api:
```Python
async def async_follow(self, target_id: str, action: bool = True)
```

## 获取评论板信息
```Python
def get_comments(self, target_id: str, target_type: str, take: int = 16, skip: int = 0, comment_id: Optional[str] = None) -> dict
```
@param target_id: 物实用户的ID/实验的id  
@param target_type: User, Discussion, Experiment  
@param take: 获取留言的数量  
@param skip: 跳过的留言数量, 为(unix时间戳 * 1000)  
@param comment_id: 从comment_id开始获取take条消息 (另一种skip的规则)  

对应的协程风格的api:
```Python
async def async_get_comments(self, target_id: str, target_type: str, take: int = 16, skip: int = 0)
```

## 获取作品的详细信息, 物实第一次读取作品会使用此接口
```Python
def get_derivatives(self, content_id: str, category: physicsLab.enums.Category) -> dict
```
@param content_id: 实验ID  
@param category: 实验区还是黑洞区  

对应的协程风格的api:
```Python
async def async_get_derivatives(self, content_id: str, category: physicsLab.enums.Category)
```

## 获取实验
```Python
def get_experiment(self, content_id: str, category: Optional[physicsLab.enums.Category] = None) -> dict
```
@param content_id: 当category不为None时, content_id为实验ID,  
否则会被识别为get_summary()["Data"]["ContentID"]的结果  
@param category: 实验区还是黑洞区  

对应的协程风格的api:
```Python
async def async_get_experiment(self, content_id: str, category: Optional[physicsLab.enums.Category] = None) -> dict
```

## 获取社区作品列表 
```Python
def get_library(self) -> dict
```
对应的协程风格的api:
```Python
async def async_get_library(self)
```

## 读取系统邮件消息
```Python
def get_message(self, message_id: str) -> dict
```
@param message_id: 消息的id  

对应的协程风格的api:
```Python
async def async_get_message(self, message_id: str)
```

## 获取用户收到的消息
```Python
def get_messages(self, category_id: int = 0, skip: int = 0, take: int = 16, no_templates: bool = True) -> dict
```
@param category_id: 消息类型:  
0: 全部, 1: 系统邮件, 2: 关注和粉丝, 3: 评论和回复, 4: 作品通知, 5: 管理记录  
@param skip: 跳过skip条消息  
@param take: 取take条消息  

对应的协程风格的api:
```Python
async def async_get_messages(self, category_id: int = 0, skip: int = 0, take: int = 16, no_templates: bool = True)
```

## 获取用户主页信息
```Python
def get_profile(self) -> dict
```

对应的协程风格的api:
```Python
async def async_get_profile(self)
```

## 获取用户的关注/粉丝列表
```Python
def get_relations(self, user_id: str, display_type: str = 'Follower', skip: int = 0, take: int = 20, query: str = '') -> dict
```
@param display_type: 只能为 Follower: 粉丝, Following: 关注  
@param skip: 跳过skip个用户  
@param take: 取take个用户  
@param query: 为用户id或昵称  

对应的协程风格的api:
```Python
async def async_get_relations(self, user_id: str, display_type: str = 'Follower', skip: int = 0, take: int = 20, query: str = '')
```

## 获取实验介绍
```Python
def get_summary(self, content_id: str, category: physicsLab.enums.Category) -> dict
```
@param content_id: 实验ID  
@param category: 实验区还是黑洞区  

对应的协程风格的api:
```Python
async def async_get_summary(self, content_id: str, category: physicsLab.enums.Category)
```

## 获取支持列表
```Python
def get_supporters(self, content_id: str, category: physicsLab.enums.Category, skip: int = 0, take: int = 16) -> dict
```
@param category: .Experiment 或 .Discussion  
@param skip: 传入一个时间戳, 跳过skip条消息  
@param take: 取take条消息  

对应的协程风格的api:
```Python
async def async_get_supporters(self, content_id: str, category: physicsLab.enums.Category, skip: int = 0, take: int = 16)
```

## 获取用户信息
```Python
def get_user(self, user_id: Optional[str] = None, name: Optional[str] = None) -> dict
```
@param user_id: 用户ID  
@param name: 用户名  

对应的协程风格的api:
```Python
async def async_get_user(self, user_id: Optional[str] = None, name: Optional[str] = None)
```

## 修改用户签名
```Python
def modify_info(self, target: str) -> dict
```
@param target: 新签名  

对应的协程风格的api:
```Python
async def async_modify_info(self, target: str)
```

## 发表评论
```Python
def post_comment(self, target_id: str, target_type: str, content: str, reply_id: Optional[str] = None) -> dict
```
@param target_id: 目标用户/实验的ID  
@param target_type: User, Discussion, Experiment  
@param content: 评论内容  
@param reply_id: 被回复的user的ID (可被自动推导)  

对应的协程风格的api:
```Python
async def async_post_comment(self, target_id: str, target_type: str, content: str, reply_id: Optional[str] = None) -> dict
```

## 查询实验
```Python
def query_experiments(self, tags: Optional[List[physicsLab.enums.Tag]] = None, exclude_tags: Optional[List[physicsLab.enums.Tag]] = None, category: physicsLab.enums.Category = <Category.Experiment: 'Experiment'>, languages: Optional[List[str]] = None, user_id: Optional[str] = None, take: int = 18, skip: int = 0) -> dict
```
@param tags: 根据列表内的物实实验的标签进行对应的搜索  
@param exclude_tags: 除了列表内的标签的实验都会被搜索到  
@param category: 实验区还是黑洞区  
@param languages: 根据列表内的语言进行对应的搜索  
@param user_id: 指定搜索的作品的发布者  
@param take: 搜索数量  
@param skip: 跳过搜索数量  

对应的协程风格的api:
```Python
async def async_query_experiments(self, tags: Optional[List[physicsLab.enums.Tag]] = None, exclude_tags: Optional[List[physicsLab.enums.Tag]] = None, category: physicsLab.enums.Category = <Category.Experiment: 'Experiment'>, languages: Optional[List[str]] = None, user_id: Optional[str] = None, take: int = 18, skip: int = 0)
```

## 领取每日签到奖励
```Python
def receive_bonus(self, activity_id: str, index: int) -> dict
```
@param activity_id: 活动id  
@param index: 该活动的第几次奖励  

对应的协程风格的api:
```Python
async def async_receive_bonus(self)
```

## 删除评论
```Python
def remove_comment(self, CommentID: str, target_type: str) -> dict
```
@param CommentID: 评论ID, 可以通过`get_comments`获取  
@param target_type: User, Discussion, Experiment  

对应的协程风格的api:
```Python
async def async_remove_comment(self, CommentID: str, target_type: str)
```

## 修改用户昵称
```Python
def rename(self, nickname: str) -> dict
```
@param nickname: 新昵称  

对应的协程风格的api:
```Python
async def async_rename(self, nickname: str)
```

## 收藏某个实验
```Python
def star(self, content_id: str, category: physicsLab.enums.Category, status: bool = True) -> dict
```
@param content_id: 实验ID  
@param category: 实验区, 黑洞区  
@param status: True: 收藏, False: 取消收藏  

对应的协程风格的api:
```Python
async def async_star(self, content_id: str, category: physicsLab.enums.Category, status: bool = True)
```

## 使用金币支持某实验
```Python
def star_content(self, content_id: str, category: physicsLab.enums.Category, status: bool = True) -> dict
```
@content_id: 实验id  
@category: 实验区还是黑洞区  
@status: 是否支持  
@return: 返回的json数据  

对应的协程风格的api:
```Python
async def async_star_content(self, content_id: str, category: physicsLab.enums.Category, status: bool = True)
```

## 上传实验图片
```Python
def upload_image(self, policy: str, authorization: str, image_path: str) -> dict
```
@param authorization: 可通过/Contents/SubmitExperiment获取  
@param image_path: 待上传的图片在本地的路径  

对应的协程风格的api:
```Python
async def async_upload_image(self, policy: str, authorization: str, image_path: str)
```
