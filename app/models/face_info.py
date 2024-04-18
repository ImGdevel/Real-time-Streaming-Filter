from dataclasses import dataclass, field
from typing import Dict

@dataclass
class Face:
    face_name : str
    encoding_list: Dict[str, str] = field(default_factory=dict) # ["face_id","encoding_value(사진)"]
