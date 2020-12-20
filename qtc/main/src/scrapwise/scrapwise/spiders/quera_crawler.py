from abc import ABC, abstractmethod
from typing import Generator

from scrapy import Spider, FormRequest, Request


def quera_authentication_failed(response) -> bool:
    # TODO: Check the contents of the response and return True if it failed
    # or False if it succeeded.
    return False


class QueraCrawler(Spider, ABC):
    name = 'quera'
    start_urls = ['https://quera.ir/accounts/login/']

    def __init__(self, username: str = '', password: str = '', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.username = username
        self.password = password

    def parse(self, response, **kwargs) -> FormRequest:
        token = response.xpath(
            "//html/body/div[3]/div/div/div[1]/form/input[@name='csrfmiddlewaretoken']/@value"
        ).extract_first()
        return FormRequest.from_response(
            response,
            formdata={
                'username': self.username,
                'password': self.password,
                'csrfmiddlewaretoken': token
            },
            callback=self.after_login
        )

    @abstractmethod
    def after_login(self, response):
        if quera_authentication_failed(response):
            self.logger.error(f'Login FAILED - username: "{self.username}", password: "{self.password}"')
