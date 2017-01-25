def html_decode(s):
    """
    Returns the ASCII decoded version of the given HTML string. This does
    NOT remove normal HTML tags like <p>.
    """

    htmlCodes = (("'", '&#39;'), ('"', '&quot;'), ('>', '&gt;'), ('<',
                 '&lt;'), ('&', '&amp;'))
    for code in htmlCodes:
        s = s.replace(code[1], code[0])
    return s
