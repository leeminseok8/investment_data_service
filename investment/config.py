import os

from dotenv import load_dotenv

load_dotenv()  # .env 파일을 읽어서 환경변수에 넣어줌

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.environ["INVESTMENT_DATABASE_NAME"],
        "USER": os.environ["INVESTMENT_DATABASE_USER"],
        "PASSWORD": os.environ["INVESTMENT_DATABASE_PASSWORD"],
        "HOST": os.environ["INVESTMENT_DATABASE_HOST"],
        "PORT": int(os.environ.get("INVESTMENT_DATABASE_PORT", "3306")),
        "OPTIONS": {"charset": "utf8mb4"},
    }
}

SECRET_KEY = os.environ["INVESTMENT_SECRET_KEY"]
