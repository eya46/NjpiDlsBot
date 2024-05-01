from urllib.parse import urlparse


def url_to_proxy(url: str) -> str:
    _ = urlparse(url)
    return "https://{}{}{}.atrust.njpi.edu.cn{}{}".format(
        _.hostname.replace(".", "-"),
        (f"-{_.port}-p" if _.port else ""),
        ("-s" if _.scheme == "https" else ""),
        (_.path if _.path else "/"),
        (f"?{_.query}" if _.query else ""),
    )
