# Given air quality data, this file generates a list of recommendations as to
# how the air quality can be improved, if it needs to be.

from awair_scores import environmental_subscore_breakdown, occupational_subscore_breakdown

# Structure containing the various recommended actuations for each component of
# air quality. For temperature and humidity, the recommendations change based on
# whether the measured value is too high or too low (compared to an ideal value)
actuations = {
    'temperature': {
        'high': [
            'Increase air conditioing',
            'Decrease heating',
            'Open windows, if cooler outside',
            'Reduce outside lighting',
            'Switch to CFL or LED bulbs',
            'Shut off computers and screens not in use',
            'Limit hot meals'
        ],
        'low': [
            'Decrease air conditioning',
            'Increase heating',
            'Open windows, if warmer outside'
        ]
    },
    'humidity': {
        'low': [
            'Run a humidifier',
            'Open windows, if more humid outside',
            'Air dry laundry',
            'Add plants to the space'
        ],
        'high': [
            'Run a dehumidifier',
            'Open windows, if less humid outside',
            'Turn on exhaust fans'
        ]
    },
    'co2': [
        'Increase HVAC cycles',
        'Open windows',
        'Increase airflow in kitchens',
        'Limit open flames',
        'Use an air purifier',
        'Limit exercise and other exertive activities'
    ],
    'voc': [
        'Reduce perfume usage',
        'Reduce air freshener usage',
        'Reduce cosmetic usage',
        'Reduce nail polish usage',
        'Reduce deodorant usage',
        'Remove carpets not made from wool, cotton, or jute'
    ],
    'pm25': [
        'Use an air cleaner',
        'Avoid strenuous activities',
        'Open windows, if cleaner outside',
        'Wet mop or vacuum the area',
        'Decrease smoking or vaping in the space',
        'Avoid anything that burns',
        'Remove pets that create dander'
    ]
}

# Provide the component subscores, measured temperature, and measured humidity,
# and this function will return a list of recommended actuations for the
# environmental and occupational subscores. It will find the component of air
# quality that is most affecting each subscore and get recommendations on how to
# change that component's value.
# @returns dict with 'environmental' and 'occupational' keys. Each key maps to
# a dict with 'field' and 'actuations' keys; the former is the name of the air
# quality component that was identified as the most significant detractor from
# the score, while the latter is a list of things occupants can do to improve
# that air quality component.
def get_actuations(component_subscores, temperature_c, humidity):
    # Compute how much was lost in each component category
    environ_lost = list(round((100 - component_subscores[i]) * environmental_subscore_breakdown[i], 2) for i in range(5))
    occupat_lost = list(round((100 - component_subscores[i]) * occupational_subscore_breakdown[i]) for i in range(5))

    # Find the component that most significantly detracts from each subscore
    def get_critical_actuation_field(score_list):
        field_map = {
            0: 'temperature',
            1: 'humidity',
            2: 'co2',
            3: 'voc',
            4: 'pm25'
        }
        most_significant = 0
        saved_index = 0
        for index, score in enumerate(score_list):
            if score > most_significant:
                most_significant = score
                saved_index = index
        return field_map[saved_index]

    environ_actuation_field = get_critical_actuation_field(environ_lost)
    occupat_actuation_field = get_critical_actuation_field(occupat_lost)

    # Recommend actuations for each subscore
    def recommend_actuations(field):
        if field == 'temperature':
            return actuations['temperature']['high' if temperature_c > 21.5 else 'low']
        elif field == 'humidity':
            return actuations['humidity']['high' if humidity > 45 else 'low']
        return actuations[field]

    return {
        'environmental': {
            'field': environ_actuation_field,
            'actuations': recommend_actuations(environ_actuation_field)
        },
        'occupational': {
            'field': occupat_actuation_field,
            'actuations': recommend_actuations(occupat_actuation_field)
        }
    }

# testing area :)
if __name__ == '__main__':
    from awair_scores import compute_component_subscores
    css = compute_component_subscores(24, 40, 2980, 1976, 5)

    recommendations = get_actuations(css, 24, 40)
    print(recommendations)
