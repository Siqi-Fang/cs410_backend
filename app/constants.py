from enum import Enum

TRUTHSOCIAL_BASE = 'https://truthsocial.com/login'


class Platform(Enum):
    TRUTHSOCIAL = 1
    FACEBOOK = 2
    TWITTER = 3

    @staticmethod
    def from_str(term):
        if term.lower() == 'truth-social':
            return Platform.TRUTHSOCIAL
        elif term.lower() == 'facebook':
            return Platform.FACEBOOK
        elif term.lower() == 'twitter':
            return Platform.TWITTER
        else:
            raise NotImplementedError

FILEDS = ['POST_DATE',
          'AUTHOR',
          'CONTENT',
          'PLATFORM',
          'URL',
          'KEYWORD']

#KEYWORDS = ["Illegal alien Latino", "Illegal immigrant Latino", "Latino Wetback", "Latino Spic", "Latino Undocumented", "Latino Beaner", "Latino Rapists", "Latino Drug dealers", "Latino Invasion"]