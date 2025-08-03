

def recreate_tournament_input(tourn_dict):
    dates = tourn_dict["dates"]
    dates = dates.split(" - ")
    beginning_date = dates[0]
    end_date = dates[1]
    tourn_data = {
        "tournament_name": tourn_dict["name"],
        "tournament_place": tourn_dict["place"],
        "tournament_beginning_date": beginning_date,
        "tournament_end_date": end_date,
        "tournament_description": tourn_dict["description"],
        "number_of_rounds": tourn_dict["number_of_rounds"]
    }
    return tourn_data
