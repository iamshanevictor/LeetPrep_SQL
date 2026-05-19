from datetime import datetime, timezone

from app.extensions import db


class User(db.Model):
    """Future user model placeholder.

    Authentication is intentionally not implemented yet.
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self):
        return f"<User {self.username}>"
