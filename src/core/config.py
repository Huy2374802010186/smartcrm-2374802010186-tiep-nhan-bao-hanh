import os

class Settings:
    PROJECT_NAME: str = "Smart CRM - Mekong Mobile (L02 Warranty Intake)"
    VERSION: str = "1.0.0"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/smartcrm")

settings = Settings()
