from dataclasses import dataclass, field
from typing import Dict

@dataclass
class Filter:
    '''데이터 클래스로서의 필터 정보'''
    name: str
    face_filter_on: bool = True
    face_filter: Dict[int, int] = field(default_factory=dict)  # 딕셔너리로 변경
    object_filter: list = field(default_factory=list)
    
    mosaic_blur_strength: float = 50
    mosaic_blur_shape: str = "rect"

    def __post_init__(self):
        if not isinstance(self.face_filter, dict):
            self.face_filter = {filter_name: -1 for filter_name in self.face_filter}
