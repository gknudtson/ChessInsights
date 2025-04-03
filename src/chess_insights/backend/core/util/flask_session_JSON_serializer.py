from flask.json.tag import TaggedJSONSerializer


class FlaskSessionJSONSerializer:
    """
    This class is used to interface TaggedJSONSerializer with flask since flask expects encode and
     decode as methods. This is a more secure, human-readable alternative to flasks, default pickle.
    """

    def __init__(self):
        self.serializer = TaggedJSONSerializer()

    def encode(self, value):
        return self.serializer.dumps(value)

    def decode(self, value):
        return self.serializer.loads(value)
