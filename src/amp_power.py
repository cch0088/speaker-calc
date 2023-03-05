from create_db import session
from sound_system import Amplifier

import click
from pick import pick
import math

def amplifier_power_required():

    title = ('Amplifier Power Required \n \n')

    description = ('This calculator provides the required electrical power \n'
                   '(power output from the amplifier) to produce a desired \n'
                    'Sound Pressure Level (SPL) at a given distance, along \n'
                    'with an amount of headroom to keep the amplifier(s) \n'
                    'out of clip. \n')
    
    heading = title + description + ('\n Select Units')

    options = ['Meters', 'Feet']
    units, index = pick(options, heading, "->")

    print('\n ' + title)

    if index == 0:
        distance_from_source = click.prompt(' Listener distance from speaker (in meters)', default=3.7, type=click.FloatRange(0.01))
        reference_distance = 1
    else:
        distance_from_source = click.prompt(' Listener distance from speaker (in feet)', default=12.0, type=click.FloatRange(0.01))
        reference_distance = 3.281

    desired_level = click.prompt(' Desired dB SPL at this distance', default=80, type=click.IntRange(1))
    headroom = click.prompt(' Amplifier headroom in dB', default=3, type=click.IntRange(0))
    sensitivity = click.prompt(' Speaker sensitivity rating in dB', default=85, type=click.IntRange(1))

    power_required = 10 ** (((desired_level + headroom - sensitivity) + 20 * math.log((distance_from_source / reference_distance), 10)) / 10)

    if power_required < 1:
        power_required = round(power_required, 4)
    else:
        power_required = int(power_required)

    click.clear()

    options = ['Yes', 'No']
    description = ('Power required: ' + str(power_required) + ' watts per channel\n\n'
                   'Assuming the speaker and amplifier output have the same \n'
                   'impedance, the amplifier will need to have ' + str(power_required) + ' watts \n'
                   'of power to drive the speaker at ' + str(desired_level) + 'dB of SPL at ' + str(distance_from_source) + ' ' + units.lower() + 
                   '.\nThe speaker must also be able to handle this much power.\n')
    heading = title + description + ('\n Store this result?')

    store, index = pick(options, heading, "->")

    if index == 0:
        new_amp = Amplifier(name="Power Amplifier", power=power_required)
        session.add(new_amp)
        session.commit()

    return power_required