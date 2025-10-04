from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from datetime import datetime
import re
import logging

from ..models import db, Waitlist

waitlist_bp = Blueprint('waitlist', __name__, url_prefix='/api/waitlist')

# Configure logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

EMAIL_REGEX = re.compile(r'^[^@\s]+@[^@\s]+\.[^@\s]+$')

@waitlist_bp.route('', methods=['POST'])
def join_waitlist():
    try:
        data = request.get_json() or {}
        email = data.get('email', '').strip().lower()
        source = data.get('source', 'direct')

        # Validate email
        if not EMAIL_REGEX.match(email):
            return jsonify({'message': 'Invalid email address.'}), 400

        # Check duplicate
        existing = Waitlist.query.filter_by(email=email).first()
        if existing:
            return jsonify({'message': 'You’re already on the list!'}), 409

        # Add new entry
        entry = Waitlist(email=email, source=source, created_at=datetime.utcnow())
        db.session.add(entry)
        db.session.commit()

        logger.info(f"✅ New waitlist signup: {email} from {source}")
        return jsonify({'message': 'Welcome to the waitlist!'}), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'You’re already on the list!'}), 409

    except Exception as e:
        logger.error(f"❌ Error processing waitlist signup: {e}")
        return jsonify({'message': 'Server error. Please try again later.'}), 500
