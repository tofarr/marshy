from typing import Union, Dict, List

ExternalType = Union[None, str, bool, int, float, List['ExternalType'], 'ExternalItemType']
ExternalItemType = Dict[str, ExternalType]
