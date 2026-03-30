from datetime import date
from models import Session, Progress


class ProgressTracker:

    def mark_completed(self, user_id, resource_id):
        db = Session()

        row = db.query(Progress).filter(
            Progress.UserID == user_id,
            Progress.ResourceID == resource_id
        ).first()

        if row is None:
            row = Progress(
                UserID=user_id,
                ResourceID=resource_id,
                CompletionPercent=100,
                LastAccessed=date.today()
            )
            db.add(row)
        else:
            row.CompletionPercent = 100
            row.LastAccessed = date.today()

        db.commit()
        db.close()


