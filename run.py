from app import create_app
from app import db

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)  # set debug=True untuk membantu debugging
