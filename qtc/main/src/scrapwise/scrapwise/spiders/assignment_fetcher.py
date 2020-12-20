from scrapy import Spider, FormRequest, Request
from .quera_crawler import QueraCrawler


class AssignmentFetcher(QueraCrawler):

    def __init__(self, assignment_id: int, username: str, password: str, *args, **kwargs):
        super().__init__(username, password, args, kwargs)
        self.assignment_id = assignment_id

    def after_login(self, response) -> Request:
        super().after_login(response)
        return Request(
            url=f'https://quera.ir/course/assignments/{self.assignment_id}/problems',
            callback=self.collect_assignment_problems
        )

    def collect_assignment_problems(self, request):
        print('Im collecting :(')
