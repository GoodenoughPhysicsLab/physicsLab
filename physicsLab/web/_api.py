# -*- coding: utf-8 -*-
''' 对物实网络api的封装
    除了上传实验的api的封装在class Experiment的__upload
    该文件提供多线程风格的api的调用方式的支持
'''

import os
import requests

from physicsLab import plAR
from physicsLab import enums
from physicsLab import errors
from physicsLab.enums import Tag, Category
from physicsLab._typing import Optional, List, TypedDict, Callable

class _api_result(TypedDict):
    ''' 物实api返回体的结构
        @param Token: 令牌
        @param AuthCode: 鉴权码
        @param Data: 实际返回的数据
    '''
    Token: str
    AuthCode: Optional[str]
    Data: dict

def _check_response(response: requests.Response, err_callback: Optional[Callable] = None) -> _api_result:
    ''' 检查返回的response
        @callback: 自定义物实返回的status对应的报错信息,
                    要求传入status_code(捕获物实返回体中的status_code), 无返回值
    '''
    errors.assert_true(err_callback is None or callable(err_callback))

    response.raise_for_status()

    response_json = response.json()
    status_code = response_json["Status"]

    if status_code == 200:
        return response_json
    if err_callback is not None:
        err_callback(status_code)
    raise errors.ResponseFail(
        f"Physics-Lab-AR's server returned error code {status_code}: {response_json['Message']}"
    )

def get_start_page() -> _api_result:
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
    if not isinstance(target_id, str):
        errors.type_error(f"Parameter `target_id` must be of type `str`, but got value `{target_id}` of type `{type(target_id).__name__}`")
    if not isinstance(index, int):
        errors.type_error(f"Parameter `index` must be of type `int`, but got value `{index}` of type `{type(index).__name__}`")
    if not isinstance(category, str):
        errors.type_error(f"Parameter `category` must be of type `str`, but got value `{category}` of type `{type(category).__name__}`")
    if not isinstance(size_category, str):
        errors.type_error(f"Parameter `size_category` must be of type `str`, but got value `{size_category}` of type `{type(size_category).__name__}`")
    if category not in ("experiments", "users"):
        raise ValueError(f"Parameter `category` must be one of ['experiments', 'users'], but got value `{category} of type '{category}'")
    if size_category not in ("small.round", "thumbnail", "full"):
        raise ValueError(f"Parameter `size_category` must be one of ['small.round', 'thumbnail', 'full'], but got value `{size_category} of type '{size_category}'")

    if category == "users":
        category += "/avatars"
    elif category == "experiments":
        category += "/images"
    else:
        errors.unreachable()

    response = requests.get(
        f"http://physics-static-cn.turtlesim.com:80/{category}"
        f"/{target_id[0:4]}/{target_id[4:6]}/{target_id[6:8]}/{target_id[8:]}/{index}.jpg!{size_category}",
    )

    if b'<Error>' in response.content:
        raise IndexError("avatar not found")
    return response.content

