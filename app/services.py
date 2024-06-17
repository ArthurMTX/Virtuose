import requests
from Virtuose.settings import API_URL


def get_all_domains():
    response = requests.get(f"{API_URL}/domains/")
    print(response)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def get_domain_uuid(uuid):
    response = requests.get(f"{API_URL}/domains/UUID/{uuid}")
    if response.status_code == 200:
        return response.json()
    else:
        return None


def get_domain_name(name):
    response = requests.get(f"{API_URL}/domains/{name}")
    if response.status_code == 200:
        return response.json()
    else:
        return None

