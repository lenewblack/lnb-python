from __future__ import annotations

from typing import Any, Dict, Generator, Optional

from lnb._pagination import ResultSet, paginate
from lnb._types import RequestOptions
from lnb.models.file import FileObject
from lnb.services._base import BaseService


class FileService(BaseService):
    _PATH = "files"

    def list(
        self,
        filters: Optional[Dict[str, Any]] = None,
        *,
        options: Optional[RequestOptions] = None,
    ) -> ResultSet[FileObject]:
        raw = self._request("GET", self._PATH, params=filters, options=options)
        return ResultSet.from_raw(FileObject, raw)

    def paginate(
        self,
        filters: Optional[Dict[str, Any]] = None,
        *,
        options: Optional[RequestOptions] = None,
    ) -> Generator[FileObject, None, None]:
        yield from paginate(self.list, filters=filters, options=options)

    def get(
        self,
        file_id: str,
        *,
        options: Optional[RequestOptions] = None,
    ) -> FileObject:
        raw = self._request("GET", f"{self._PATH}/{file_id}", options=options)
        return self._parse(FileObject, raw)

    def upload(
        self,
        filename: str,
        content: bytes,
        mime_type: str = "application/octet-stream",
        *,
        options: Optional[RequestOptions] = None,
    ) -> FileObject:
        """Upload a file using multipart/form-data."""
        files = {"file": (filename, content, mime_type)}
        raw = self._request("POST", self._PATH, files=files, options=options)
        return self._parse(FileObject, raw)

    def delete(
        self,
        file_id: str,
        *,
        options: Optional[RequestOptions] = None,
    ) -> None:
        self._request("DELETE", f"{self._PATH}/{file_id}", options=options)
