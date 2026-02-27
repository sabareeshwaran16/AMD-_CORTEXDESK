"""
Network guard - ensures no external network calls.
"""
from app.core.config import settings


def check_network_allowed(url: str) -> bool:
    """
    Check if a network request is allowed.
    Only localhost is allowed unless external_network_enabled is True.
    
    Args:
        url: URL to check
    
    Returns:
        True if allowed, False otherwise
    """
    if settings.external_network_enabled:
        return True
    
    # Only allow localhost
    allowed_hosts = ['localhost', '127.0.0.1', '0.0.0.0']
    for host in allowed_hosts:
        if host in url:
            return True
    
    return False


def block_external_requests():
    """Block all external HTTP requests."""
    # TODO: Implement request blocking middleware
    # This would intercept requests and block non-localhost URLs
    pass

