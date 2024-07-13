import petl

from data_collections.models import Collection, SWPerson


class SWAPILoader:
    def __init__(self, table, ts, create=True, collection=None):
        self.table = table
        self.ts = ts
        self.create = create
        self.collection = collection

    def create_collection(self):
        file_name = f"collection_{self.ts}.csv"

        if self.create:
            petl.tocsv(self.table, file_name)
            self.collection = Collection()
            self.collection.file.name = file_name
            self.collection.save()

            self.create = False
        else:
            petl.appendcsv(self.table, file_name)

        return self.collection

    def create_persons(self, collection):
        sw_persons_to_create = []
        for row in list(petl.dicts(self.table)):
            row["collection"] = collection
            sw_person = SWPerson(**row)
            sw_persons_to_create.append(sw_person)

        SWPerson.objects.bulk_create(sw_persons_to_create)

    def load_data(self):
        self.create_collection()
        self.create_persons(self.collection)