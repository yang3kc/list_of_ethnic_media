import tldextract
from urllib.parse import urlparse, urlunparse


def extract_domain(url):
    """
    Extracts the main domain (e.g., example.com) from a URL using tldextract.

    Parameters:
        url (str): The input URL.

    Returns:
        str: The extracted domain (e.g., example.com), or an empty string if not valid.

    Examples:
        >>> extract_domain("https://www.example.com/path")
        'example.com'
        >>> extract_domain("http://sub.example.co.uk/page")
        'example.co.uk'
        >>> extract_domain("invalid-url")
        ''
    """
    url = url.strip()
    ext = tldextract.extract(url)
    if ext.domain and ext.suffix:
        domain = f"{ext.domain}.{ext.suffix}"
        domain = domain.lower()
        return domain
    return ""


def remove_parameters(url):
    """
    Removes query parameters and fragments from a URL while preserving the path.

    Parameters:
        url (str): The input URL to clean.

    Returns:
        str: The URL without query parameters and fragments.

    Examples:
        >>> remove_parameters("https://example.com/page?param=value#section")
        'https://example.com/page'
        >>> remove_parameters("https://example.com/path/to/page")
        'https://example.com/path/to/page'
        >>> remove_parameters("https://example.com/page")
        'https://example.com/page'
    """
    url = url.strip()
    try:
        # Parse the URL into components
        parsed = urlparse(url)
        # Reconstruct the URL without query and fragment
        cleaned = urlunparse(
            (
                parsed.scheme,
                parsed.netloc,
                parsed.path,
                "",  # params
                "",  # query
                "",  # fragment
            )
        )
        return cleaned
    except Exception:
        # If URL parsing fails, return the original URL
        return url


def extract_path(url):
    """
    Extracts the path component from a URL.

    Parameters:
        url (str): The input URL to extract the path from.

    Returns:
        str: The path component of the URL. Returns an empty string if URL parsing fails
             or if the path is just "/".

    Examples:
        >>> extract_path("https://example.com/path/to/page")
        '/path/to/page'
        >>> extract_path("https://example.com")
        ''
        >>> extract_path("https://example.com/")
        ''
        >>> extract_path("example.com")
        ''
        >>> extract_path("example.com/path")
        '/path'
        >>> extract_path("invalid-url")
        ''
        >>> extract_path("https://example.com/path//to///page")
        '/path/to/page'
        >>> extract_path(None)
        ''
        >>> extract_path("")
        ''
    """
    url = url.strip()
    if not url:  # Handle None or empty string
        return ""

    try:
        # Normalize the URL string
        url = str(url).strip()

        # Add scheme if missing to handle bare domains
        if not url.startswith(("http://", "https://")):
            url = "https://" + url

        # Parse the URL and get path
        parsed = urlparse(url)
        path = parsed.path

        # Clean up the path
        if not path or path == "/":
            return ""

        # Normalize path by removing duplicate slashes and trailing slash
        path = "/" + "/".join(filter(None, path.split("/")))
        path = path.lower()
        return path

    except Exception:
        return ""
