# -*-coding:utf8;-*-
"""
The MIT License (MIT)

Copyright (c) 2022 zcache https://github.com/guangrei/zcache

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

from zcache.version import __version__
from zcache.Interface import StorageInterface
import time
import json
import os
from ftplib import FTP
from io import BytesIO
from typing import Dict, Any, Tuple, Union


class FTPStorage(StorageInterface):
    def __init__(
        self,
        path: str,
        host: str = "",
        user: str = "",
        password: str = "",
        persistent: str = "",
    ):
        self.host = os.environ.get("FTPHOST", host)
        self.user = os.environ.get("FTPUSER", user)
        self.password = os.environ.get("FTPPASSWORD", password)
        self.persistent = os.environ.get("FTPPERSISTENT", persistent)
        self._path = path
        if self.persistent == "True":
            self.connection = FTP(self.host)
            self.connection.login(user=self.user, passwd=self.password)
        exists, _type = self.exists(path)
        if not exists:
            self.create(path)
        self._path = path

    @property
    def filesystem(self) -> bool:
        return True

    @property
    def path(self) -> str:
        return self._path

    def create(self, path: str) -> None:
        data: Dict[str, Any] = {}
        data["first_created"] = time.strftime("%Y-%m-%d %H:%M:%S")
        data["version"] = __version__
        data["url"] = "https://github.com/guangrei/zcache"
        data["data"] = {}
        data["limit"] = 0
        self.save(data)

    def load(self) -> Dict[str, Any]:
        data = self.read(self._path)
        ret = json.loads(data.decode("utf-8"))
        return dict(ret)

    def save(self, data: Dict[str, Any]) -> None:
        json_encoded = json.dumps(data)
        json_encoded_bytes = json_encoded.encode("utf-8")
        self.write(self._path, json_encoded_bytes)

    def read(self, remote_file_path: str) -> bytes:
        # Menggunakan BytesIO untuk menyimpan data file di memory
        memory_file = BytesIO()
        if not self.persistent == "True":
            # Koneksi ke FTP server
            with FTP(self.host) as ftp:
                ftp.login(user=self.user, passwd=self.password)
                # Mendownload file ke memory
                ftp.retrbinary("RETR {}".format(remote_file_path), memory_file.write)

                # Pindahkan pointer ke awal agar siap untuk dibaca
                memory_file.seek(0)

                # Mengembalikan isi file
                return memory_file.read()
        else:
            # Mendownload file ke memory
            self.connection.retrbinary(
                "RETR {}".format(remote_file_path), memory_file.write
            )

            # Pindahkan pointer ke awal agar siap untuk dibaca
            memory_file.seek(0)

            # Mengembalikan isi file
            return memory_file.read()

    def write(self, remote_file_path: str, data: bytes) -> None:
        # Menggunakan BytesIO untuk membaca data file dari memory
        memory_file = BytesIO(data)
        if not self.persistent == "True":
            # Koneksi ke FTP server
            with FTP(self.host) as ftp:
                ftp.login(user=self.user, passwd=self.password)
                # Mengunggah file dari memory ke FTP server
                ftp.storbinary("STOR {}".format(remote_file_path), memory_file)
        else:
            self.connection.storbinary("STOR {}".format(remote_file_path), memory_file)

    def exists(self, remote_path: str) -> Tuple[bool, Union[bool, str]]:
        if not self.persistent == "True":
            # Koneksi ke FTP server
            with FTP(self.host) as ftp:
                ftp.login(user=self.user, passwd=self.password)

                try:
                    # Coba untuk mengubah direktori ke path yang diberikan
                    ftp.cwd(remote_path)
                    return True, "directory"
                except BaseException:
                    try:
                        # Jika gagal, coba cek apakah path tersebut adalah file
                        dir_name, file_name = os.path.split(remote_path)
                        ftp.cwd(dir_name)
                        files = ftp.nlst()
                        return file_name in files, "file"
                    except BaseException:
                        # Jika keduanya gagal, berarti path tidak ada
                        return False, False
        else:
            try:
                # Coba untuk mengubah direktori ke path yang diberikan
                self.connection.cwd(remote_path)
                return True, "directory"
            except BaseException:
                try:
                    # Jika gagal, coba cek apakah path tersebut adalah file
                    dir_name, file_name = os.path.split(remote_path)
                    self.connection.cwd(dir_name)
                    files = self.connection.nlst()
                    return file_name in files, "file"
                except BaseException:
                    # Jika keduanya gagal, berarti path tidak ada
                    return False, "file"

    def mkdir(self, remote_dir_path: str) -> bool:
        if not self.persistent == "True":
            # Koneksi ke FTP server
            with FTP(self.host) as ftp:
                ftp.login(user=self.user, passwd=self.password)

                try:
                    # Membuat direktori baru
                    ftp.mkd(remote_dir_path)
                    return True
                except BaseException:
                    # Jika terjadi kesalahan, return False
                    return False
        else:
            try:
                # Membuat direktori baru
                self.connection.mkd(remote_dir_path)
                return True
            except BaseException:
                # Jika terjadi kesalahan, return False
                return False

    def delete(self, remote_file_path: str) -> bool:
        if not self.persistent == "True":
            # Koneksi ke FTP server
            with FTP(self.host) as ftp:
                ftp.login(user=self.user, passwd=self.password)

                try:
                    # Hapus file dari FTP server
                    ftp.delete(remote_file_path)
                    return True
                except BaseException:
                    # Jika terjadi kesalahan, return False
                    return False
        else:
            try:
                # Hapus file dari FTP server
                self.connection.delete(remote_file_path)
                return True
            except BaseException:
                # Jika terjadi kesalahan, return False
                return False

    def __del__(self) -> None:
        if getattr(self, "connection"):
            self.connection.quit()
