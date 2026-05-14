from app import create_app, db
from app.config import DeploymentConfig
from flask_migrate import Migrate

app = create_app(DeploymentConfig)

if __name__ == '__main__':
    app.run(debug=True)