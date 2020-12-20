from scrapy import Spider, FormRequest

from .quera_crawler import QueraCrawler


class AssignmentFetcher(QueraCrawler):

    def __init__(self, assignment_id: int, problem_id: int, username: str, password: str, *args, **kwargs):
        super().__init__(username, password, args, kwargs)
        self.assignment_id = assignment_id
        self.problem_id = problem_id

    def after_login(self, response):
        pass
