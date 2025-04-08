from app.routes import app
from app.database import engine
from app.models import Base

Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
