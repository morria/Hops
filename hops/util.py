"""
Utility functions
"""
from typing import TypeVar, Dict, Any, List

T = TypeVar('T')
def get_or_else(d: Dict[str, Any], path: List[str], default: T = None) -> T:
    """
    Get or else
    """
    current = d
    for key in path:
        if not isinstance(current, dict) or key not in current:
            return default
        current = current[key]
    return current
