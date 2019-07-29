from datetime import datetime


class Entry(object):

    class Author(object):
        NAME = "name"
        URI = "uri"

        def __init__(self, name, uri):
            self._name = name
            self._uri = uri

        @staticmethod
        def create_author(author):
            return Entry.Author(author.find(Entry.Author.NAME),
                                author.find(Entry.Author.URI))

    class Category(object):
        LABEL = 'label'
        TERM = 'term'

        def __init__(self, label, term):
            self._label = label
            self._term = term

        @staticmethod
        def create_category(category):
            if category:
                return Entry.Category(category.get(Entry.Category.LABEL),
                                      category.get(Entry.Category.TERM))

    class Content(object):
        TYPE = "type"

        def __init__(self, cnt_type, cont):
            self._type = cnt_type
            self._cont = cont

        @staticmethod
        def create_content(cnt):
            return Entry.Content(cnt[Entry.Content.TYPE], cnt.text)

    def __init__(self, author, category, content, link, updated, title):
        self._author = author
        self._category = category
        self._content = content
        self._link = link
        self._update = datetime.strptime(
            ''.join(updated.rsplit(':', 1)), '%Y-%m-%dT%H:%M:%S%z')
        self._title = title

    @staticmethod
    def create_entry(xml_entry):
        a = Entry.Author.create_author(xml_entry.find("author"))
        cat = Entry.Category.create_category(xml_entry.find("category"))
        cnt = Entry.Content.create_content(xml_entry.find("content"))
        lnk = xml_entry.find("link").get('href')
        updated = xml_entry.find("updated").text
        title = xml_entry.find("title").text

        return Entry(a, cat, cnt, lnk, updated, title)
