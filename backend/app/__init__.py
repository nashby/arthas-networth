from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from flask_httpauth import HTTPBasicAuth

from redis import Redis
import rq

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

auth = HTTPBasicAuth()

redis = Redis.from_url(app.config['REDIS_URL'])
task_queue = rq.Queue('arthas_networth_import', connection=redis)

from app import routes
