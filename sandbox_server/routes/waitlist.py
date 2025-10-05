from flask import Blueprint, request, jsonify
from datetime import datetime
from ..models import db, Waitlist

bp = Blueprint('waitlist', __name__, url_prefix='/waitlist')

@bp.route('', methods=['POST'])
def join_waitlist():
    data = request.get_json()
    email = data.get('email')
    if not email:
        return jsonify({'error': 'Email required'}), 400

    existing = Waitlist.query.filter_by(email=email).first()
    if existing:
        return jsonify({'message': "You're already on the list!"}), 409

    entry = Waitlist(email=email, created_at=datetime.utcnow())
    db.session.add(entry)
    db.session.commit()

    return jsonify({'message': 'Welcome to the waitlist!'}), 201