from app import app
import os

if __name__ == "__main__":
    app.run(port=os.getenv('PORT', 5000), ssl_context="adhoc")
