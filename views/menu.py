class Menu:
    """
    A Menu class representing a menu within the application.
    Allows for easier creation and display of various menus.

    Arguments:
        menu name (string)
        option to display (dict), containing:
            'text' (string to display as the name of the option)
            'key' (string acting as expected value within a console menu)
    """
    def __init__(self, menu_name, options):
        self.options = []
        self.option_keys = []
        for key in options:
            self.options.append(options[key]["text"])
            self.option_keys.append(options[key]["key"])
            if options[key]["key"] == "Q":
                self.option_keys.append("q")
        self.menu_name = menu_name

    def display_menu(self):
        print((
           f"{self.menu_name}"
           ))
        ticker = 0
        for option in self.options:
            print(f"{self.option_keys[ticker]}: {option}")
            ticker = ticker + 1
        user_choice = input(">>> ")
        if user_choice not in self.option_keys:
            while user_choice not in self.option_keys:
                print("Please insert a valid option")
                user_choice = input(">>> ")
        return user_choice
