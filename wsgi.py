from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(port=7000,load_dotenv=True)
