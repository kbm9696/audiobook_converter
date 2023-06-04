USER_POST = {
    "type": "object",
    "properties": {
        "user-id": {"type": "string"},
        "username": {"type": "string"},
        "password": {"type": "string"},
        "premium-user": {"type": "boolean"}
    },
    "required": ["user-id", "username", "password", "premium-user"]
}
USER_PATCH = {
    "type": "object",
    "properties": {
        "username": {"type": "string"},
        "password": {"type": "string"}
    },
    "additionalProperties": False
}
AUDIOBOOK_POST = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "premium": {"type": "string", "enum": ["True","False"]},
        "type_of_storage": {"type": "string", "enum": ["nft", "ipfs", "web3"]}
    },
    "required": ["title", "premium", "type_of_storage"],
    "additionalProperties": False
}
AUDIOBOOK_PATCH = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "premium": {"type": "boolean"},
    },
    "additionalProperties": False
}