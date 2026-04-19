from typing import Optional


def build_absolute_file_url(request, file_field) -> Optional[str]:
    """Returns the absolute URL for File/ImageField or None."""
    if not file_field:
        return None
    url = getattr(file_field, "url", None)
    if not url:
        return None
    if request:
        try:
            return request.build_absolute_url(url)
        except Exception:
            return url
    return url
