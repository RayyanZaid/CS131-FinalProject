from flask import Flask, request, jsonify, send_file
import os

from flask_cors import CORS

app = Flask(__name__)

# Or enable CORS for all domains on all routes
CORS(app, resources={r"/*": {"origins": "*"}})

IMAGE_SAVE_PATH = "images"  # Ensure this directory exists
data_store = {
    "sheetMusicName": None,
    "imagePath": None
}

@app.route('/submit', methods=['POST'])
def submit():
    data = request.form
    image = request.files['image']
    sheetMusicName = data['title']
    imagePath = os.path.join(IMAGE_SAVE_PATH, image.filename)
    image.save(imagePath)
    data_store["sheetMusicName"] = sheetMusicName
    data_store["imagePath"] = imagePath
    print(f"Received title: {sheetMusicName}, saved image to: {imagePath}")
    return jsonify({"message": "Data received"}), 200

@app.route('/check', methods=['GET'])
def check():
    if data_store["sheetMusicName"] and data_store["imagePath"]:
        

        title = data_store["sheetMusicName"]
        imagePath = data_store["imagePath"]
        data_store["sheetMusicName"] = None
        data_store["imagePath"] = None


        return jsonify({
            "title": title,
            "imagePath": imagePath
        }), 200
    else:
        return jsonify({"message": "Waiting for data"}), 204

@app.route('/get_image', methods=['GET'])
def get_image():
    image_path = request.args.get('imagePath')
    if os.path.exists(image_path):
        return send_file(image_path)
    else:
        return jsonify({"message": "Image not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
