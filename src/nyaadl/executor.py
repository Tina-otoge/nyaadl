from .nyaa import Torrent
from . import config

import subprocess

def run(torrent: Torrent, command=None):
    command = command or config.get('command')
    args = [x.format(torrent.torrent_url) for x in command.split()]
    subprocess.run(args)
