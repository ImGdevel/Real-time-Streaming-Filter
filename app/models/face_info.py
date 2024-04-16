from dataclasses import dataclass, field
from typing import Dict

class Face:
    face_name : str
    encoding_list: Dict[str, str] = field(default_factory=dict)
