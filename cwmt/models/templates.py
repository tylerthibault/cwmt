from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from cwmt import core

app = core.app
db = app.db
bcrypt = app.bcrypt

# -------------------------
# template-location Table
# -------------------------
template_cohort_locations = db.Table('template_locations',
    db.Model.metadata,
    db.Column('location_id', db.Integer, db.ForeignKey('locations.id'), primary_key=True),
    db.Column('template_id', db.Integer, db.ForeignKey('templates.id'), primary_key=True)
)

# -------------------------
# CohortTemplates Table
# -------------------------
class Template(db.Model):
    __tablename__ = 'templates'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    default_name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    default_max_capacity = db.Column(db.Integer, nullable=False)
    default_number_of_days = db.Column(db.Integer, nullable=False)

    # RELATIONSHIPS
    # locations = db.relationship('Location', secondary=TemplateCohortLocations, backref='cohort_templates')

    @classmethod
    def create(cls, data:dict):
        try:
            cohort_template = cls(
                default_name=data['default_name'],
                description=data.get('description', None),
                default_max_capacity=data.get('default_max_capacity', 10),
                default_number_of_days=data.get('default_number_of_days', 10),
            )
            db.session.add(cohort_template)
            db.session.commit()
            core.logger.log(f'Template {cohort_template.default_name} created.', with_flash=True, flash_category='success')
            return cohort_template
        except Exception as e:
            core.logger.log(f'Template creation failed. {str(e)}', with_flash=True, status='error')
            return None
    
    @classmethod
    def get_all(cls):
        return cls.query.all()
    
    @classmethod
    def get(cls, id):
        return cls.query.get(id)
    
    @classmethod
    def update(cls, data:dict):
        cohort_template = cls.get(data['id'])
        for key, value in data.items():
            setattr(cohort_template, key, value)
        db.session.commit()
        return cohort_template
    
    @classmethod
    def delete(cls, id):
        template = cls.get(id)
        db.session.delete(template)
        db.session.commit()
        return template