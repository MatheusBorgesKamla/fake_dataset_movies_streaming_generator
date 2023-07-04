import csv

class DataTypeNotSupportedForIngestionException(Exception):
    def __init__(self, data):
        self.data = data
        self.message = f"Data type {type(data)} is not supported for ingestion"
        super().__init__(self.message)
        
class Writer:
    
    def __init__(self, path: str, overwrite = True) -> None:
        self.path = path
        self.overwrite = overwrite
    
    def erase_file(self) -> None:
        f = open(self.path, 'w')
        f.close()
    
    def write_row(self, row: str) -> None:
        with open(self.path, 'a') as f:
            f.write(row+"\n")

    
    def write_csv(self, data: list) -> None:
        file_cond = "w" if self.overwrite else "a"

        if isinstance(data, list):
            with open(self.path, file_cond) as f:
                writer = csv.DictWriter(f, fieldnames=list(data[0].keys()))
                writer.writeheader()
                writer.writerows(data)
        else:
            raise DataTypeNotSupportedForIngestionException(data)