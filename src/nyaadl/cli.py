from simple_term_menu import TerminalMenu

from .nyaa import Torrent


def ask(l: list[Torrent]):
    items = [
        f'[{get_key(index)}] ' + torrent.name.replace('|', '\\|') + '|' + (
            f'Category: {torrent.category} \\| Date: {torrent.date}'
            f' \\| Size: {torrent.size}'
            '\n'
            f'Seeds: {torrent.seeds} \\| Peers: {torrent.peers}'
            f' \\| Downloads: {torrent.downloads}'
        ) for index, torrent in enumerate(l)
    ]
    menu = TerminalMenu(
            items[:20],
        title='Select a torrent:',
        preview_title='Details',
        preview_size=0.4,
        preview_command=str,
        clear_screen=True,
    )
    index = menu.show()
    if index is None:
        return None
    return l[index]


def get_key(i: int):
    if i < 10:
        return i
    return chr(ord('a') + i - 10)
