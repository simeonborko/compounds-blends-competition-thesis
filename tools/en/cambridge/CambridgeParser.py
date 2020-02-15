from html.parser import HTMLParser


class CambridgeParser(HTMLParser):

    inside = False
    found = False
    depth = 0
    entry = ''
    text = ''

    def handle_starttag(self, tag, attrs):
        if tag == 'span':
            if len(attrs) == 1 and attrs[0][0] == 'class' and 'ipa' in attrs[0][1] and not self.found:
                self.inside = True
                self.found = True
            if self.inside:
                self.depth += 1

    def handle_endtag(self, tag):
        if tag == 'span' and self.inside:
            self.depth -= 1
            if self.depth == 0:
                self.inside = False
            elif self.depth < 0:
                raise Exception

    def handle_data(self, data):
        if self.inside:
            self.text += data

    def error(self, message):
        raise NotImplementedError
