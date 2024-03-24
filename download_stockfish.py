import os
import sys
import zipfile
import requests
import os
import sys
import stat
import shutil
import tarfile


platform = sys.platform
file_extension = ".exe" if platform == "win32" else ""
stockfish_path = f"./TEMP/sf{file_extension}"

def download_sf() -> None:
    """Download Stockfish 15."""
    if os.path.exists(stockfish_path):
        return

    windows_or_linux = "windows" if platform == "win32" else "ubuntu"
    sf_base = f"stockfish-{windows_or_linux}-x86-64-modern"
    archive_ext = "zip" if platform == "win32" else "tar"
    archive_link = f"https://github.com/official-stockfish/Stockfish/releases/download/sf_16/{sf_base}.{archive_ext}"

    response = requests.get(archive_link, allow_redirects=True)
    archive_name = f"./TEMP/sf_zip.{archive_ext}"
    with open(archive_name, "wb") as file:
        file.write(response.content)

    archive_open = zipfile.ZipFile if archive_ext == "zip" else tarfile.TarFile
    with archive_open(archive_name, "r") as archive_ref:
        archive_ref.extractall("./TEMP/")

    exe_ext = ".exe" if platform == "win32" else ""
    shutil.copyfile(f"./TEMP/stockfish/{sf_base}{exe_ext}", stockfish_path)

    if windows_or_linux == "ubuntu":
        st = os.stat(stockfish_path)
        os.chmod(stockfish_path, st.st_mode | stat.S_IEXEC)

os.makedirs("TEMP", exist_ok=True)
download_sf()

