from datetime import datetime, timezone

from app.extensions import db


class Attempt(db.Model):
    """Future attempt tracking model placeholder."""

    id = db.Column(db.Integer, primary_key=True)
    problem_id = db.Column(db.String(120), nullable=False)
    submitted_query = db.Column(db.Text, nullable=False)
    is_correct = db.Column(db.Boolean, nullable=True)
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self):
        return f"<Attempt problem_id={self.problem_id}>"
