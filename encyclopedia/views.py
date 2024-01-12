import markdown2
from django.shortcuts import render, redirect
from django.forms import Form, CharField, Textarea, ValidationError, TextInput
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, *, title: str):
    entry_content_in_markdown = util.get_entry(title)
    if entry_content_in_markdown is None:
        return render(request, "encyclopedia/error.html")

    markdown_to_html_converter = markdown2.Markdown()
    entry_content_in_html = markdown_to_html_converter.convert(entry_content_in_markdown)
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


class NewPageContentForm(Form):
    page_title = CharField(label="Enter the page name here", widget=TextInput(attrs={'rows': 1}))
    page_content = CharField(label="Enter page content here",
                             widget=Textarea(attrs={'rows': 11, 'style': 'display: block;'}))

    def clean_page_title(self):
        cleaned_page_title = self.cleaned_data.get('page_title')
        page_title_already_exists = util.get_entry(cleaned_page_title) is not None
        if page_title_already_exists:
            raise ValidationError("Page title already exists!")

        return cleaned_page_title


def create_new_page(request):
    if request.method == "GET":
        page_content_form = NewPageContentForm()
        return render(request, "encyclopedia/create-new-page.html", {
            "page_content_form": page_content_form
        })

    if request.method == "POST":
        page_content_form = NewPageContentForm(request.POST)
        if page_content_form.is_valid():
            page_title = page_content_form.cleaned_data['page_title']
            page_content = page_content_form.cleaned_data['page_content']
            util.save_entry(page_title, page_content)
            return redirect("encyclopedia:entry", title=page_title)

        return render(request, "encyclopedia/create-new-page.html", {
            "page_content_form": page_content_form
        })


class EditPageContentForm(Form):
    page_content = CharField(label="Edit page content here",
                             widget=Textarea(attrs={'rows': 11, 'style': 'display: block;'}))


def edit_page(request, *, title: str):
    if request.method == "GET":
        initial_page_content = util.get_entry(title)
        edit_page_content_form = EditPageContentForm(initial={'page_content': initial_page_content})
        return render(request, "encyclopedia/edit-page.html", {
            "title": title,
            "edit_page_content_form": edit_page_content_form
        })

    if request.method == "POST":
        edited_page_content_form = EditPageContentForm(request.POST)
        if edited_page_content_form.is_valid():
            edited_page_content = edited_page_content_form.cleaned_data['page_content']
            util.save_entry(title, edited_page_content)
            return redirect("encyclopedia:entry", title=title)

        return render(request, "encyclopedia/error.html")
