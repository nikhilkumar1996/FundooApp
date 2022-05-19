from .api import UserLogin, Registration, ActivateEmail, ForgotPassword, ResetPassword, GetAllUsers

user_routes = [
    (UserLogin, '/login'),
    (Registration, '/register'),
    (ActivateEmail, '/activate_email'),
    (ForgotPassword, '/forgot_password'),
    (ResetPassword, '/reset_password'),
    (GetAllUsers, '/get_all_users')
]
