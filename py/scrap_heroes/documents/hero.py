import mongoengine


class Hero(mongoengine.Document):
    """
    Class storing all information about heroes
    """

    meta = {
        "db_alias": "heroes",
    }

    data = mongoengine.DictField()
    french_name = mongoengine.StringField()
    official_slug = mongoengine.StringField()  # Contains the official name of the Hero

    @classmethod
    def find_hero_from_french_name(cls, french_name):
        return cls.objects(french_name__iexact=french_name).first()
