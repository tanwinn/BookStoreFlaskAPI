from flask import Flask, Response, json, request
from werkzeug import exceptions

import data_reader

app = Flask(__name__)


@app.route("/books/<isbn>")
def get_isbn(isbn):
    # query param
    include_author = request.args.get("includeAuthor") == "1"
    related_depth = int(request.args.get("includeRelated", 0))

    book_title = data_reader.get_title_by_isbn(isbn)
    if not book_title:
        raise exceptions.NotFound

    result = {
        "isbn": isbn,
        "title": book_title,
    }

    if include_author:
        author = data_reader.get_author_by_isbn(isbn)
        if author:
            result.update(author={"id": author.id, "name": author.name})
        else:
            result.update(author={})

    if related_depth > 0:
        related_isbns = data_reader.get_related_by_isbn(isbn, related_depth)
        related_isbns.remove(isbn)
        related = []
        for related_isbn in related_isbns:
            related.append(
                {
                    "isbn": related_isbn,
                    "title": data_reader.get_title_by_isbn(related_isbn),
                }
            )
        result.update(related=related)

    return json.dumps(result), 200, {"Content-Type": "application/json"}
