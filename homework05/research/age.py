import datetime as dt
import statistics
import typing as tp

from vkapi.friends import get_friends


def age_predict(user_id: int) -> tp.Optional[float]:
    """
    Наивный прогноз возраста пользователя по возрасту его друзей.

    Возраст считается как медиана среди возраста всех друзей пользователя

    :param user_id: Идентификатор пользователя.
    :return: Медианный возраст пользователя.
    """
    curr_year = dt.datetime.now().year
    friends = get_friends(user_id).items
    ages = []
    for friend in friends:
        try:
            ages.append(curr_year - int(friend["bdate"][-4:]))
        except:
            pass
    if ages:
        return statistics.median(ages)
    else:
        return None
