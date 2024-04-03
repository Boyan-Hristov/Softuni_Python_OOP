from project.band_members.musician import Musician


class Singer(Musician):
    # check if it works without calling the super().__init__

    @property
    def available_skills(self):
        return [
            "sing high pitch notes",
            "sing low pitch notes"
        ]
