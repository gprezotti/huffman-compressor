from pathlib import Path


class FileHandler:
    @staticmethod
    def read_binary(path):
        return Path(path).read_bytes()

    @staticmethod
    def write_binary(path, data):
        Path(path).write_bytes(data)
