import json
import os
from typing import Dict, Any, Optional

DATA_DIR = os.getenv("DATA_DIR", ".")
HOST_COMPANY_FILE = os.path.join(DATA_DIR, "host_company.json")


def save_host_company(company_data: Dict[str, Any]) -> Dict[str, Any]:
    os.makedirs(DATA_DIR, exist_ok=True)

    with open(HOST_COMPANY_FILE, "w", encoding="utf-8") as f:
        json.dump(company_data, f, indent=4)

    return company_data


def get_host_company() -> Optional[Dict[str, Any]]:
    if not os.path.exists(HOST_COMPANY_FILE):
        return None

    with open(HOST_COMPANY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)
