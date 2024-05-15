from flask import Blueprint, request, jsonify
import os
import uuid
from werkzeug.utils import secure_filename
import requests

photo_view = Blueprint('photo_view', __name__)


#Route to Upload Selfie
@photo_view.route('/uploadSelfie', methods=['POST'])
def upload_selfie():
    if 'selfie' not in request.files:
        return jsonify({'error': 'No selfie uploaded'}), 400

    selfie_file = request.files['selfie']
    if selfie_file.filename == '':
        return jsonify({'error': 'No selected selfie'}), 400

    # Generate a unique filename for the selfie
    filename = secure_filename(selfie_file.filename)
    unique_filename = f"selfie_{uuid.uuid4().hex}_{filename}"

    # Save the selfie to the server
    upload_folder = 'static/uploads/selfies/'
    os.makedirs(upload_folder, exist_ok=True)
    filepath = os.path.join(upload_folder, unique_filename)
    selfie_file.save(filepath)

    return jsonify({'success': 'Selfie uploaded successfully', 'filename': unique_filename}), 200


#Route to upload Event photos
@photo_view.route('/uploadEvent', methods=['POST'])
def upload_event_photos():
    if 'photos' not in request.files:
        return jsonify({'error': 'No photos uploaded'}), 400

    photos = request.files.getlist('photos')
    if not photos:
        return jsonify({'error': 'No selected photos'}), 400

    event_id = request.form.get('event_id')
    if not event_id:
        return jsonify({'error': 'Event ID is required'}), 400

    event_folder = os.path.join('static/uploads/events/', str(event_id))
    os.makedirs(event_folder, exist_ok=True)

    uploaded_filenames = []

    for photo_file in photos:
        if photo_file.filename == '':
            continue

        # Generate a unique filename for each photo
        filename = secure_filename(photo_file.filename)
        unique_filename = f"{uuid.uuid4().hex}_{filename}"

        # Save the photo to the event folder
        filepath = os.path.join(event_folder, unique_filename)
        photo_file.save(filepath)

        uploaded_filenames.append(unique_filename)

    return jsonify({'success': 'Photos uploaded successfully', 'filenames': uploaded_filenames}), 200

#Route to send selfie for computation
@photo_view.route('/sendSelfie', methods=['POST'])
def send_selfie_to_url():
    url_to_send_selfies = request.form.get('url')

    if not url_to_send_selfies:
        return jsonify({'error': 'URL is required'}), 400

    # Assuming 'selfie' is the key for the uploaded selfie filename
    selfie_filename = request.form.get('selfie')
    selfie_path = os.path.join('static/uploads/selfies', selfie_filename)

    if not os.path.isfile(selfie_path):
        return jsonify({'error': f"Selfie file '{selfie_filename}' not found."}), 404

    try:
        with open(selfie_path, 'rb') as selfie_file:
            files = {'selfie': selfie_file}
            response = requests.post(url_to_send_selfies, files=files)
            if response.status_code == 200:
                return jsonify({'success': 'Selfie uploaded successfully'}), 200
            else:
                return jsonify({'error': f"Failed to upload selfie '{selfie_filename}'. Status code: {response.status_code}"}), 500
    except Exception as e:
        return jsonify({'error': f"Error uploading selfie: {str(e)}"}), 500
