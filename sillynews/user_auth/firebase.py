import firebase_admin
from firebase_admin import auth, credentials

app = None


def initialize():
    global app
    if not app:
        cred = credentials.Certificate('firebase_adminsdk.json')
        try:
            app = firebase_admin.get_app(name="AuthApp")
        except ValueError:
            app = firebase_admin.initialize_app(credential=cred, name="AuthApp")
        return app


def verify_token(token):
    global app
    if not app:
        initialize()
    try:
        user = firebase_admin.auth.verify_id_token(token, app=app)
    except:
        return None
    return user