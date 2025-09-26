"""
This file is deprecated in favor of the modular `app.py` + routes/ structure.

Previously, `sandbox_server.py` implemented all endpoints in a monolithic Flask app.
Now, use `app.py` as the canonical entrypoint for the sandbox server.

Keeping this file only for reference / backward compatibility.
"""

if __name__ == "__main__":
    import warnings
    warnings.warn(
        "sandbox_server.py is deprecated. Use app.py instead.",
        DeprecationWarning,
    )
    from app import app
    app.run(host="0.0.0.0", port=8080)
