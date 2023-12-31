d = """Status: active
Name: Best of OLED Ever in 8K HDR ULTRA HD 240 FPS Dolby Vision.mp4
Downloaded: 4.26%
DownloadSpeed': 2.38 MiB/s
ETA: 17m42s
GID: fb11825cd2ff7995"""


def extract_gid(message_update):
    gid = [item.split(':')[1].strip() for item in message_update.split('\n') if 'GID' in item or 'Name' in item]
    return gid if gid else None


print(extract_gid(d))
