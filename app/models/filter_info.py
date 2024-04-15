from dataclasses import dataclass, field

@dataclass
class Filter:
    '''데이터 클래스로서의 필터 정보'''
    name: str
    face_filter_on: bool = field(default=True)
    face_filter: list = field(default_factory=list)
    object_filter: list = field(default_factory=list)
    