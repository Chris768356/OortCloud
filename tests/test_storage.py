import io
from werkzeug.datastructures import FileStorage
from CloudApp.services.storage import StorageService

def test_save_and_get_file(tmp_path):
  
    storage = StorageService(str(tmp_path))
    user_uuid = "1234567890abcdef1234567890abcdef"
    
   
    dummy_content = b"Hallo Cloud"
    fake_file = FileStorage(
        stream=io.BytesIO(dummy_content),
        filename="test_dokument.pdf"
    )

    
    dto = storage.save_file(fake_file, user_uuid)

    
    assert dto.original_filename == "test_dokument.pdf"
    assert dto.file_size == 11
    assert dto.storage_filename.endswith(".pdf")
    
    saved_path = storage.get_file_path(dto.storage_filename, user_uuid)
    assert saved_path is not None
    assert saved_path.is_file()
    assert saved_path.read_bytes() == dummy_content


def test_delete_file(tmp_path):
    storage = StorageService(str(tmp_path))
    user_uuid = "1234567890abcdef1234567890abcdef"
    fake_file = FileStorage(stream=io.BytesIO(b"Inhalt"), filename="weg_damit.txt")
    
    dto = storage.save_file(fake_file, user_uuid)

    storage.delete_file(dto.storage_filename, user_uuid)
    assert storage.get_file_path(dto.storage_filename, user_uuid) is None