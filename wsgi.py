from app import app

if __name__ == "__main__":
    app.run(port=os.getenv('PORT', 5000), ssl_context="adhoc")
