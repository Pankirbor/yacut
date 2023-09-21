from random import choices
from string import digits, ascii_letters

SIMBOLS = digits + ascii_letters


def get_unique_short_id(all_links):
    all_short_links = [link.short for link in all_links]
    short_link = None

    while True:
        short_link = "".join(choices(SIMBOLS, k=6))
        if short_link not in set(all_short_links):
            break

    return short_link


def search_existing_link(all_links, original_link):
    for item in all_links:
        if item.original == original_link:
            return item
