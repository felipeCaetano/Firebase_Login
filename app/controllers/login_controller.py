class LogInController:
    def __init__(self, auth_service, view):
        self.auth_service = auth_service
        self.view = view

    def log_user_in(self, email, password):
        if not email or not password:
            self.view.show_snack_bar("Email e senha são obrigatórios.")
            return
        try:
            self.auth_service.sign_in(email, password)
            self.view.clear_inputs()
            self.view.page.update()
            self.view.page.go("/view-reg")
        except ValueError as e:
            self.view.show_snack_bar(str(e))
