import requests


def get_server_url(server_ip: str, server_port: str):
    return f"http://{server_ip}:{server_port}"


def get_headers(api_key: str):
    return {
        "X-API-Key": api_key,
    }


def get_model(
    server_ip: str,
    server_port: str,
    api_key: str,
):
    server_url = get_server_url(
        server_ip,
        server_port,
    )

    response = requests.get(
        f"{server_url}/models",
        headers=get_headers(api_key),
        timeout=10,
    )

    response.raise_for_status()

    return response.json()


def send_message(
    message: str,
    server_ip: str,
    server_port: str,
    api_key: str,
):
    server_url = get_server_url(
        server_ip,
        server_port,
    )

    response = requests.post(
        f"{server_url}/chat",
        headers=get_headers(api_key),
        json={
            "message": message,
        },
        timeout=120,
    )

    response.raise_for_status()

    return response.json()