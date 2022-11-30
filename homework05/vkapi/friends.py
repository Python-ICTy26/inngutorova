import dataclasses
import math
import time
import typing as tp

import requests

from vkapi import config, session, Session
from vkapi.config import VK_CONFIG
from vkapi.exceptions import APIError

QueryParams = tp.Optional[tp.Dict[str, tp.Union[str, int]]]


@dataclasses.dataclass(frozen=True)
class FriendsResponse:
    count: int
    items: tp.List[tp.Dict[str, tp.Any]]


def get_friends(
    user_id: int, count: int = 5000, offset: int = 0, fields: tp.Optional[tp.List[str]] = None
) -> FriendsResponse:
    """
    Получить список идентификаторов друзей пользователя или расширенную информацию
    о друзьях пользователя (при использовании параметра fields).
    :param user_id: Идентификатор пользователя, список друзей для которого нужно получить.
    :param count: Количество друзей, которое нужно вернуть.
    :param offset: Смещение, необходимое для выборки определенного подмножества друзей.
    :param fields: Список полей, которые нужно получить для каждого пользователя.
    :return: Список идентификаторов друзей пользователя или список пользователей.
    """
    ses = Session(f"{VK_CONFIG['domain']}")
    friends = ses.get(
        "friends.get",
        user_id=user_id,
        count=count,
        offset=offset,
        fields=fields,
        v=config.VK_CONFIG["version"],
        access_token=config.VK_CONFIG["access_token"],
    ).json()["response"]

    return FriendsResponse(friends["count"], friends["items"])


class MutualFriends(tp.TypedDict):
    id: int
    common_friends: tp.List[int]
    common_count: int


def get_mutual(
    source_uid: tp.Optional[int] = None,
    target_uid: tp.Optional[int] = None,
    target_uids: tp.Optional[tp.List[int]] = None,
    order: str = "",
    count: tp.Optional[int] = None,
    offset: int = 0,
    progress=None,
) -> tp.List[MutualFriends]:
    """
    Получить список идентификаторов общих друзей между парой пользователей.
    :param source_uid: Идентификатор пользователя, чьи друзья пересекаются с друзьями пользователя с идентификатором target_uid.
    :param target_uid: Идентификатор пользователя, с которым необходимо искать общих друзей.
    :param target_uids: Cписок идентификаторов пользователей, с которыми необходимо искать общих друзей.
    :param order: Порядок, в котором нужно вернуть список общих друзей.
    :param count: Количество общих друзей, которое нужно вернуть.
    :param offset: Смещение, необходимое для выборки определенного подмножества общих друзей.
    :param progress: Callback для отображения прогресса.
    """
    domain = VK_CONFIG["domain"]
    access_token = VK_CONFIG["access_token"]
    version = VK_CONFIG["version"]
    url = f"{domain}/friends.getMutual"
    mutual = []
    if target_uids is None:
        count = 1
    else:
        count = math.ceil(len(target_uids) / 100)
    for i in range(0, count):
        response = requests.get(
            url,
            {
                "access_token": access_token,
                "source_uid": source_uid,
                "target_uid": target_uid,
                "target_uids": target_uids,
                "order": order,
                "count": count,
                "offset": i * 100,
                "v": version,
            },
        ).json()["response"]
        mutual += response
        if i % 3 == 0:
            time.sleep(1)
    return mutual