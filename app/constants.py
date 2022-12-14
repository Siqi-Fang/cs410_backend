from enum import Enum

TRUTHSOCIAL_BASE = 'https://truthsocial.com/login'
FB_RECENT_TOGGLE = '&filters=eyJyZWNlbnRfcG9zdHM6MCI6IntcIm5hbWVcIjpcInJlY2VudF9wb3N0c1wiLFwiYXJnc1wiOlwiXCJ9In0%3D'

class Platform(Enum):
    TRUTHSOCIAL = 1
    FACEBOOK = 2
    TWITTER = 3
    GATEWAYPUNDIT = 4

    @staticmethod
    def from_str(term):
        if term.lower() == 'truth-social':
            return Platform.TRUTHSOCIAL
        elif term.lower() == 'facebook':
            return Platform.FACEBOOK
        elif term.lower() == 'twitter':
            return Platform.TWITTER
        elif term.lower() == 'gateway-pundit':
            return Platform.GATEWAYPUNDIT
        else:
            raise NotImplementedError

FIELDS = ['POST_DATE',
          'AUTHOR',
          'CONTENT',
          'PLATFORM',
          'URL',
          'KEYWORD',
          'SENTIMENT',
          'SCORE',]

KEYWORDS = ["Illegal alien Latino", "Illegal immigrant Latino", "Latino Wetback", "Latino Spic", \
            "Latino Undocumented", "Latino Beaner", "Latino Rapists", "Latino Drug dealers", "Latino Invasion"]