from hashlib import sha1
from struct import unpack

import bencodepy
import requests
from bencode import Decoder, Encoder


def parse_torrent(torrent_path: str, decode=bencodepy.decode):
    with open(torrent_path, "rb") as f:
        return decode(f.read())


def get_torrent_peers(info_hash, announcer_url, size, port):
    data = {
        "info_hash": info_hash,
        "peer_id": "-PC0001-474569229936",
        "uploaded": "0",
        "downloaded": "0",
        "left": size,
        "port": port,
        "compact": "1"
    }
    r = requests.get(announcer_url, params=data)
    return r.content


def chunks(peers, n):
    for i in range(0, len(peers), n):
        yield peers[i:i + n]


if __name__ == '__main__':
    # Main blog
    # https://blog.jse.li/posts/torrent/
    decoder = Decoder()
    encoder = Encoder()
    torrent_info = parse_torrent("ubuntu-20.04.1-desktop-amd64.iso.torrent", decode=decoder.decode)
    announce_url = torrent_info[b"announce"]
    torrent_size = torrent_info[b"info"][b"length"]
    info_bencode = encoder.encode(torrent_info[b'info'])
    info_hash = sha1(info_bencode).digest()

    expected_hash = b"\xd1\x10\x1a+\x9d (\x11\xa0^\x8cW\xc5W\xa2\x0b\xf9t\xdc\x8a"
    assert info_hash == expected_hash
    data = get_torrent_peers(info_hash, announce_url, torrent_size, 7000)
    torrent_tracker_info = decoder.decode(data)
    print(torrent_tracker_info)
    peers = torrent_tracker_info[b"peers"]
    for chunk in chunks(peers, 6):
        ip = ".".join([str(i) for i in chunk[:4]])
        port = unpack(">H", chunk[4:6])[0]
        print(ip, port)

