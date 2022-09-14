from dataclasses import dataclass
from simple_term_menu import TerminalMenu

from .nyaa import Torrent


@dataclass
class MenuItem:
    title: str
    details: str
    target: Torrent


def ask(l: list[Torrent], prompt=False):
    l = l[:20]
    items = [MenuItem(
        title=torrent.name,
        details=(
            f'Category: {torrent.category} | Date: {torrent.date}'
            f' | Size: {torrent.size}'
            '\n'
            f'Seeds: {torrent.seeds} | Peers: {torrent.peers}'
            f' | Downloads: {torrent.downloads}'
        ),
        target=torrent,
    ) for torrent in l]
    if not prompt:
        try:
            result = show_term_menu(items)
        except Exception:
            result = simple_term_ask(items)
    else:
        result = simple_term_ask(items)
    return result


def show_term_menu(items: list[MenuItem]):
    cli_items = [
        f'[{get_key(index)}] ' + item.title.replace('|', '\\|') + '|' + (
            item.details.replace('|', '\\|')
        ) for index, item in enumerate(items)
    ]
    menu = TerminalMenu(
        cli_items,
        title='Select a torrent:',
        preview_title='Details',
        preview_size=0.4,
        preview_command=str,
        clear_screen=True,
    )
    try:
        index = menu.show()
    except Exception as e:
        menu._reset_term()
        raise e
    if index is None:
        return None
    return items[index].target


def get_key(i: int):
    if i < 10:
        return i
    return chr(ord('a') + i - 10)


def simple_term_ask(items: list[MenuItem]):
    items = list(reversed(items))
    size = len(items)
    for index, item in enumerate(items):
        index = size - index
        print(index, item.title)
        print('...', item.details.replace('\n', '\n... '))
        print('-' * 20)
    index = input(f'Your choice [1-{size}] > ')
    try:
        index = int(index)
        index = size - index
        if index < 0 or index >= size:
            raise ValueError('Out of range')
    except ValueError:
        print('Invalid choice')
        return None
    return items[index].target
