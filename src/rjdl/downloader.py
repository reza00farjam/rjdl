import os
import sys
import time
import requests


def downloader(url: str, path: str = "", show_download_progress: bool = True) -> None:

    """Downloads given direct download link at the given path.
    (It will use default path if the given path wasn't accessible)

    Args:
        url (:obj:`str`): Valid downloadable url.
        path (:obj:`str`): Download path.
        show_download_progress (:obj:`bool`): Show download progress bar trigger.

    Raises:
        :class:`BrokenPipeError`
        :class:`ConnectionError`
        :class:`FileExistsError`
    """

    if path and path.endswith("\\"):
        path = path[:-1]

    if not os.path.exists(path):
        if not os.access(os.path.dirname(path), os.W_OK):
            path = ""
        else:
            os.mkdir(path)

    if path and not path.endswith("\\"):
        path += "\\"

    try:
        header = requests.head(url, allow_redirects=True)
        file_name = header.url.split("/")[-1]
    except requests.exceptions.ConnectionError:
        raise ConnectionError("Check your connection") from None

    if os.path.isfile(path + file_name):
        raise FileExistsError("File already exists")

    with open(path + file_name, "wb") as file:
        try:
            response = requests.get(url, allow_redirects=True, stream=True)
            total_length = response.headers["Content-Length"]
        except requests.exceptions.ConnectionError:
            raise ConnectionError("Check your connection") from None

        if total_length is None:
            file.write(response.content)
        else:
            try:
                dl = 0
                start = time.perf_counter()
                total_length = int(total_length.strip())

                for data in response.iter_content(chunk_size=4096):
                    dl += len(data)
                    file.write(data)

                    if show_download_progress:
                        done = int(50 * dl / total_length)

                        sys.stdout.write(
                            "\r|{}{}| {:3}% | {:7.2f} kbps ".format(
                                "\U00002588" * done,
                                "-" * (50 - done),
                                2 * done,
                                round((dl / (time.perf_counter() - start)) / 1000, 2),
                            )
                        )
                        sys.stdout.flush()
                if show_download_progress:
                    print("")
            except Exception:
                file.close()
                os.remove(path + file_name)

                raise BrokenPipeError("Connection has been broken") from None
