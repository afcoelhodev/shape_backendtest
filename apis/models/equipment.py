from apis.models.model import db


class equipment(db.Model):
    __tablename__ = 'equipments'

    id = db.Column(db.BigInteger, primary_key=True)
    vessel_id = db.Column(db.BigInteger, db.ForeignKey('vessels.code'))
    name = db.Column(db.String(256))
    code = db.Column(db.String(8), unique=True)
    location = db.Column(db.String(256))
    active = db.Column(db.Boolean)

    def __init__(self, vessel_id, name, code, location, active=True):
        self.vessel_id = vessel_id
        self.name = name
        self.code = code
        self.location = location
        self.active = True


    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()


    def formatted(self):
        return {
            'id': self.id,
            'vessel_id': self.vessel_id,
            'name': self.name,
            'code': self.code,
            'location': self.location,
            'active': self.active
        }