from django.db import models
from django.core.validators import FileExtensionValidator
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import googleapiclient.http



PLATFORMS = {
    "Youtube": "Youtube",
}

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]


class VideoPost(models.Model):

    class Platforms(models.TextChoices):
        Youtube = 'Yt', ('Youtube')


    title = models.CharField(blank=False, max_length=200)
    description = models.TextField(blank=True)
    file = models.FileField(validators= [FileExtensionValidator( ['mp4'] )])
    platforms = models.TextField(default=Platforms.Youtube, choices=Platforms)
    
    def save(self, *args, **kwargs):
        # New video
        if not self.pk:

            super().save(*args, **kwargs)

            flow = InstalledAppFlow.from_client_secrets_file(
                "C:/Users/user/Downloads/client_secret.json",
                scopes=SCOPES, 
                redirect_uri="http://127.0.0.1:8000/oauth2callback"
            )


            creds = flow.run_local_server(
                port=8080, 
                access_type='offline', 
                prompt='consent')

            youtube = build('youtube', 'v3', credentials=creds)

            request_body = {
                "snippet": {
                    "title": self.title,
                    "description": self.description,
                },
                "status": {
                    "privacyStatus": "private"
                }
            }

            video_path = self.file.path
            video = googleapiclient.http.MediaFileUpload(video_path, chunksize=-1, resumable=True)

            request = youtube.videos().insert(
                part="snippet, status",
                body=request_body,
                media_body= video
            )

            response = None

            while response is None:
                status, response = request.next_chunk()



        