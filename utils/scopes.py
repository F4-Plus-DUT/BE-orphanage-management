def read_scopes(file_path: str) -> dict:
    """
    Read file.json and return a dict of data
    """
    import json

    with open(file_path) as json_file:
        data: dict = json.load(json_file)
        return data
