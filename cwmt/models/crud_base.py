from cwmt import core

class CRUDModel:
    @classmethod
    def create(cls, data: dict):
        attrs = {key: value for key, value in data.items() if hasattr(cls, key)}
        instance = cls(**attrs)
        core.app.db.session.add(instance)
        core.app.db.session.commit()
        core.logger.log(f'{cls.__name__} created.', with_flash=True, flash_category='success')
        return instance

    @classmethod
    def get(cls, id):
        return cls.query.get(id)

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def update(cls, id, data: dict):
        instance = cls.get(id)
        for key, value in data.items():
            setattr(instance, key, value)
        core.app.db.session.commit()
        core.logger.log(f'{cls.__name__} updated.', with_flash=True, flash_category='success')
        return instance

    @classmethod
    def delete(cls, id):
        instance = cls.get(id)
        core.app.db.session.delete(instance)
        core.app.db.session.commit()
        core.logger.log(f'{cls.__name__} deleted.', with_flash=True, flash_category='success')
        return instance
