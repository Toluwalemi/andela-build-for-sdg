def estimator(data):
    avg_income = data['region']['avgDailyIncomeInUSD']
    avg_income_population = data['region']['avgDailyIncomePopulation']
    period_type = data['periodType']
    time_to_elapse = data['timeToElapse']
    reported_cases = data['reportedCases']
    total_hospital_beds = data['totalHospitalBeds']

    impact_currently_infected = reported_cases * 10
    severe_impact_currently_infected = reported_cases * 50
    available_beds = 0.35 * total_hospital_beds

    # function to calculate number of days
    def number_of_days(days, calc_period_type=period_type, calc_time_to_elapse=time_to_elapse):
        if calc_period_type == 'days':
            days = time_to_elapse
        elif calc_period_type == 'weeks':
            days = time_to_elapse * 7
        elif calc_period_type == 'months':
            days = calc_time_to_elapse * 30
        return days

    def severe_positive_cases(case):
        days = number_of_days(calc_period_type=period_type, calc_time_to_elapse=time_to_elapse) // 3
        return case * (2 ** days)

    def severe_cases_req_time(case):
        return 0.15 * severe_positive_cases(case)

    def hospital_beds_req_time(case):
        return int(available_beds - severe_cases_req_time(case))

    # this functions estimates how much money the economy is likely to lose
    def money_to_lose(case):
        func = severe_positive_cases(case)
        days = number_of_days(period_type, time_to_elapse)
        return int((func * avg_income_population * avg_income) / days)

    result = {
        "data": data,
        "impact": {
            "currentlyInfected": impact_currently_infected,
            "infectionsByRequestedTime": severe_positive_cases(impact_currently_infected),
            "severeCasesByRequestedTime": int(severe_cases_req_time(impact_currently_infected)),
            "hospitalBedsByRequestedTime": hospital_beds_req_time(impact_currently_infected),
            "casesForICUByRequestedTime": int(0.05 * severe_positive_cases(impact_currently_infected)),
            "casesForVentilatorsByRequestedTime": int(0.02 * severe_positive_cases(impact_currently_infected)),
            "dollarsInFlight": money_to_lose(impact_currently_infected)
        },
        "severeImpact": {
            "currentlyInfected": severe_impact_currently_infected,
            "infectionsByRequestedTime": severe_positive_cases(severe_impact_currently_infected),
            "severeCasesByRequestedTime": int(severe_cases_req_time(severe_impact_currently_infected)),
            "hospitalBedsByRequestedTime": hospital_beds_req_time(severe_impact_currently_infected),
            "casesForICUByRequestedTime": int(0.05 * severe_positive_cases(severe_impact_currently_infected)),
            "casesForVentilatorsByRequestedTime": int(0.02 * severe_positive_cases(severe_impact_currently_infected)),
            "dollarsInFlight": money_to_lose(severe_impact_currently_infected)
        }
    }

    return result
