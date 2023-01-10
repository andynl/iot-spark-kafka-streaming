from sys import argv
import numpy as np

DEVICE_PROFILES = {
    "jkt": {'temp': (51.3, 17.7), 'humd': (77.4, 18.7), 'pres': (1019.9, 9.5) },
    "bdg": {'temp': (49.5, 19.3), 'humd': (33.0, 13.9), 'pres': (1012.0, 41.3) },
    "jog": {'temp': (63.9, 11.7), 'humd': (62.8, 21.8), 'pres': (1015.9, 11.3) },
}

profile_name = argv[1]
profile = DEVICE_PROFILES[profile_name]

print(np.random.normal(profile['temp'][0], profile['temp'][1]))