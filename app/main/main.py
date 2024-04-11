from dotenv import load_dotenv

load_dotenv()

from app.presentation.fastapi.configs import create_app

app = create_app()
