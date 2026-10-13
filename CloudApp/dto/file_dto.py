from dataclasses import dataclass

@dataclass(frozen=True)
class StoredFileDTO:
    uuid : str
    original_filename : str
    storage_filename :str
    file_size : int

    
