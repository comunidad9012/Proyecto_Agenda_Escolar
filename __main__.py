from waitress import serve

from rutas import app

if __name__ == "__main__":
    serve(app, listen="localhost:5000")
