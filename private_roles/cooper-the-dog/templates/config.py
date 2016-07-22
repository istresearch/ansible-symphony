# Flask-Security config
SECURITY_URL_PREFIX = "/cooper/admin"
SECURITY_PASSWORD_HASH = "{{ cooper_flask_pw_hash }}"
SECURITY_PASSWORD_SALT = "{{ cooper_flask_pw_salt }}"

# Flask-Security URLs, overridden because they don't put a / at the end
SECURITY_LOGIN_URL = "/login/"
SECURITY_LOGOUT_URL = "/logout/"
SECURITY_REGISTER_URL = "/register/"

SECURITY_POST_LOGIN_VIEW = "cooper/home"
SECURITY_POST_LOGOUT_VIEW = "cooper/home"
SECURITY_POST_REGISTER_VIEW = "cooper/admin/login/"

# Flask-Security features
SECURITY_REGISTERABLE = True
SECURITY_SEND_REGISTER_EMAIL = False
