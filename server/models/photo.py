from datetime import datetime


class Photo:
    def __init__(self, filename, upload_date=None):
        self.filename = filename
        self.upload_date = upload_date or datetime.now()
