from flask import Flask
from flask_cors import CORS
from views.photo_view import photo_view

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Register the photo_view blueprint
app.register_blueprint(photo_view, url_prefix='/photos')

if __name__ == '__main__':
    app.run(debug=True)
