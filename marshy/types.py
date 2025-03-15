from typing import Union, Dict, List

ExternalType = Union[
    None,
    str,
    bool,
    int,
    float,
    list["marshy.types.ExternalType"],
    "marshy.types.ExternalItemType",
]
ExternalItemType = dict[str, ExternalType]
