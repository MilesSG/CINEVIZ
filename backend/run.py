from app import create_app
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True) 