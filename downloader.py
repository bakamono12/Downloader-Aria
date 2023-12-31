import os
import time
import threading
from aria2p import API, Download, Client

domain = os.environ.get("RAILWAY_PUBLIC_DOMAIN") or "http://localhost"
port = os.environ.get("PORT") or 6800


class Aria2Downloader:
    def __init__(self, download_dir='downloads'):
        self.download_dir = download_dir
        self.aria2 = API(Client(
            host=domain,
            port=port,
            secret="baka")
        )

    def start_download(self, url):
        options = {
            'dir': self.download_dir,
        }
        download = self.aria2.add_uris([url], options=options)
        # threading.Thread(target=self._check_download_status(download), args=(download,), daemon=True).start()
        return self._check_download_status(download)

    def _check_download_status(self, download):
        while not download.is_complete:
            download.update()
            status = download.status
            download_speed = download.download_speed_string or 0
            eta = download.eta_string or 0

            progress_info = {
                'gid': download.gid,
                'status': status,
                'name': download.name,
                'downloaded': download.progress_string(),
                'download_speed': download_speed(),
                'eta': eta(),
                'is_complete': download.is_complete
            }
            yield progress_info
        return f"Download complete: {download.name} ({download.files[0]})"

    def cancel_download(self, gid):
        download = self.aria2.get_download(gid)
        if download:
            download.remove()

    def pause_download(self, gid):
        download = self.aria2.get_download(gid)
        if download:
            download.pause()

    def resume_download(self, gid):
        download = self.aria2.get_download(gid)
        if download:
            download.resume()

# if __name__ == "__main__":
#     downloader = Aria2Downloader()
