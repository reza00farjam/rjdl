from urllib import parse

from click import ParamType


class URLType(ParamType):
    name = "url"

    def convert(self, value, param, ctx):
        url = parse.urlparse(value)

        if url.netloc != "www.radiojavan.com":
            self.fail(f"{url.netloc} is not a valid url", param, ctx)
        if url.scheme != "https":
            url = url._replace(scheme="https")

        return url.geturl()
