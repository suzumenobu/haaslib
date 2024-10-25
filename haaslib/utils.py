from typing import Any, Dict, Optional
from datetime import datetime, timezone

def unix_timestamp() -> int:
    """Get current Unix timestamp"""
    return int(datetime.now(timezone.utc).timestamp())

def format_query_params(params: Dict[str, Any]) -> Dict[str, str]:
    """Format query parameters for API requests"""
    formatted = {}
    for key, value in params.items():
        if value is None:
            continue
        if isinstance(value, bool):
            formatted[key] = str(value).lower()
        elif isinstance(value, (int, float)):
            formatted[key] = str(value)
        else:
            formatted[key] = str(value)
    return formatted

def validate_market_tag(market_tag: str) -> bool:
    """Validate market tag format"""
    parts = market_tag.split('_')
    return len(parts) >= 4 and all(parts)

def parse_market_tag(market_tag: str) -> Optional[Dict[str, str]]:
    """Parse market tag into components"""
    if not validate_market_tag(market_tag):
        return None
        
    parts = market_tag.split('_')
    return {
        'price_source': parts[0],
        'base': parts[1],
        'quote': parts[2],
        'market_type': parts[3] if len(parts) > 3 else 'SPOT'
    }
