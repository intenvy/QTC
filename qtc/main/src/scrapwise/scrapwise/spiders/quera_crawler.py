from abc import ABC, abstractmethod
from scrapy import Spider, FormRequest


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

    def parse(self, response, **kwargs):
        return FormRequest.from_response(
            response,
            formdata={
                'username': self.username,
                'password': self.password
            },
            callback=self.after_login
        )

    @abstractmethod
    def after_login(self, response):
        if quera_authentication_failed(response):
            self.logger.error(f'Login FAILED - username: "{self.username}", password: "{self.password}"')
            return
