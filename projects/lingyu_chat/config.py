"""Customer support configuration loaded from the repository .env."""
import os
from ai_learning.config import get_chat_model_name, load_environment

load_environment()
DASHSCOPE_API_KEY = os.environ.get("DASHSCOPE_API_KEY")
INTENT_RECOGNIZE_MODEL = os.environ.get("INTENT_MODEL", "qwen-flash")
TONGYI_MODEL = get_chat_model_name()
TONGYI_TEMPERATURE = 0.3
TONGYI_MAX_OUTPUT_LENGTH = 1024
