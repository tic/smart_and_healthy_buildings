# Given air quality information, the code in this file generates our customized
# air quality subscores. All formulas were computed using cubic or exponential
# regression with the AWAIR score explanation document serving as the ground
# truth for each component score.

# Generate a score from 0 (worst) to 100 (best) that is representative of the
# given temperature.
def score_temperature(temperature_c):
    # round temperature to 2 digits
    temperature_c = round(temperature_c, 2)

    if temperature_c < 21.5:
        if temperature_c < 1.36:
            return 0
        a = 0.0324
        b = -1.2626
        c = 17.8644
        d = -22.007
        rating = a*(temperature_c ** 3) + b*(temperature_c ** 2) + c*temperature_c + d
        if rating > 100:
            return 100
        return round(rating, 2)

    if temperature_c > 21.5:
        if temperature_c > 40.87:
            return 0
        a = -0.0315
        b = 2.8074
        c = -85.3775
        d = 950.5292
        rating = a*(temperature_c ** 3) + b*(temperature_c ** 2) + c*temperature_c + d
        if rating > 100:
            return 100
        return round(rating, 2)

    return 100

# Generate a score from 0 (worst) to 100 (best) that is representative of the
# given relative humidity.
def score_humidity(humidity):
    if humidity > 45.2:
        a = -0.00184
        b = 0.3792
        c = -26.3494
        d = 683.7282
        rating = a*(humidity ** 3) + b*(humidity ** 2) + c*humidity + d
        return round(rating, 2)

    if humidity < 44.8:
        if humidity < 0.1:
            return 0
        a = 0.00356
        b = -0.2737
        c = 7.3135
        d = -0.454
        rating = a*(humidity ** 3) + b*(humidity ** 2) + c*humidity + d
        return round(rating, 2)

    return 100

# Generate a score from 0 (worst) to 100 (best) that is representative of the
# given CO2 concentration.
def score_co2(co2_ppm):
    adj_co2 = co2_ppm / 100
    if adj_co2 > 50:
        return 0
    a = -0.0022
    b = 0.1505
    c = -3.9903
    d = 99.9546
    rating = a*(adj_co2 ** 3) + b*(adj_co2 ** 2) + c*adj_co2 + d
    return round(rating, 2)

# Generate a score from 0 (worst) to 100 (best) that is representative of the
# given VOC concentration.
def score_voc(voc_ppb):
    if voc_ppb > 60000:
        return 0
    a = 100
    b = 0.99988
    rating = a*(b ** voc_ppb)
    return round(rating, 2)

# Generate a score from 0 (worst) to 100 (best) that is representative of the
# given PM2.5 concentration.
def score_pm25(pm25):
    a = 100
    b = 0.9925253
    rating = a*(b ** pm25)
    return round(rating, 2)

# Generate the subscores for the provided air quality components
def compute_subscores(temperature_c, humidity, co2_ppm, voc_ppb, pm25):
    # Compute the score for each of the 5 categories
    temp_subscore = score_temperature(temperature_c)
    humidity_subscore = score_humidity(humidity)
    co2_subscore = score_co2(co2_ppm)
    voc_subscore = score_voc(voc_ppb)
    pm25_subscore = score_pm25(pm25)

    component_subscores = [
        temp_subscore,
        humidity_subscore,
        co2_subscore,
        voc_subscore,
        pm25_subscore
    ]

    # Compute the subscores
    environmental_subscore_breakdown = [0.25, 0.30, 0.05, 0.10, 0.30]
    environmental = sum([environmental_subscore_breakdown[i] * component_subscores[i] for i in range(5)])

    occupational_subscore_breakdown = [0.05, 0.15, 0.325, 0.325, 0.15]
    occupational = sum([occupational_subscore_breakdown[i] * component_subscores[i] for i in range(5)])

    overall = sum([0.2 * component_subscores[i] for i in range(5)])
    # Return the computed subscores
    return [environmental, occupational, overall]

##########################
# testing area! :)
if __name__ == '__main__':
    print(score_temperature(24))
    print(score_humidity(40))
    print(score_co2(2980))
    print(score_voc(1975))
    print(score_pm25(5))
    print(compute_subscores(24, 40, 2980, 1976, 5))
