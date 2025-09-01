import requests

def main(url: str):
    try:
        resp = requests.get(url, timeout=5)

        if resp.ok:
            return "ping great"
        else:
            return f"ping failed with status code: {resp.status_code}"

    except requests.ConnectionError:
        return "ping not available (connection error)"
    except requests.Timeout:
        return "ping not available (timeout)"
    except requests.RequestException as e:
        return f"ping not available (error: {e})"
