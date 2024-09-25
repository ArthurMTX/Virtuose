import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app.models.domain import Domains

def domain_list(QEMU_URI: str) -> dict:
    """
    Returns a list of all domains.

    Returns:
        dict: A dictionary containing all domains.
    """
    domains = Domains(QEMU_URI)
    return domains.list_all()