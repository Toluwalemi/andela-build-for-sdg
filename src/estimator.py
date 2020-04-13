def estimator(data):
    avg_income = data['region']['avgDailyIncomeInUSD']
    avg_income_population = data['region']['avgDailyIncomePopulation']
    period_type = data['periodType']
    time_to_elapse = data['timeToElapse']
    reported_cases = data['reportedCases']
    hospital_beds = data['totalHospitalBeds']

    impact_currently_infected = reported_cases * 10
    severe_impact_currently_infected = reported_cases * 50

    # function to calculate number of days
    def number_of_days(period_type, time_to_elapse):
        if period_type == 'days':
            days = time_to_elapse
        elif period_type == 'weeks':
            days = time_to_elapse * 7
        elif period_type == 'months':
            days = time_to_elapse * 30
        return days

    return data
