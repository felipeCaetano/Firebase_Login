from gotrue.errors import AuthApiError

class AuthService:
    def __init__(self, supabase):
        self.supabase = supabase

    def sign_in(self, email, password):
        try:
            data = self.supabase.auth.sign_in_with_password({
                "email": email,
                "password": password,
            })
            return data
        except AuthApiError as e:
            if e.args[0] == "Invalid login credentials":
                raise ValueError("Invalid login credentials")
            else:
                raise
