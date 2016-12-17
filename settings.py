__author__ = 'marcus'

import yaml
import aiml

def init(bot_profile, bot):
    f = open(bot_profile)
    # use safe_load instead load
    props = yaml.safe_load(f)
    keys = props['bot'].keys()
    for key in keys:
        bot.setBotPredicate(key, props['bot'][key])

    f.close()







