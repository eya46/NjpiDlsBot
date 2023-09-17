from urllib.parse import urlparse


def url_to_proxy(url: str) -> str:
    _ = urlparse(url)
    return "https://{0}{1}{2}.atrust.njpi.edu.cn{3}{4}".format(
        _.hostname.replace(".", "-"),
        (f"-{_.port}-p" if _.port else ""),
        ("-s" if _.scheme == "https" else ""),
        (_.path if _.path else "/"),
        (f"?{_.query}" if _.query else "")
    )
