import time
import typing as tp

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


class Session:
    """
    Сессия.

    :param base_url: Базовый адрес, на который будут выполняться запросы.
    :param timeout: Максимальное время ожидания ответа от сервера.
    :param max_retries: Максимальное число повторных запросов.
    :param backoff_factor: Коэффициент экспоненциального нарастания задержки.
    """

    def __init__(
        self,
        base_url: str,
        timeout: float = 5.0,
        max_retries: int = 3,
        backoff_factor: float = 0.3,
    ) -> None:
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor

    def get(self, url: str, *args: tp.Any, **kwargs: tp.Any) -> requests.Response:
        count = 0
        while True:
            try:
                response = requests.get(self.base_url + "/" + url, timeout=self.timeout)
                response.raise_for_status()
                return response
            except requests.exceptions.HTTPError:
                if self.max_retries == 1:
                    raise requests.exceptions.HTTPError
                if count == self.max_retries:
                    raise requests.exceptions.RetryError
                sleep = (self.backoff_factor * (2**count)).__round__()
                time.sleep(sleep)
                count += 1

            except requests.exceptions.ConnectionError:
                raise requests.exceptions.ConnectionError

            except requests.exceptions.ReadTimeout:
                raise requests.exceptions.ReadTimeout

    def post(self, url: str, *args: tp.Any, **kwargs: tp.Any) -> requests.Response:
        count = 0
        while True:
            try:
                response = requests.post(
                    self.base_url + url, data=kwargs, timeout=self.timeout
                )
                response.raise_for_status()
                return response
            except requests.exceptions.HTTPError:
                if self.max_retries == 1:
                    raise requests.exceptions.HTTPError
                if count == self.max_retries:
                    raise requests.exceptions.RetryError
                sleep = (self.backoff_factor * (2**count)).__round__()
                time.sleep(sleep)
                count += 1

            except requests.exceptions.ConnectionError:
                raise requests.exceptions.ConnectionError

            except requests.exceptions.ReadTimeout:
                raise requests.exceptions.ReadTimeout
