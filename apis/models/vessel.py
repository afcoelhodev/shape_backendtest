from apis.models.model import db


class vessel(db.Model):
    __tablename__ = 'vessels'

    id = db.Column(db.BigInteger, primary_key=True)
    code = db.Column(db.String(8), unique=True)

    def __init__(self, code):
        self.code = code

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def formatted(self):
        return {
            'id': self.id,
            'code': self.code
        }