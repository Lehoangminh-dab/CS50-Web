from django.shortcuts import render
from markdown2 import markdown
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title: str):
    entry_content_md = util.get_entry(title)
    if entry_content_md is None:
        return render(request, "encyclopedia/error.html")

    entry_content_html = markdown(entry_content_md)
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "entry_content": entry_content_html
    })
