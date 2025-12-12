

import requests
from django.conf import settings

DROPi_BASE_URL = "https://api.dropi.co"

def dropi_login():
    url = f"{DROPi_BASE_URL}/auth/login"

    data = {
        "email": settings.DROPI_EMAIL,
        "password": settings.DROPI_PASSWORD,
        "white_brand_id": settings.DROPI_WHITE_BRAND_ID
    }

    headers = {
        "dropi-integration-key": settings.DROPI_INTEGRATION_KEY
    }

    response = requests.post(url, json=data)
    response.raise_for_status()

    return response.json()["token"]



def dropi_get_products(token):
    url = f"{DROPi_BASE_URL}/products"

    headers = {
        "Authorization": f"Bearer {token}",
        "dropi-integration-key": settings.DROPI_INTEGRATION_KEY
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    return response.json()["data"]
