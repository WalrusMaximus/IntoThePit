from app import app
from app import models
import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(debug=True, port=port)