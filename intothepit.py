from app import app
from app import models
import os

if 'ON_HEROKU' in os.environ:
    models.initialize()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    models.initialize()
    app.run(debug=True, port=port)