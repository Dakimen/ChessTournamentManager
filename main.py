from controllers.application_controller import ApplicationController


def main():
    """Entry point of the application, instantiates ApplicationController and executes it's .run()"""
    application_controller = ApplicationController()
    application_controller.run()


main()
