from data_manager.storage_config import DataManagerTinyDB


def get_data_manager(db_type="tinydb"):
    """
    Chooses database manager by matching it to the name given in Args.
    Args:
    name of the database to be used (string, defaults to 'tinydb')
    """
    if db_type == "tinydb":
        return DataManagerTinyDB()
    else:
        raise ValueError("Unsupported DB type")


data_manager = get_data_manager("tinydb")
