"""Helper functions for qBittorrent."""

from qbittorrent.client import Client


def setup_client(url: str, username: str, password: str, verify_ssl: bool) -> Client:
    """Create a qBittorrent client."""
    client = Client(url, verify=verify_ssl)
    client.login(username, password)
    # Get an arbitrary attribute to test if connection succeeds
    client.get_alternative_speed_status()
    return client


def seconds_to_hhmmss(seconds):
    """Convert seconds to HH:MM:SS format."""
    if seconds == 8640000:
        return "None"

    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"


def format_unix_timestamp(timestamp):
    """Format a UNIX timestamp to a human-readable date."""
    dt_object = datetime.fromtimestamp(timestamp, tz=UTC)
    formatted_date = dt_object.strftime("%Y-%m-%dT%H:%M:%S%z")
    return formatted_date


def format_progress(torrent):
    """Format the progress of a torrent."""
    progress = torrent["progress"]
    progress = float(progress) * 100
    progress = f"{progress:.2f}"

    return progress


def format_torrents(torrents: list[dict[str, Any]]):
    """Format a list of torrents."""
    value = {}
    for torrent in torrents:
        value[torrent["name"]] = format_torrent(torrent)

    return value


def format_torrent(torrent):
    """Format a single torrent."""
    value = {}
    value["id"] = torrent["hash"]
    value["added_date"] = format_unix_timestamp(torrent["added_on"])
    value["percent_done"] = format_progress(torrent)
    value["status"] = torrent["state"]
    value["eta"] = seconds_to_hhmmss(torrent["eta"])
    value["ratio"] = "{:.2f}".format(float(torrent["ratio"]))

    return value
