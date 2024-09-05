import tempfile
from django.core.files.storage import FileSystemStorage
from django.utils.deconstruct import deconstructible


@deconstructible
class TempFileSystemStorage(FileSystemStorage):
    def __init__(
        self,
        base_url=None,
        file_permissions_mode=None,
        directory_permissions_mode=None,
    ):
        super().__init__(
            tempfile.gettempdir(),
            base_url,
            file_permissions_mode,
            directory_permissions_mode,
        )
