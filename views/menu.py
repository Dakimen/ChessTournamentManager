class Menu:
    def __init__(self, menu_name, options):
        self.options = []
        self.option_keys = []
        for key in options:
            self.options.append(options[key]["text"])
            self.option_keys.append(options[key]["key"])
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
