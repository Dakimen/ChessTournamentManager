from storage_config import DataManagerTinyDB


def get_data_manager(db_type="tinydb"):
    if db_type == "tinydb":
        return DataManagerTinyDB()
    else:
        raise ValueError("Unsupported DB type")


data_manager = get_data_manager("tinydb")
