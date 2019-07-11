import mistune

class ClassRenderer(mistune.Renderer):
    """
    Applying classes to the rendered html
    This is here for the purpose of applying Tachyons styling directly,
    instead of having to write the CSS
    Since blog content is dynamic, we have to apply the classes
    while in the renderer.
    FIXME: find a better solution: don't rely on copy-pasting code of the lib
    """

    # A dict mapping HTML elements to classes.
    cls = {
        'paragraph': 'tj pl3 pr3 pl0-ns pl0-ns', # <p>
        'h1': 'f2 pb2 pl3 pr3 pl0-ns pl0-ns bb bw2 b--dark-blue',
        'h2': 'f2 pb1 pl3 pr3 pl0-ns pl0-ns bb bl-0 bt-0 br-0 b--dashed b--dark-blue bw1',
        'h3': 'f3 pl3 pr3 pl0-ns pl0-ns',
        'h4': 'f4 pl3 pr3 pl0-ns pl0-ns',
        'h5': 'f5 pl3 pr3 pl0-ns pl0-ns',
        'h6': 'f6 pl3 pr3 pl0-ns pl0-ns',
        'table': 'green',
        'image': '', # <img>
        'link': '', # <a>
        'block_code': 'pl3 pr3 pl0-ns pl0-ns', # <pre> -> <code>
    }

    def paragraph(self, text):
        """Rendering paragraph tags. Like ``<p>``."""
        return '<p class="%s">%s</p>\n' % (self.cls['paragraph'], text.strip(' '))

    def header(self, text, level, raw=None):
        """Rendering header/heading tags like ``<h1>`` ``<h2>``.
        :param text: rendered text content for the header.
        :param level: a number for the header level, for example: 1.
        :param raw: raw text content of the header.
        """
        return '<h%d class="%s">%s</h%d>\n' % (level,
                                             self.cls['h' + str(level)], # determine the correct entry in dict
                                             text, level)

    def table(self, header, body):
        """Rendering table element. Wrap header and body in it.
        :param header: header part of the table.
        :param body: body part of the table.
        """
        return (
                   '<table class="%s">\n<thead>%s</thead>\n'
                   '<tbody>\n%s</tbody>\n</table>\n'
               ) % (self.cls['table'], header, body)

    def image(self, src, title, text):
        """Rendering a image with title and text.
        :param src: source link of the image.
        :param title: title text of the image.
        :param text: alt text of the image.
        """
        src = mistune.escape_link(src)
        text = mistune.escape(text, quote=True)
        if title:
            title = mistune.escape(title, quote=True)
            html = '<img src="%s" alt="%s" title="%s" class="%s"' % (src, text, title, self.cls['image'])
        else:
            html = '<img src="%s" alt="%s" class="%s"' % (src, text, self.cls['image'])
        if self.options.get('use_xhtml'):
            return '%s />' % html
        return '%s>' % html

    def link(self, link, title, text):
        """Rendering a given link with content and title.
        :param link: href link for ``<a>`` tag.
        :param title: title content for `title` attribute.
        :param text: text content for description.
        """
        link = mistune.escape_link(link)
        if not title:
            return '<a href="%s">%s</a>' % (link, text)
        title = mistune.escape(title, quote=True)

        return '<a href="%s" title="%s" class="%s">%s</a>' % (link, title,
                                                              self.cls['link'],
                                                              text)

    def block_code(self, code, lang=None):
        """Rendering block level code. ``pre > code``.
        :param code: text content of the code block.
        :param lang: language of the given code.
        """
        code = code.rstrip('\n')
        if not lang:
            code = mistune.escape(code, smart_amp=False)
            return '<pre><code>%s\n</code></pre>\n' % code
        code = mistune.escape(code, quote=True, smart_amp=False)

        return '<pre class="%s"><code class="lang-%s">%s\n</code></pre>\n' % (self.cls['block_code'], lang, code)

def markdown(content):
    renderer = ClassRenderer()
    markdown_f = mistune.Markdown(renderer=renderer)
    return markdown_f(content)
