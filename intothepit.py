from app import app

DEBUG = True
PORT = 8000

if __name__ == '__main__':
    app.run(debug=DEBUG, port=PORT)