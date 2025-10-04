def register_routes(app):
    from .waitlist import bp as waitlist_bp
    app.register_blueprint(waitlist_bp)