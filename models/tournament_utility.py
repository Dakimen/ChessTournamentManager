

def recreate_tournament_input(tourn_dict):
    """
    Creates a dictionary with basic tournament information to allow for easier tournament instantiation.

    Arguments:
        A dictionary containing:
            'name' (string)
            'place' (string)
            'dates' (string in 'dd/mm/yyy - dd/mm/yyyy' format)
            'description' (string)
            'number_of_rounds' (string)
    """
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
