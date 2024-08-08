from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import Storage
from django.utils import timezone
from django.utils.functional import LazyObject
from django.utils.module_loading import import_string


def get_storage_class(import_path: str | None = None) -> Storage:
    return import_string(import_path or settings.DELTY_FILE_STORAGE)


class DefaultStorage(LazyObject):
    def _setup(self):
        self._wrapped = import_string(settings.DELTY_FILE_STORAGE)()


delty_storage = DefaultStorage()


class StorageService:
    STORE_DIRECTORY = "element-snapshots"

    def upload_message(self, content: str, hash: str) -> str:
        """Upload email_message content to S3 bucket, and return file's full S3
        URL.
        """
        try:
            file_path = self.generate_file_path(hash)
            content_file = ContentFile(content.encode())
            delty_storage.save(file_path, content_file)  # type: ignore
            # This is used in order to remove authentication from the URL
            delty_storage.querystring_auth = False
            return delty_storage.url(file_path)  # type: ignore
        except Exception as exc:
            raise exc

    @classmethod
    def generate_file_path(cls, element_hash: str) -> str:
        return "{}/{}_{}.html".format(
            cls.STORE_DIRECTORY,
            f"{element_hash}",
            timezone.now().strftime("%Y%m%d%-H%M%S"),
        )
