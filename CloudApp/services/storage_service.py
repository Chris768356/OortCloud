from pathlib import Path
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from CloudApp.dto.file_dto import StoredFileDTO
import uuid
import shutil

class StorageService:

    def __init__(self,base_path):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)        

    def get_user_folder(self, directory_uuid : str) -> Path:
        user_path = self.base_path / directory_uuid
        user_path.mkdir(parents=True, exist_ok=True)
        return user_path

    def save_file(self,file: FileStorage, directory_uuid: str) -> StoredFileDTO:
        file_name = secure_filename(file.filename) or "unnamed_data"
        file_uuid = uuid.uuid4().hex
        file_ext = file_name.rsplit('.', 1)[1].lower()
        storage_filename = uuid.uuid4().hex + "." + file_ext
        user_path = self.get_user_folder(directory_uuid)
        file_path = user_path / storage_filename
        file.save(file_path)
        file_size = file_path.stat().st_size
        file_dto = StoredFileDTO(file_uuid, file_name,storage_filename, file_size)
        return file_dto

    def delete_file(self, storage_filename: str , directory_uuid: str) -> bool:
        delete_path = self.get_file_path(storage_filename, directory_uuid)
        if delete_path is not None:
            delete_path.unlink()
            return True
        else: 
            return False

    def get_file_path(self, storage_filename: str , directory_uuid: str) -> Path | None:
        user_folder = self.get_user_folder(directory_uuid)
        file_path = user_folder / storage_filename
        if file_path.is_file():
            return file_path
        else:
            return None

    def delete_user_folder(self, directory_uuid: str) -> bool | None:
        user_folder = self.base_path / directory_uuid
        if user_folder.exists():
            try:
                shutil.rmtree(user_folder)
                return True
            except OSError:
                raise OSError("Ein serverseitiger Fehler ist aufgetreten. Deine Dateien konnten nicht gelöscht werden.")
  
                
     