from django.shortcuts import render, redirect
from markdown2 import markdown
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title: str):
    entry_content_in_markdown = util.get_entry(title)
    if entry_content_in_markdown is None:
        return render(request, "encyclopedia/error.html")

    entry_content_in_html = markdown(entry_content_in_markdown)
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "entry_content": entry_content_in_html
    })


def search(request):
    if request.method != "GET":
        print("Encyclopedia entry search isn't using GET method.")
        return render(request, "encyclopedia/entry.html")

    entry_title_parameter = request.GET.get('q', '')

    entry_found = util.get_entry(entry_title_parameter) is not None
    if entry_found:
        return redirect("encyclopedia:entry", title=entry_title_parameter)

    search_results = []
    entry_titles = util.list_entries()
    for entry_title in entry_titles:
        if entry_title_parameter.lower() in entry_title.lower():
            search_results.append(entry_title)

    return render(request, "encyclopedia/search.html", {
        "search_results": search_results
    })
