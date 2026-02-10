import os

OP_ENV = os.getenv("OP_ENV", "sandbox")

OPERATOR_EMAIL = os.getenv("OPERATOR_EMAIL", "test+test@getpackage.com")
OPERATOR_PASSWORD = os.getenv("OPERATOR_PASSWORD", "AA1122aa")

if OP_ENV == "sandbox":
    OP_BASE_URL = os.getenv("OP_BASE_URL", "https://frontend-sandbox.getpackage.com")
    OP_API_URL = os.getenv("OP_API_URL", "https://sandbox-apiv2.getpackage.com")
    OP_API_KEY = os.getenv("OP_API_KEY", "APIKEY 2d9ebcc2-89b5-4c36-ae4f-5835f80ef127")
    DEFAULT_COURIER_ID = "433877"
else:
    OP_BASE_URL = os.getenv("OP_BASE_URL", "https://operator-stg.getpackage.dev")
    OP_API_URL = os.getenv("OP_API_URL", "https://api-stg.getpackage.dev")
    OP_API_KEY = os.getenv("OP_API_KEY", "APIKEY 8502cc15-cfee-4763-a7da-f75460f71359")
    DEFAULT_COURIER_ID = "353325"

COURIER_ID = os.getenv("OPERATOR_COURIER_ID", DEFAULT_COURIER_ID)

HEADLESS = os.getenv("HEADLESS", "true").lower() not in {"0", "false", "no"}
SLOW_MO = int(os.getenv("SLOW_MO", "0"))

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOADS_DIR = os.path.join(ROOT_DIR, "downloads")
RESOURCES_DIR = os.path.join(os.path.dirname(ROOT_DIR), "src", "test", "resources")
