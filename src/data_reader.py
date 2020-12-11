"""Preprocess data and provide util methods for APP"""

import dataclasses as dt
import logging
from pprint import pformat as pf

import books

AUTHORS_BY_ISBN = {}
AUTHORS_BY_ID = {}
TITLE_BY_ISBN = {}
RELATED = {}
LOGGER = logging.getLogger(__name__)


@dt.dataclass
class Author:
    """Author dataclass"""

    id: str = None
    name: str = None


def get_author_by_isbn(isbn: str) -> Author:
    if not AUTHORS_BY_ISBN:
        _parse_author_data()
    return AUTHORS_BY_ISBN.get(isbn)


def get_title_by_isbn(isbn: str) -> str:
    if not TITLE_BY_ISBN:
        _parse_title_data()
    return TITLE_BY_ISBN.get(isbn)


def get_related_by_isbn(isbn: str, depth: int) -> dict:
    if not RELATED:
        _parse_related_book_data()
    book_included = set()
    i = 0
    queue = [(isbn, 0)]
    while i < len(queue):
        LOGGER.debug(queue[i])
        isbn = queue[i][0]
        current_depth = queue[i][1]
        if current_depth > depth:
            break
        book_included.add(isbn)
        related_isbns = RELATED.get(isbn, [])
        for rel_isbn in related_isbns:
            if rel_isbn not in book_included:
                queue.append((rel_isbn, current_depth + 1))
        i += 1
    return book_included


def _parse_author_data():
    for entry in books.AUTHORS:
        author_id = entry["id"]
        AUTHORS_BY_ID[author_id] = Author(id=author_id, name=entry["name"])

    for entry in books.BOOKS_AUTHORS:
        isbn = entry["isbn"]
        author_id = entry["authorId"]
        AUTHORS_BY_ISBN.update({isbn: AUTHORS_BY_ID[author_id]})


def _parse_title_data():
    for entry in books.BOOKS:
        TITLE_BY_ISBN[entry["isbn"]] = entry["title"]


def _parse_related_book_data():
    for entry in books.BOOKS_RELATED:
        if entry["isbn"] in RELATED:
            RELATED[entry["isbn"]].append(entry["relatedIsbn"])
        else:
            RELATED[entry["isbn"]] = [entry["relatedIsbn"]]
