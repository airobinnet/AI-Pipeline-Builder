# backend\app\__init__.py

from quart import Quart
from quart_cors import cors

app = Quart(__name__)
app = cors(app, allow_origin="http://localhost:3000")

from app import routes