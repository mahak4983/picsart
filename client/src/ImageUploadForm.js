import React, { useState } from 'react';

const ImageUploadForm = () => {
    const [selfie, setSelfie] = useState(null);
    const [eventPhotos, setEventPhotos] = useState([]);
    const [eventID, setEventID] = useState('');
    const [uploadStatus, setUploadStatus] = useState('');

    const handleSelfieChange = (e) => {
        const selectedSelfie = e.target.files[0];
        setSelfie(selectedSelfie);
    };

    const handleEventPhotosChange = (e) => {
        const selectedPhotos = Array.from(e.target.files);
        setEventPhotos(selectedPhotos);
    };

    const handleUploadSelfie = async () => {
        if (!selfie) {
            alert('Please select a selfie to upload.');
            return;
        }

        const formData = new FormData();
        formData.append('selfie', selfie);

        try {
            const response = await fetch('http://localhost:5000/photos/uploadSelfie', {
                method: 'POST',
                body: formData,
            });

            if (response.ok) {
                const data = await response.json();
                setUploadStatus(`Selfie uploaded successfully: ${data.filename}`);
            } else {
                setUploadStatus('Error uploading selfie.');
            }
        } catch (error) {
            console.error('Error uploading selfie:', error);
            setUploadStatus('Error uploading selfie.');
        }
    };

    const handleUploadEventPhotos = async () => {
        if (!eventPhotos.length || !eventID) {
            alert('Please select event photos and enter an event ID.');
            return;
        }

        const formData = new FormData();
        formData.append('event_id', eventID);
        eventPhotos.forEach((photo) => {
            formData.append('photos', photo);
        });

        try {
            const response = await fetch('http://localhost:5000/photos/uploadEvent', {
                method: 'POST',
                body: formData,
            });

            if (response.ok) {
                const data = await response.json();
                setUploadStatus(`Uploaded ${data.filenames.length} photos for event ${eventID}`);
            } else {
                setUploadStatus('Error uploading event photos.');
            }
        } catch (error) {
            console.error('Error uploading event photos:', error);
            setUploadStatus('Error uploading event photos.');
        }
    };

    return (
        <div>
            <h1>Image Upload Form</h1>
            <h2>Upload Selfie</h2>
            <input type="file" accept=".jpg,.png" onChange={handleSelfieChange} />
            <button onClick={handleUploadSelfie}>Upload Selfie</button>
            <h2>Upload Event Photos</h2>
            <input type="text" placeholder="Enter Event ID" value={eventID} onChange={(e) => setEventID(e.target.value)} />
            <input type="file" accept=".jpg,.png" multiple onChange={handleEventPhotosChange} />
            <button onClick={handleUploadEventPhotos}>Upload Event Photos</button>
            {uploadStatus && <p>{uploadStatus}</p>}
        </div>
    );
};

export default ImageUploadForm;
