# -*- coding: utf-8 -*-
''' 对物实网络api的封装
    除了上传实验的api的封装在class Experiment的__upload
    该文件提供多线程风格的api的调用方式的支持
'''

import os
import requests

from physicsLab import plAR
from physicsLab import errors
from physicsLab.enums import Tag, Category
from physicsLab._typing import Optional, List, TypedDict, Callable

def _check_response(response: requests.Response, err_callback: Optional[Callable] = None) -> dict:
    ''' 检查返回的response
        @callback: 自定义物实返回的status对应的报错信息,
                    要求传入status_code(捕获物实返回体中的status_code), 无返回值
    '''
    assert err_callback is None or callable(err_callback)

    response.raise_for_status()

    response_json = response.json()
    status_code = response_json["Status"]

    if status_code == 200:
        return response_json
    if err_callback is not None:
        err_callback(status_code)
    raise errors.ResponseFail(
        f"Physics-Lab-AR returned error code {status_code}: {response_json['Message']}"
    )

def get_start_page() -> dict:
    ''' 获取主页数据 '''
    response = requests.get("https://physics-api-cn.turtlesim.com/Users")

    return _check_response(response)

def get_avatar(target_id: str, index: int, category: str, size_category: str) -> bytes:
    ''' 获取头像/实验封面
        @param target_id: 用户id或实验id
        @param index: 历史图片的索引
        @param category: 只能为 "experiments" 或 "users"
        @param size_category: 只能为 "small.round" 或 "thumbnail" 或 "full"
    '''
    if not isinstance(target_id, str) \
            or not isinstance(index, int) \
            or not isinstance(category, str) \
            or not isinstance(size_category, str):
        raise TypeError
    if category not in ("experiments", "users"):
        raise ValueError
    if size_category not in ("small.round", "thumbnail", "full"):
        raise ValueError

    if category == "users":
        category += "/avatars"
    elif category == "experiments":
        category += "/images"
    else:
        assert False

    response = requests.get(
        f"http://physics-static-cn.turtlesim.com:80/{category}"
        f"/{target_id[0:4]}/{target_id[4:6]}/{target_id[6:8]}/{target_id[8:]}/{index}.jpg!{size_category}",
    )

    if b'<Error>' in response.content:
        raise IndexError("avatar not found")
    return response.content

class _login_res(TypedDict):
    Token: str
    AuthCode: str
    Data: dict