# TODO 进一步封装发送请求的函数
class _User:
    ''' 该class仅提供阻塞的api '''
    token: str
    auth_code: str
    # True: 绑定了账号; False: 未绑定账号，是匿名登录
    is_binded: bool
    # 硬件指纹
    device_token: str
    # 账号id
    user_id: str
    # 昵称
    nickname: Optional[str]
    # 签名
    signature: Optional[str]
    # 金币数量
    gold: int
    # 用户等级
    level: int
    # 头像的索引
    avatar: int
    avatar_region: int
    decoration: int
    # 存储了所有与每日活动有关的奖励信息 (比如ActivityID)
    statistic: dict

    def __init__(*args, **kwargs) -> None:
        raise NotImplementedError

    def get_library(self) -> _api_result:
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
    ) -> _api_result:
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
        if not isinstance(category, Category):
            errors.type_error(f"Parameter `category` must be an instance of Category enum, but got value `{category}` of type `{type(category).__name__}`")
        if not isinstance(tags, (list, type(None))):
            errors.type_error(f"Parameter `tags` must be of type 'list' or None, but got value `{tags}` of type `{type(tags).__name__}`")
        if tags is not None and not all(isinstance(tag, Tag) for tag in tags):
            errors.type_error(f"Parameter `tags` must be a list of Tag enum instances, but got value `{tags} of type list containing non-Tag elements")
        if not isinstance(exclude_tags, (list, type(None))):
            errors.type_error(f"Parameter `exclude_tags` must be of type 'list' or None, but got value `{exclude_tags}` of type `{type(exclude_tags).__name__}`")
        if exclude_tags is not None and not all(isinstance(tag, Tag) for tag in exclude_tags):
            errors.type_error(f"Parameter `exclude_tags` must be a list of Tag enum instances, but got value `{exclude_tags} of type list containing non-Tag elements")
        if not isinstance(languages, (list, type(None))):
            errors.type_error(f"Parameter `languages` must be of type `Optional[list]`, but got value `{languages}` of type `{type(languages).__name__}`")
        if languages is not None and not all(isinstance(language, str) for language in languages):
            errors.type_error(f"Parameter `languages` must be type `list | str`, but got value `{languages}` of type `{type(languages).__name__}`")
        if not isinstance(exclude_languages, (list, type(None))):
            errors.type_error(f"Parameter `exclude_languages` must be of type `Optional[list]`, but got value `{exclude_languages}` of type `{type(exclude_languages).__name__}`")
        if exclude_languages is not None and not all(isinstance(language, str) for language in exclude_languages):
            errors.type_error(f"Parameter `exclude_languages` must be a list of str, but got value `{exclude_languages} of type list containing non-str elements")
        if not isinstance(user_id, (str, type(None))):
            errors.type_error(f"Parameter `user_id` must be of type `str` or None, but got value `{user_id}` of type {type(user_id).__name__}`")
        if not isinstance(take, int):
            errors.type_error(f"Parameter `take` must be of type `int`, but got value `{take}` of type `{type(take).__name__}`")
        if not isinstance(skip, int):
            errors.type_error(f"Parameter `skip` must be of type `int`, but got value `{skip}` of type `{type(skip).__name__}`")
        if not isinstance(from_skip, (str, type(None))):
            errors.type_error(f"Parameter `from_skip` must be of type `str` or None, but got value `{from_skip}` of type `{type(from_skip).__name__}`")

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
    ) -> _api_result:
        ''' 获取实验
            @param content_id: 当category不为None时, content_id为实验ID,
                               否则会被识别为get_summary()["Data"]["ContentID"]的结果
            @param category: 实验区还是黑洞区
        '''
        if not isinstance(content_id, str):
            errors.type_error(f"Parameter `content_id` must be of type `str`, but got value `{content_id}` of type `{type(content_id).__name__}`")
        if not isinstance(category, (Category, type(None))):
            errors.type_error(f"Parameter `category` must be an instance of Category enum or None, but got value `{category}` of type `{type(category).__name__}`")

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

    def confirm_experiment(self, summary_id: str, category: Category, image_counter: int) -> _api_result:
        ''' 确认发布实验
        '''
        if not isinstance(summary_id, str):
            errors.type_error(f"Parameter `summary_id` must be of type `str`, but got value `{summary_id}` of type `{type(summary_id).__name__}`")
        if not isinstance(category, Category):
            errors.type_error(f"Parameter `category` must be an instance of Category enum, but got value `{category}` of type `{type(category).__name__}`")
        if not isinstance(image_counter, int):
            errors.type_error(f"Parameter `image_counter` must be of type `int`, but got value `{image_counter}` of type `{type(image_counter).__name__}`")

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

    def remove_experiment(self, summary_id: str, category: Category, reason: Optional[str] = None) -> _api_result:
        ''' 隐藏实验
            @param summary_id: 实验ID
            @param category: 实验区还是黑洞区
        '''
        if not isinstance(summary_id, str):
            errors.type_error(f"Parameter `summary_id` must be of type `str`, but got value `{summary_id}` of type `{type(summary_id).__name__}`")
        if not isinstance(category, Category):
            errors.type_error(f"Parameter `category` must be an instance of Category enum, but got value `{category}` of type `{type(category).__name__}`")
        if not isinstance(reason, (str, type(None))):
            errors.type_error(f"Parameter `reason` must be of type `str` or None, but got value `{reason}` of type `{type(reason).__name__}`")

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
            special: Optional[str] = None,
    ) -> _api_result:
        ''' 发表评论
            @param target_id: 目标用户/实验的ID
            @param target_type: User, Discussion, Experiment
            @param content: 评论内容
            @param reply_id: 被回复的user的ID (可被自动推导)
            @param special: 为 "Reminder" 的话则是发送警告, 为None则是普通的评论
        '''
        if not isinstance(target_id, str):
            errors.type_error(f"Parameter `target_id` must be of type `str`, but got value `{target_id}` of type `{type(target_id).__name__}`")
        if not isinstance(content, str):
            errors.type_error(f"Parameter `content` must be of type `str`, but got value `{content}` of type `{type(content).__name__}`")
        if not isinstance(target_type, str):
            errors.type_error(f"Parameter `target_type` must be of type `str`, but got value `{target_type}` of type `{type(target_type).__name__}`")
        if not isinstance(reply_id, (str, type(None))):
            errors.type_error(f"Parameter `reply_id` must be of type `str` or None, but got value `{reply_id}` of type `{type(reply_id).__name__}`")
        if target_type not in ("User", "Discussion", "Experiment"):
            raise ValueError(f"Parameter `target_type` must be one of ['User', 'Discussion', 'Experiment'], but got value `{target_type}`")
        if special not in (None, "Reminder"):
            raise ValueError(f"Parameter `special` must be one of [None, 'Reminder'], but got value `{special}`")

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
                        reply_id = self.get_user(_nickname, enums.GetUserMode.by_name)["Data"]["User"]["ID"]
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
                "Special": special,
            },
            headers={
                "Content-Type": "application/json",
                "x-API-Token": self.token,
                "x-API-AuthCode": self.auth_code,
            }
        )

        return _check_response(response)

    def remove_comment(self, comment_id: str, target_type: str) -> _api_result:
        ''' 删除评论
            @param comment_id: 评论ID, 可以通过`get_comments`获取
            @param target_type: User, Discussion, Experiment
        '''
        if not isinstance(comment_id, str):
            errors.type_error(f"Parameter `comment_id` must be of type `str`, but got value `{commend_id}` of type `{type(comment_id).__name__}`")
        if not isinstance(target_type, str):
            errors.type_error(f"Parameter `target_type` must be of type `str`, but got value `{target_type}` of type `{type(target_type).__name__}`")
        if target_type not in ("User", "Discussion", "Experiment"):
            raise ValueError(f"Parameter `target_type` must be one of ['User', 'Discussion', 'Experiment'], but got value `{target_type}`")

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
    ) -> _api_result:
        ''' 获取评论板信息
            @param target_id: 物实用户的ID/实验的id
            @param target_type: User, Discussion, Experiment
            @param take: 获取留言的数量
            @param skip: 跳过的留言数量, 为(unix时间戳 * 1000)
            @param comment_id: 从comment_id开始获取take条消息 (另一种skip的规则)
        '''
        if not isinstance(target_id, str):
            errors.type_error(f"Parameter `target_id` must be of type `str`, but got value `{target_id}` of type `{type(target_id).__name__}`")
        if not isinstance(target_type, str):
            errors.type_error(f"Parameter `target_type` must be of type `str`, but got value `{target_type}` of type `{type(target_type).__name__}`")
        if not isinstance(take, int):
            errors.type_error(f"Parameter `take` must be of type `int`, but got value `{take}` of type `{type(take).__name__}`")
        if not isinstance(skip, int):
            errors.type_error(f"Parameter `skip` must be of type `int`, but got value `{skip}` of type `{type(skip).__name__}`")
        if not isinstance(comment_id, (str, type(None))):
            errors.type_error(f"Parameter `comment_id` must be of type `str` or None, but got value `{comment_id}` of type `{type(comment_id).__name__}`")
        if target_type not in ("User", "Discussion", "Experiment"):
            raise ValueError(f"Parameter `target_type` must be one of ['User', 'Discussion', 'Experiment'], but got value `{target_type} of type '{target_type}'")

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

    def get_summary(self, content_id: str, category: Category) -> _api_result:
        ''' 获取实验介绍
            @param content_id: 实验ID
            @param category: 实验区还是黑洞区
        '''
        if not isinstance(content_id, str):
            errors.type_error(f"Parameter `content_id` must be of type `str`, but got value `{content_id}` of type `{type(content_id).__name__}`")
        if not isinstance(category, Category):
            errors.type_error(f"Parameter `category` must be an instance of Category enum, but got value `{category}` of type `{type(category).__name__}`")

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

    def get_derivatives(self, content_id: str, category: Category) -> _api_result:
        ''' 获取作品的详细信息, 物实第一次读取作品会使用此接口
            @param content_id: 实验ID
            @param category: 实验区还是黑洞区
        '''
        if not isinstance(content_id, str):
            errors.type_error(f"Parameter `content_id` must be of type `str`, but got value `{content_id}` of type `{type(content_id).__name__}`")
        if not isinstance(category, Category):
            errors.type_error(f"Parameter `category` must be an instance of Category enum, but got value `{category}` of type `{type(category).__name__}`")

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
            msg: str,
            get_user_mode: enums.GetUserMode,
    ) -> _api_result:
        ''' 获取用户信息
            @param msg: 用户ID/用户名
            @param get_user_mode: 根据ID/用户名获取用户信息
        '''
        if not isinstance(msg, str):
            errors.type_error(f"Parameter `msg` must be of type `str`, but got value `{msg}` of type {type(msg).__name__}`")
        if not isinstance(get_user_mode, enums.GetUserMode):
            errors.type_error(f"Parameter `get_user_mode` must be an instance of type "
                            f"`physicsLab.enums.GetUserMode`, but got value `{get_user_mode}` of type {type(get_user_mode).__name__}`")

        if get_user_mode == enums.GetUserMode.by_id:
            body = {"ID": msg}
        elif get_user_mode == enums.GetUserMode.by_name:
            body = {"Name": msg}
        else:
            errors.unreachable()

        response = requests.post(
            "https://physics-api-cn.turtlesim.com:443/Users/GetUser",
            json=body,
            headers={
                "Content-Type": "application/json",
                "x-API-Token": self.token,
                "x-API-AuthCode": self.auth_code,
            }
        )

        return _check_response(response)

    def get_profile(self) -> _api_result:
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

    def star_content(self, content_id: str, category: Category, star_type: int, status: bool = True) -> _api_result:
        ''' 收藏/支持 某个实验
            @param content_id: 实验ID
            @param category: 实验区, 黑洞区
            @param star_type: 0: 收藏, 1: 使用金币支持实验
            @param status: True: 收藏, False: 取消收藏 (对支持无作用)
        '''
        if not isinstance(content_id, str):
            errors.type_error(f"Parameter `content_id` must be of type `str`, but got value `{content_id}` of type `{type(content_id).__name__}`")
        if not isinstance(category, Category):
            errors.type_error(f"Parameter `category` must be an instance of Category enum, but got value `{category}` of type `{type(category).__name__}`")
        if not isinstance(status, bool):
            errors.type_error(f"Parameter `status` must be of type `bool`, but got value `{status}` of type `{type(status).__name__}`")
        if not isinstance(star_type, int):
            errors.type_error(f"Parameter `star_type` must be of type `int`, but got value `{star_type}` of type `{type(star_type).__name__}`")
        if star_type not in (0, 1):
            raise ValueError(f"Parameter `star_type` must be one of [0, 1], but got value `{star_type} of type '{star_type}'")

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

    def upload_image(self, policy: str, authorization: str, image_path: str) -> _api_result:
        ''' 上传实验图片
            @param authorization: 可通过/Contents/SubmitExperiment获取
            @param image_path: 待上传的图片在本地的路径
        '''
        if policy is None or authorization is None:
            raise RuntimeError("Sorry, Physics-Lab-AR can't upload this iamge")
        if not isinstance(policy, str):
            errors.type_error(f"Parameter `policy` must be of type `str`, but got value `{policy}` of type `{type(policy).__name__}`")
        if not isinstance(authorization, str):
            errors.type_error(f"Parameter `authorization` must be of type `str`, but got value `{authorization}` of type `{type(authorization).__name__}`")
        if not isinstance(image_path, str):
            errors.type_error(f"Parameter `image_path` must be of type `str`, but got value `{image_path}` of type `{type(image_path).__name__}`")
        if not os.path.exists(image_path) or not os.path.isfile(image_path):
            raise FileNotFoundError(f"`{image_path}` not found")

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
                    f"{response.json()['message']}`"
                )
            return response.json()

    def get_message(self, message_id: str) -> _api_result:
        ''' 读取系统邮件消息
            @param message_id: 消息的id
        '''
        if not isinstance(message_id, str):
            errors.type_error(f"Parameter `message_id` must be of type `str`, but got value `{message_id}` of type `{type(message_id).__name__}`")

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
    ) -> _api_result:
        ''' 获取用户收到的消息
            @param category_id: 消息类型:
                0: 全部, 1: 系统邮件, 2: 关注和粉丝, 3: 评论和回复, 4: 作品通知, 5: 管理记录
            @param skip: 跳过skip条消息
            @param take: 取take条消息
            @param no_templates: 是否不返回消息种类的模板消息
        '''
        if category_id not in (0, 1, 2, 3, 4, 5):
            errors.type_error(f"Parameter `category_id` must be an integer within [0, 5], but got value `{category_id}` of type `{category_id}`")
        if not isinstance(skip, int):
            errors.type_error(f"Parameter `skip` must be of type `int`, but got value `{skip}` of type `{type(skip).__name__}`")
        if not isinstance(take, int):
            errors.type_error(f"Parameter `take` must be of type `int`, but got value `{take}` of type `{type(take).__name__}`")
        if not isinstance(no_templates, bool):
            errors.type_error(f"Parameter `no_templates` must be of type `bool`, but got value `{no_templates}` of type `{type(no_templates).__name__}`")

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
    ) -> _api_result:
        ''' 获取支持列表
            @param category: .Experiment 或 .Discussion
            @param skip: 传入一个时间戳, 跳过skip条消息
            @param take: 取take条消息
        '''
        if not isinstance(content_id, str):
            errors.type_error(f"Parameter `content_id` must be of type `str`, but got value `{content_id}` of type `{type(content_id).__name__}`")
        if not isinstance(category, Category):
            errors.type_error(f"Parameter `category` must be an instance of Category enum, but got value `{category}` of type `{type(category).__name__}`")
        if not isinstance(skip, int):
            errors.type_error(f"Parameter `skip` must be of type `int`, but got value `{skip}` of type `{type(skip).__name__}`")
        if not isinstance(take, int):
            errors.type_error(f"Parameter `take` must be of type `int`, but got value `{take}` of type `{type(take).__name__}`")

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
    ) -> _api_result:
        ''' 获取用户的关注/粉丝列表
            @param display_type: 只能为 Follower: 粉丝, Following: 关注
            @param skip: 跳过skip个用户
            @param take: 取take个用户
            @param query: 为用户id或昵称
        '''
        if display_type not in ("Follower", "Following"):
            raise ValueError(f"Parameter `display_type` must be one of ['Follower', 'Following'], but got value `{display_type}` of type `{display_type}`")
        if not isinstance(user_id, str):
            errors.type_error(f"Parameter `user_id` must be of type `str`, but got value `{user_id}` of type `{type(user_id).__name__}`")
        if not isinstance(skip, int):
            errors.type_error(f"Parameter `skip` must be of type `int`, but got value `{skip}` of type `{type(skip).__name__}`")
        if not isinstance(take, int):
            errors.type_error(f"Parameter `take` must be of type `int`, but got value `{take}` of type `{type(take).__name__}`")

        if display_type == "Follower":
            display_type_ = 0
        elif display_type == "Following":
            display_type_ = 1
        else:
            errors.unreachable()

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

    def follow(self, target_id: str, action: bool = True) -> _api_result:
        ''' 关注用户
            @param target_id: 被关注的用户的id
            @param action: true为关注, false为取消关注
        '''
        if not isinstance(target_id, str):
            errors.type_error(f"Parameter `target_id` must be of type `str`, but got value `{target_id}` of type `{type(target_id).__name__}`")
        if not isinstance(action, bool):
            errors.type_error(f"Parameter `action` must be of type `bool`, but got value `{action}` of type `{type(action).__name__}`")

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

    def rename(self, nickname: str) -> _api_result:
        ''' 修改用户昵称
            @param nickname: 新昵称
        '''
        if not isinstance(nickname, str):
            errors.type_error(f"Parameter `nickname` must be of type `str`, but got value `{nickname}` of type {type(nickname).__name__}`")

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

    def modify_information(self, target: str) -> _api_result:
        ''' 修改用户签名
            @param target: 新签名
        '''
        if not isinstance(target, str):
            errors.type_error(f"Parameter `target` must be of type `str`, but got value `{target}` of type `{type(target).__name__}`")

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

    def receive_bonus(self, activity_id: str, index: int) -> _api_result:
        ''' 领取每日签到奖励
            @param activity_id: 活动id
            @param index: 该活动的第几次奖励
        '''
        if not isinstance(activity_id, str):
            errors.type_error(f"Parameter `activity_id` must be of type `str`, but got value `{activity_id}` of type `{type(activity_id).__name__}`")
        if not isinstance(index, int):
            errors.type_error(f"Parameter `index` must be of type `int`, but got value `{index}` of type `{type(index).__name__}`")
        if index < 0:
            raise ValueError(f"Parameter `index` must be a non-negative integer, but got value `{index}`")

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

    def ban(self, target_id: str, reason: str, length: int) -> _api_result:
        ''' 封禁用户
            @param target_id: 要封禁的用户的id
            @param reason: 封禁理由
            @param length: 封禁天数
        '''
        if not isinstance(target_id, str):
            errors.type_error(f"Parameter target_id must be of type `str`, but got value `{target_id}` of type `{type(target_id).__name__}`")
        if not isinstance(reason, str):
            errors.type_error(f"Parameter reason must be of type `str`, but got value `{reason}` of type `{type(reason).__name__}`")
        if not isinstance(length, int):
            errors.type_error(f"Parameter length must be of type `int`, but got value `{length}` of type `{type(length).__name__}`")

        if length <= 0: #TODO 改天试试负数会发生什么
            raise ValueError

        response = requests.post(
            "https://physics-api-cn.turtlesim.com:443/Users/Ban",
            json={
                "TargetID": target_id,
                "Reason": reason,
                "Length": length,
            },
            headers={
                "Content-Type": "application/json",
                "x-API-Token": self.token,
                "x-API-AuthCode": self.auth_code,
            },
        )

        return _check_response(response)

    def unban(self, target_id: str, reason: str) -> _api_result:
        ''' 解除封禁
            @param target_id: 要解除封禁的用户的id
            @param reason: 解封理由
        '''
        if not isinstance(target_id, str):
            errors.type_error(f"Parameter target_id must be of type `str`, but got value `{target_id}` of type `{type(target_id).__name__}`")
        if not isinstance(reason, str):
            errors.type_error(f"Parameter reason must be of type `str`, but got value `{reason}` of type `{type(reason).__name__}`")

        response = requests.post(
            "https://physics-api-cn.turtlesim.com:443/Users/Unban",
            json={
                "TargetID": target_id,
                "Reason": reason,
            },
            headers={
                "Content-Type": "application/json",
                "x-API-Token": self.token,
                "x-API-AuthCode": self.auth_code,
            }
        )

        return _check_response(response)
