"""Google Drive API client for file operations."""
import pickle
import os
from pathlib import Path
from typing import List, Dict, Optional
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io
from tqdm import tqdm
from config import Config


class GDriveClient:
    """Client for interacting with Google Drive API."""
    
    def __init__(self):
        self.service = None
        self.creds = None
        self._authenticate()
    
    def _authenticate(self):
        """Authenticate with Google Drive API."""
        # Load existing credentials
        if Config.TOKEN_FILE.exists():
            with open(Config.TOKEN_FILE, 'rb') as token:
                self.creds = pickle.load(token)
        
        # Refresh or create new credentials
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                if not Config.CREDENTIALS_FILE.exists():
                    raise FileNotFoundError(
                        f"credentials.json not found at {Config.CREDENTIALS_FILE}\n"
                        "Download it from Google Cloud Console: "
                        "https://console.cloud.google.com/apis/credentials"
                    )
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(Config.CREDENTIALS_FILE), Config.SCOPES
                )
                self.creds = flow.run_local_server(port=0)
            
            # Save credentials
            with open(Config.TOKEN_FILE, 'wb') as token:
                pickle.dump(self.creds, token)
        
        self.service = build('drive', 'v3', credentials=self.creds)
    
    def list_files(self, query: Optional[str] = None, page_size: int = 100) -> List[Dict]:
        """List files from Google Drive."""
        files = []
        page_token = None
        
        # Build query
        if query is None:
            # Default: all files except trashed
            query = "trashed=false"
        
        print("Fetching files from Google Drive...")
        
        while True:
            try:
                results = self.service.files().list(
                    q=query,
                    pageSize=page_size,
                    pageToken=page_token,
                    fields="nextPageToken, files(id, name, mimeType, modifiedTime, size, webViewLink, parents)"
                ).execute()
                
                items = results.get('files', [])
                files.extend(items)
                
                page_token = results.get('nextPageToken')
                if not page_token:
                    break
                    
            except Exception as e:
                print(f"Error fetching files: {e}")
                break
        
        print(f"Found {len(files)} files")
        return files
    
    def download_file(self, file_id: str, file_name: str, mime_type: str, 
                     destination: Path) -> Optional[Path]:
        """Download a file from Google Drive."""
        try:
            # Handle Google Workspace files (Docs, Sheets, Slides)
            if mime_type in Config.EXPORT_MIME_TYPES:
                export_mime = Config.EXPORT_MIME_TYPES[mime_type]
                request = self.service.files().export_media(
                    fileId=file_id,
                    mimeType=export_mime
                )
                # Update file extension
                file_name = Path(file_name).stem + Config.SUPPORTED_MIME_TYPES[mime_type]
            else:
                request = self.service.files().get_media(fileId=file_id)
            
            # Download file
            file_path = destination / file_name
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            
            done = False
            while not done:
                status, done = downloader.next_chunk()
            
            # Write to file
            with open(file_path, 'wb') as f:
                f.write(fh.getvalue())
            
            return file_path
            
        except Exception as e:
            print(f"Error downloading {file_name}: {e}")
            return None
    
    def sync_files(self, destination: Path = None) -> List[Path]:
        """Sync all supported files from Google Drive."""
        if destination is None:
            destination = Config.STORAGE_PATH
        
        destination.mkdir(parents=True, exist_ok=True)
        
        # Build query for supported file types
        mime_conditions = [f"mimeType='{mime}'" for mime in Config.SUPPORTED_MIME_TYPES.keys()]
        query = f"trashed=false and ({' or '.join(mime_conditions)})"
        
        files = self.list_files(query=query)
        
        # Filter by size
        files = [f for f in files if not f.get('size') or int(f.get('size', 0)) <= Config.MAX_FILE_SIZE_BYTES]
        
        print(f"\nDownloading {len(files)} files...")
        downloaded_paths = []
        
        for file in tqdm(files, desc="Downloading"):
            file_path = self.download_file(
                file['id'],
                file['name'],
                file['mimeType'],
                destination
            )
            if file_path:
                downloaded_paths.append(file_path)
        
        print(f"\nSuccessfully downloaded {len(downloaded_paths)} files")
        return downloaded_paths
    
    def get_file_metadata(self, file_id: str) -> Optional[Dict]:
        """Get metadata for a specific file."""
        try:
            file = self.service.files().get(
                fileId=file_id,
                fields="id, name, mimeType, modifiedTime, size, webViewLink, parents"
            ).execute()
            return file
        except Exception as e:
            print(f"Error getting file metadata: {e}")
            return None
