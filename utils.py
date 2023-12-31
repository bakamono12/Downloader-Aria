import re
import requests
import logging

logger = logging.getLogger(__name__)

PATH = "./downloads"
EMOJI = ["😀", "😃", "😄", "😁", "😆", "😅", "😂", "🤣", "😊", "😇", "🙂", "🙃", "😉", "😌", "😍", "🥰", "😘", "😗", "😙", "😚", ]


async def is_download_link(url):
    for link in url:
        try:
            response = requests.get(link, stream=True, allow_redirects=True)
            content_disposition = response.headers.get("Content-Disposition", "")
            content_type = response.headers.get("Content-Type", "")
            mime_type = ["video/mp4", "video/x-matroska", "application/octet-stream", "video/3gpp", "video/quicktime",
                         "video/x-msvideo", "video/x-ms-wmv", "video/x-flv", "video/webm", "video/x-m4v", "video/MP2T",
                         "video/3gpp", "video/quicktime", "video/x-msvideo", "video/x-ms-wmv", "video/x-flv",
                         "video/webm",
                         "video/x-m4v"]
            if "attachment" in content_disposition.lower() or content_type in mime_type:
                return True
        except Exception as e:
            print(f"Error checking headers: {e}")
        return False


async def extract_gid(message_update):
    gid = [item.split(':')[1].strip() for item in message_update.split('\n') if 'GID' in item or 'Name' in item]
    return gid if gid else None


def extract_links(message):
    # fetch all links
    try:
        url_pattern = r'https?://\S+'
        matches = re.findall(url_pattern, message)

        return matches
    except Exception as e:
        logger.error(f"Error extracting links: {e}")
        return []