# TODO 进一步封装发送请求的函数
class _User:
    ''' 该class仅提供阻塞的api '''
    def __init__(
            self,
            email: Optional[str] = None,
            password: Optional[str] = None,
            /, *,
            token: Optional[str] = None,
            auth_code: Optional[str] = None,
    ) -> None:
        ''' 邮箱密码登录:
            @param email: 邮箱
            @param password: 密码
            @usage: User(YOUR_EMAIL, YOUR_PASSWORD)

            token / auth_code登录:
            @usage: User(token=YOUR_TOKEN, auth_code=YOUR_AUTH_CODE)

            临时的匿名账号 (权限受限):
            @usage: User()
        '''
        if not isinstance(email, (str, type(None))) \
                or not isinstance(password, (str, type(None))) \
                or not isinstance(token, (str, type(None))) \
                or not isinstance(auth_code, (str, type(None))):
            raise TypeError

        if token is not None and auth_code is not None:
            # 只有登录一定会返回auth_code, 其他api返回的AuthCode可能是无效的None
            self.token = token
            self.auth_code = auth_code
            tmp = self.__login()
        else:
            tmp = self.__login(email, password)
            self.token = tmp["Token"]
            self.auth_code = tmp["AuthCode"]

        # True: 绑定了账号; False: 未绑定账号，是匿名登录
        self.is_binded: bool = tmp["Data"]["User"]["IsBinded"]
        # 硬件指纹
        self.device_token: str = tmp["Data"]["DeviceToken"]
        # 账号id
        self.user_id: str = tmp["Data"]["User"]["ID"]
        # 昵称
        self.nickname: Optional[str] = tmp["Data"]["User"]["Nickname"]
        # 签名
        self.signature: Optional[str] = tmp["Data"]["User"]["Signature"]
        # 金币数量
        self.gold: int = tmp["Data"]["User"]["Gold"]
        # 用户等级
        self.level: int = tmp["Data"]["User"]["Level"]
        # 头像的索引
        self.avatar: int = tmp["Data"]["User"]["Avatar"]
        self.avatar_region: int = tmp["Data"]["User"]["AvatarRegion"]
        self.decoration: int = tmp["Data"]["User"]["Decoration"]
        self.verification = tmp["Data"]["User"]["Verification"]
        # 存储了所有与每日活动有关的奖励信息 (比如ActivityID)
        self.statistic: dict = tmp["Data"]["Statistic"]

    def __login(
            self,
            email: Optional[str] = None,
            password: Optional[str] = None,
    ) -> _login_res:
        ''' 登录, 默认为匿名登录

            通过返回字典的Token与AuthCode实现登陆
        '''
        assert isinstance(email, (str, type(None))) and isinstance(password, (str, type(None)))

        plar_version = plAR.get_plAR_version()
        if plar_version is not None:
            plar_version = int(f"{plar_version[0]}{plar_version[1]}{plar_version[2]}")
        else:
            plar_version = 2411

        headers = {
            "Content-Type": "application/json",
        }
        if hasattr(self, "token") and hasattr(self, "auth_code"):
            headers["x-API-Token"] = self.token
            headers["x-API-AuthCode"] = self.auth_code

        response = requests.post(
            "http://physics-api-cn.turtlesim.com/Users/Authenticate",
            json={
                "Login": email,
                "Password": password,
                "Version": plar_version,
                "Device": {
                    "Identifier": "7db01528cf13e2199e141c402d79190e",
                    "Language": "Chinese"
                },
            },
            headers=headers,
        )

        return _check_response(response)

    def get_library(self) -> dict:
        ''' 获取社区作品列表 '''
        response = requests.post(
            "https://physics-api-cn.turtlesim.com/Contents/GetLibrary",
            json={
                "Identifier": "Discussions",
                "Language": "Chinese",
            },
            headers={
                "Content-Type": "application/json",
                "x-API-Token": self.token,
                "x-API-AuthCode": self.auth_code,
            }
        )

        return _check_response(response)

    def query_experiments(
            self,
            category: Category,
            tags: Optional[List[Tag]] = None,
            exclude_tags: Optional[List[Tag]] = None,
            languages: Optional[List[str]] = None,
            exclude_languages: Optional[List[str]] = None,
            user_id: Optional[str] = None,
            take: int = 20,
            skip: int = 0,
            from_skip: Optional[str] = None,
    ) -> dict:
        ''' 查询实验
            @param category: 实验区还是黑洞区
            @param tags: 根据列表内的物实实验的标签进行对应的搜索
            @param exclude_tags: 除了列表内的标签的实验都会被搜索到
            @param languages: 根据列表内的语言进行对应的搜索
            @param exclude_languages: 除了列表内的语言的实验都会被搜索到
            @param user_id: 指定搜索的作品的发布者
            @param take: 搜索数量
            @param skip: 跳过搜索数量
        '''
        if not isinstance(category, Category) \
                or not isinstance(tags, (list, type(None))) \
                or tags is not None and not all(isinstance(tag, Tag) for tag in tags) \
                or not isinstance(exclude_tags, (list, type(None))) \
                or exclude_tags is not None and not all(isinstance(tag, Tag) for tag in exclude_tags) \
                or not isinstance(languages, (list, type(None))) \
                or languages is not None and not all(isinstance(language, str) for language in languages) \
                or not isinstance(exclude_languages, (list, type(None))) \
                or exclude_languages is not None \
                and not all(isinstance(language, str) for language in exclude_languages) \
                or not isinstance(user_id, (str, type(None))) \
                or not isinstance(take, int) \
                or not isinstance(skip, int) \
                or not isinstance(from_skip, (str, type(None))):
            raise TypeError

        if languages is None:
            languages = []
        if exclude_languages is None:
            exclude_languages = []

        if tags is None:
            _tags = None
        else:
            _tags = [tag.value for tag in tags]

        if exclude_tags is None:
            _exclude_tags = exclude_tags
        else:
            _exclude_tags = [tag.value for tag in exclude_tags]

        response = requests.post(
            "http://physics-api-cn.turtlesim.com/Contents/QueryExperiments",
            json={
                "Query": {
                    "Category": category.value,
                    "Languages": languages,
                    "ExcludeLanguages": exclude_languages,
                    "Tags": _tags,
                    "ExcludeTags": _exclude_tags,
                    "ModelTags": None,
                    "ModelID": None,
                    "ParentID": None,
                    "UserID": user_id,
                    "Special": None,
                    "From": from_skip,
                    "Skip": skip,
                    "Take": take,
                    "Days": 0,
                    "Sort": 0, # TODO 这个也许是那个史上热门之类的?
                    "ShowAnnouncement": False,
                }
            },
            headers={
                "Content-Type": "application/json",
                "x-API-Token": self.token,
                "x-API-AuthCode": self.auth_code,
            },
        )

        return _check_response(response)

    def get_experiment(
            self,
            content_id: str,
            category: Optional[Category] = None,
    ) -> dict:
        ''' 获取实验
            @param content_id: 当category不为None时, content_id为实验ID,
                               否则会被识别为get_summary()["Data"]["ContentID"]的结果
            @param category: 实验区还是黑洞区
        '''
        if not isinstance(content_id, str) \
                or not isinstance(category, (Category, type(None))):
            raise TypeError

        if category is not None:
            # 如果传入的是实验ID, 先获取summary来得到ContentID
            content_id = self.get_summary(content_id, category)["Data"]["ContentID"]

        response = requests.post(
            "https://physics-api-cn.turtlesim.com:443/Contents/GetExperiment",
            json={
                "ContentID": content_id,
            },
            headers={
                "Content-Type": "application/json",
                "x-API-Token": self.token,
                "x-API-AuthCode":self.auth_code,
            }
        )

        return _check_response(response)

    def confirm_experiment(self, summary_id: str, category: Category, image_counter: int) -> dict:
        ''' 确认发布实验
        '''
        if not isinstance(summary_id, str) \
                or not isinstance(category, Category) \
                or not isinstance(image_counter, int):
            raise TypeError

        response = requests.post(
            "https://physics-api-cn.turtlesim.com/Contents/ConfirmExperiment",
            json={
                "SummaryID": summary_id,
                "Category": category.value,
                "Image": image_counter,
                "Extension": ".jpg",
            },
            headers={
                "Content-Type": "application/json",
                "x-API-Token": self.token,
                "x-API-AuthCode":self.auth_code,
            }
        )

        return _check_response(response)

    def remove_experiment(self, summary_id: str, category: Category, reason: Optional[str] = None) -> dict:
        ''' 隐藏实验
            @param summary_id: 实验ID
            @param category: 实验区还是黑洞区
        '''
        if not isinstance(summary_id, str) \
                or not isinstance(category, Category) \
                or not isinstance(reason, (str, type(None))):
            raise TypeError

        _plar_ver = plAR.get_plAR_version()
        plar_ver = f"{_plar_ver[0]}{_plar_ver[1]}{_plar_ver[2]}" if _plar_ver is not None else "2411"

        response = requests.post(
            "https://physics-api-cn.turtlesim.com:443/Contents/RemoveExperiment",
            json={
                "Category": category.value,
                "SummaryID": summary_id,
                "Hiding": True,
                "Reason": reason,
            },
            headers={
                "Content-Type": "application/json",
                "x-API-Token": self.token,
                "x-API-AuthCode": self.auth_code,
                "x-API-Version": plar_ver,
            }
        )

        return _check_response(response)

    def post_comment(
            self,
            target_id: str,
            target_type: str,
            content: str,
            reply_id: Optional[str] = None,
    ) -> dict:
        ''' 发表评论
            @param target_id: 目标用户/实验的ID
            @param target_type: User, Discussion, Experiment
            @param content: 评论内容
            @param reply_id: 被回复的user的ID (可被自动推导)
        '''
        if not isinstance(target_id, str) \
                or not isinstance(content, str) \
                or not isinstance(target_type, str) \
                or not isinstance(reply_id, (str, type(None))):
            raise TypeError
        if target_type not in ("User", "Discussion", "Experiment"):
            raise ValueError

        if reply_id is None:
            reply_id = ""

            # 物实支持多语: 中文、英文、法文、德文、西班牙文、日文、乌克兰文、波兰文
            if content.startswith("回复@") \
                    or content.startswith("Reply@") \
                    or content.startswith("Répondre@") \
                    or content.startswith("Antworten@") \
                    or content.startswith("Respuesta@") \
                    or content.startswith("応答@") \
                    or content.startswith("Відповісти@") \
                    or content.startswith("Odpowiadać@"):
                _nickname = ""
                is_match: bool = False
                for chr in content:
                    if chr in (':', ' '):
                        break
                    elif is_match:
                        _nickname += chr
                    elif chr == '@':
                        is_match = True
                        continue

                if _nickname != "":
                    try:
                        reply_id = self.get_user(name=_nickname)["Data"]["User"]["ID"]
                    except errors.ResponseFail:
                        pass

        assert isinstance(reply_id, str)

        response = requests.post(
            "https://physics-api-cn.turtlesim.com:443/Messages/PostComment",
            json={
                "TargetID": target_id,
                "TargetType": target_type,
                "Language": "Chinese",
                "ReplyID": reply_id,
                "Content": content,
                "Special": None
            },
            headers={
                "Content-Type": "application/json",
                "x-API-Token": self.token,
                "x-API-AuthCode": self.auth_code,
            }
        )

        return _check_response(response)

    def remove_comment(self, comment_id: str, target_type: str) -> dict:
        ''' 删除评论
            @param comment_id: 评论ID, 可以通过`get_comments`获取
            @param target_type: User, Discussion, Experiment
        '''
        if not isinstance(comment_id, str) \
                or not isinstance(target_type, str):
            raise TypeError
        if target_type not in ("User", "Discussion", "Experiment"):
            raise ValueError

        response = requests.post(
            "https://physics-api-cn.turtlesim.com:443/Messages/RemoveComment",
            json={
                "TargetType": target_type,
                "CommentID": comment_id,
            },
            headers={
                "Content-Type": "application/json",
                "x-API-Token": self.token,
                "x-API-AuthCode": self.auth_code,
            }
        )

        return _check_response(response)

    def get_comments(
            self,
            target_id: str,
            target_type: str,
            take: int = 16,
            skip: int = 0,
            comment_id: Optional[str] = None,
    ) -> dict:
        ''' 获取评论板信息
            @param target_id: 物实用户的ID/实验的id
            @param target_type: User, Discussion, Experiment
            @param take: 获取留言的数量
            @param skip: 跳过的留言数量, 为(unix时间戳 * 1000)
            @param comment_id: 从comment_id开始获取take条消息 (另一种skip的规则)
        '''
        if not isinstance(self.token, str) \
                or not isinstance(self.auth_code, str) \
                or not isinstance(target_type, str) \
                or not isinstance(take, int) \
                or not isinstance(skip, int) \
                or not isinstance(comment_id, (str, type(None))):
            raise TypeError
        if target_type not in ("User", "Discussion", "Experiment"):
            raise ValueError

        response = requests.post(
            "https://physics-api-cn.turtlesim.com:443/Messages/GetComments",
            json={
                "TargetID": target_id,
                "TargetType": target_type,
                "CommentID": comment_id,
                "Take": take,
                "Skip": skip,
            },
            headers={
                "Content-Type": "application/json",
                "x-API-Token": self.token,
                "x-API-AuthCode": self.auth_code,
            }
        )

        return _check_response(response)

    def get_summary(self, content_id: str, category: Category) -> dict:
        ''' 获取实验介绍
            @param content_id: 实验ID
            @param category: 实验区还是黑洞区
        '''
        if not isinstance(content_id, str) or not isinstance(category, Category):
            raise TypeError

        response = requests.post(
            "https://physics-api-cn.turtlesim.com/Contents/GetSummary",
            json={
                "ContentID": content_id,
                "Category": category.value,
            },
            headers={
                "Content-Type": "application/json",
                "x-API-Token": self.token,
                "x-API-AuthCode": self.auth_code,
            }
        )

        def callback(status_code):
            if status_code == 403:
                raise PermissionError("login failed")
            if status_code == 404:
                raise errors.ResponseFail("experiment not found(may be you select category wrong)")

        return _check_response(response, callback)

    def get_derivatives(self, content_id: str, category: Category) -> dict:
        ''' 获取作品的详细信息, 物实第一次读取作品会使用此接口
            @param content_id: 实验ID
            @param category: 实验区还是黑洞区
        '''
        if not isinstance(content_id, str) or not isinstance(category, Category):
            raise TypeError

        response = requests.post(
            "https://physics-api-cn.turtlesim.com/Contents/GetDerivatives",
            json={
                "ContentID": content_id,
                "Category": category.value,
            },
            headers={
                "Content-Type": "application/json",
                "x-API-Token": self.token,
                "x-API-AuthCode": self.auth_code,
            }
        )

        return _check_response(response)

    def get_user(
            self,
            user_id: Optional[str] = None,
            name: Optional[str] = None,
    ) -> dict:
        ''' 获取用户信息
            @param user_id: 用户ID
            @param name: 用户名
        '''
        if not isinstance(user_id, (str, type(None))) \
                    or not isinstance(name, (str, type(None))):
            raise TypeError
        if user_id is None and name is None:
            raise ValueError("user_id and name can't be None at the same time")

        response = requests.post(
            "https://physics-api-cn.turtlesim.com:443/Users/GetUser",
            json={
                "ID": user_id,
                "Name": name,
            },
            headers={
                "Content-Type": "application/json",
                "x-API-Token": self.token,
                "x-API-AuthCode": self.auth_code,
            }
        )

        return _check_response(response)

    def get_profile(self) -> dict:
        ''' 获取用户主页信息
        '''
        response = requests.post(
            "https://physics-api-cn.turtlesim.com:443/Contents/GetProfile",
            json={
                "ID": self.user_id,
            },
            headers={
                "Content-Type": "application/json",
                "x-API-Token": self.token,
                "x-API-AuthCode": self.auth_code,
            }
        )

        return _check_response(response)

    def star_content(self, content_id: str, category: Category, star_type: int, status: bool = True) -> dict:
        ''' 收藏/支持 某个实验
            @param content_id: 实验ID
            @param category: 实验区, 黑洞区
            @param star_type: 0: 收藏, 1: 使用金币支持实验
            @param status: True: 收藏, False: 取消收藏 (对支持无作用)
        '''
        if not isinstance(content_id, str) \
                or not isinstance(category, Category) \
                or not isinstance(status, bool) \
                or not isinstance(star_type, int):
            raise TypeError
        if star_type not in (0, 1):
            raise ValueError

        response = requests.post(
            "https://physics-api-cn.turtlesim.com/Contents/StarContent",
            json={
                "ContentID": content_id,
                "Status": status,
                "Category": category.value,
                "Type": star_type,
            },
            headers={
                "Content-Type": "application/json",
                "x-API-Token": self.token,
                "x-API-AuthCode": self.auth_code,
            }
        )

        return _check_response(response)

    def upload_image(self, policy: str, authorization: str, image_path: str) -> dict:
        ''' 上传实验图片
            @param authorization: 可通过/Contents/SubmitExperiment获取
            @param image_path: 待上传的图片在本地的路径
        '''
        if policy is None or authorization is None:
            raise RuntimeError("Sorry, Physics-Lab-AR can't upload this iamge")
        if not isinstance(policy, str) \
                or not isinstance(authorization, str) \
                or not isinstance(image_path, str):
            raise TypeError
        if not os.path.exists(image_path) or not os.path.isfile(image_path):
            raise FileNotFoundError

        with open(image_path, "rb") as f:
            data = {
                "policy": (None, policy, None),
                "authorization": (None, authorization, None),
                "file": ("temp.jpg", f, None),
            }
            response = requests.post(
                "http://v0.api.upyun.com/qphysics",
                files=data,
            )
            response.raise_for_status()
            if response.json()["code"] != 200:
                raise errors.ResponseFail(
                    f"Physics-Lab-AR returned error code {response.json()['code']} : "
                    f"{response.json()['message']}"
                )
            return response.json()

    def get_message(self, message_id: str) -> dict:
        ''' 读取系统邮件消息
            @param message_id: 消息的id
        '''
        if not isinstance(message_id, str):
            raise TypeError

        response = requests.post(
            "https://physics-api-cn.turtlesim.com/Messages/GetMessage",
            json={
                "MessageID": message_id,
            },
            headers={
                "Content-Type": "application/json",
                "x-API-Token": self.token,
                "x-API-AuthCode": self.auth_code,
            },
        )

        return _check_response(response)

    def get_messages(
            self,
            category_id: int,
            skip: int = 0,
            take: int = 16,
            no_templates: bool = True,
    ) -> dict:
        ''' 获取用户收到的消息
            @param category_id: 消息类型:
                0: 全部, 1: 系统邮件, 2: 关注和粉丝, 3: 评论和回复, 4: 作品通知, 5: 管理记录
            @param skip: 跳过skip条消息
            @param take: 取take条消息
            @param no_templates: 是否不返回消息种类的模板消息
        '''
        if category_id not in (0, 1, 2, 3, 4, 5) \
                or not isinstance(skip, int) \
                or not isinstance(take, int) \
                or not isinstance(no_templates, bool):
            raise TypeError

        response = requests.post(
            "https://physics-api-cn.turtlesim.com/Messages/GetMessages",
            json={
                "CategoryID": category_id,
                "Skip": skip,
                "Take": take,
                "NoTemplates": no_templates,
            },
            headers={
                "Content-Type": "application/json",
                "x-API-Token": self.token,
                "x-API-AuthCode": self.auth_code,
            }
        )

        return _check_response(response)

    def get_supporters(
            self,
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
        if not isinstance(content_id, str) \
                or not isinstance(category, Category) \
                or not isinstance(skip, int) \
                or not isinstance(take, int):
            raise TypeError

        response = requests.post(
            "https://physics-api-cn.turtlesim.com/Contents/GetSupporters",
            json={
                "ContentID": content_id,
                "Category": category.value,
                "Skip": skip,
                "Take": take,
            },
            headers={
                "Content-Type": "application/json",
                "x-API-Token": self.token,
                "x-API-AuthCode": self.auth_code,
            }
        )

        return _check_response(response)

    def get_relations(
            self,
            user_id: str,
            display_type: str = "Follower",
            skip: int = 0,
            take: int = 20,
            query: str = "", # TODO 获取编辑，志愿者列表啊之类的貌似也是这个api
    ) -> dict:
        ''' 获取用户的关注/粉丝列表
            @param display_type: 只能为 Follower: 粉丝, Following: 关注
            @param skip: 跳过skip个用户
            @param take: 取take个用户
            @param query: 为用户id或昵称
        '''
        if display_type not in ("Follower, Following") \
                or not isinstance(user_id, str) \
                or not isinstance(skip, int) \
                or not isinstance(take, int):
            raise TypeError

        if display_type == "Follower":
            display_type_ = 0
        elif display_type == "Following":
            display_type_ = 1
        else:
            assert False

        response = requests.post(
            "https://physics-api-cn.turtlesim.com:443/Users/GetRelations",
            json={
                "UserID": user_id,
                "DisplayType": display_type_,
                "Skip": skip,
                "Take": take,
                "Query": query,
            },
            headers={
                "Content-Type": "application/json",
                "x-API-Token": self.token,
                "x-API-AuthCode": self.auth_code,
            }
        )

        return _check_response(response)

    def follow(self, target_id: str, action: bool = True) -> dict:
        ''' 关注用户
            @param target_id: 被关注的用户的id
            @param action: true为关注, false为取消关注
        '''
        if not isinstance(target_id, str) \
                or not isinstance(action, bool):
            raise TypeError

        response = requests.post(
            "https://physics-api-cn.turtlesim.com:443/Users/Follow",
            json={
                "TargetID": target_id,
                "Action": int(action),
            },
            headers={
                "Content-Type": "application/json",
                "x-API-Token": self.token,
                "x-API-AuthCode": self.auth_code,
            },
        )

        return _check_response(response)

    def rename(self, nickname: str) -> dict:
        ''' 修改用户昵称
            @param nickname: 新昵称
        '''
        if not isinstance(nickname, str):
            raise TypeError

        response = requests.post(
            "https://physics-api-cn.turtlesim.com:443/Users/Rename",
            json={
                "Target": nickname,
                "UserID": self.user_id,
            },
            headers={
                "Content-Type": "application/json",
                "x-API-Token": self.token,
                "x-API-AuthCode": self.auth_code,
            },
       )

        return _check_response(response)

    def modify_information(self, target: str) -> dict:
        ''' 修改用户签名
            @param target: 新签名
        '''
        if not isinstance(target, str):
            raise TypeError

        response = requests.post(
            "https://physics-api-cn.turtlesim.com:443/Users/ModifyInformation",
            json={
                "Target": target,
                "Field":"Signature",
            },
            headers={
                "Content-Type": "application/json",
                "x-API-Token": self.token,
                "x-API-AuthCode": self.auth_code,
            },
       )

        return _check_response(response)

    def receive_bonus(self, activity_id: str, index: int) -> dict:
        ''' 领取每日签到奖励
            @param activity_id: 活动id
            @param index: 该活动的第几次奖励
        '''
        if not isinstance(activity_id, str) \
                or not isinstance(index, int):
            raise TypeError
        if index < 0:
            raise ValueError

        response = requests.post(
            "https://physics-api-cn.turtlesim.com:443/Users/ReceiveBonus",
            json={
                "ActivityID": activity_id,
                "Index": index,
                "Statistic": self.statistic,
            },
            headers={
                "Content-Type": "application/json",
                "x-API-Token": self.token,
                "x-API-AuthCode": self.auth_code,
            },
        )

        return _check_response(response)
