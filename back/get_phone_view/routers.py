class OsaExtraRouter:
    apps = {'api'}
    schema_name = 'osa_extra'

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.apps:
            return self.schema_name
        else:
            return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.apps:
            return self.schema_name
        else:
            return None

    def allow_relation (self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.apps:
            return db == self.schema_name
        return None


class DefaultRouter:
    default_db = 'default'

    def db_for_read(self, model, **hints):
        return self.default_db

    def db_for_write(self, model, **hints):
        return self.default_db

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return db == self.default_db
