from typing import Union, Dict, List

ExternalType = Union[None, str, bool, int, float, List['marshy.types.ExternalType'], 'marshy.types.ExternalItemType']
ExternalItemType = Dict[str, ExternalType]
