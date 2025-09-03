import msgspec
from typing import Literal
from pathlib import Path

class DatasetItem(msgspec.Struct):
    behavior_id: str
    behavior: str
    category: Literal["drug", "chemical", "biological", "radiological", "nuclear", "explosive"]
    optimizer_target: str


def load_dataset() -> list[DatasetItem]:    
    path = Path(__file__).parent.parent/ "datasets" / "transluce_cbrn.jsonl"

    lines = []
    with open(path, "r") as f:
        for line in f:
            lines.append(msgspec.json.decode(line, type=DatasetItem))

    return lines
