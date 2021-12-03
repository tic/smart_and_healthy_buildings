# Given air quality information, the code in this file generates our customized
# air quality subscores.

# Generate a score from 0 (worst) to 100 (best) that is representative of the
# given temperature.
def score_temperature(temperature):
    pass

# Generate a score from 0 (worst) to 100 (best) that is representative of the
# given relative humidity.
def score_humidity(humidity):
    pass

# Generate a score from 0 (worst) to 100 (best) that is representative of the
# given CO2 concentration.
def score_co2(co2_ppm):
    pass

# Generate a score from 0 (worst) to 100 (best) that is representative of the
# given VOC concentration.
def score_voc(voc_ppb):
    pass

# Generate a score from 0 (worst) to 100 (best) that is representative of the
# given PM2.5 concentration.
def score_pm25(pm25):
    pass

# Generate the subscores for the provided air quality components
def compute_subscores(temperature, humidity, co2_ppm, voc_ppb, pm25):
    # Initialize the two subscores
    environmental = 0
    occupational = 0

    # Compute the score for each of the 5 categories


    # Return the computed subscores
    return [environmental, occupational]
