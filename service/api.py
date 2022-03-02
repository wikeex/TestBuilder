from typing import List


class ReqParam:
    def __init__(self):
        self.label: str = ''
        self.name: str = ''
        self.description: str = ''
        self.required: bool = False
        self.type: str = ''
        self.position: str = ''
        self.children: List[ReqParam] = []


class ResParam:
    def __init__(self):
        self.label: str = ''
        self.name: str = ''
        self.description: str = ''


class Api:
    def __init__(self):
        self.name: str = ''
        self.description: str = ''
        self.path: str = ''
        self.method: str = ''
        self.params: List[ReqParam] = []


class Group:
    def __init__(self):
        self.name: str = ''
        self.description: str = ''

        self.apis: List[Api] = []
