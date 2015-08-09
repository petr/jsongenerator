# -*- coding: utf-8 -*-

from faker import Faker

__all__ = (
    'Parser',
    'Generator',
)


class Parser(object):
    definitions = None
    data_to_parse = None

    def __init__(self, data_to_parse):
        if 'definitions' in data_to_parse:
            self.definitions =  dict(data_to_parse['definitions'].items())
        else:
            self.definitions = {}

        self.data_to_parse = data_to_parse

    def get_entity_by_ref(self, ref):
        ref_last_name = ref.split('/').pop()
        assert ref_last_name in self.definitions, 'Theres no such ref as %s in definitions' % ref_last_name
        return self.definitions.get(ref_last_name)

    def begin(self):
        return self.parse_entity(self.data_to_parse)

    def parse_entity(self, entity):
        '''
            Detect entity type and parse in valid way
        '''
        if 'type' not in entity:
            raise Exception('Cannot find type key in %s' % entity)

        python_entity_type = type(entity['type'])
        if python_entity_type is str or python_entity_type is unicode:
            parse_func = 'parse_%s' % entity['type']
            assert hasattr(self, parse_func), '%s is not implemented' % parse_func
            return getattr(self, parse_func)(entity)
        elif python_entity_type is list:
            # If entity type is array we take the first one and make new entity type
            try:
                modified_type = entity['type'][0]
            except IndexError:
                raise
            entity['type'] = modified_type
            return self.parse_entity(entity)
        else:
            raise NotImplementedError('%s type is not implemented yet' % python_entity_type)

    def parse_object(self, entity, description=None):
        assert 'properties' in entity, 'Invalid entity object! Must has \'properties\' key.'

        parsed_entity = {}
        for key, child_entity in entity['properties'].iteritems():
            parsed_entity[key] = self.parse_entity(child_entity)

        return parsed_entity

    @staticmethod
    def parse_integer(entity, description=None):
        return ('integer', (),)

    @staticmethod
    def parse_string(entity, description=None):
        return ('string', (),)

    @staticmethod
    def parse_null(entity, description=None):
        return ('null', (),)

    @staticmethod
    def parse_number(entity, description=None):
        return ('nubmer', (),)

    def parse_array(self, entity, description=None):
        assert 'items' in entity, 'There is should and items in array type entity.'
        parsed_entity = []
        max_items = 100
        items = entity['items']
        items_length = len(items)
        assert items_length > 0, 'There is no any items in array entity!'

        if items_length == 1:
            item = items[0]
            assert '$ref' in item, '$ref key is not exists in array item of entity'
            item_entity = self.get_entity_by_ref(item['$ref'])
            for index in range(0, max_items):
                parsed_entity.append(self.parse_entity(item_entity))
        else:
            raise NotImplementedError('Parsing for several items is not implemented yet.')

        return parsed_entity


class Generator(object):
    def generate(self, data):
        result = {}
        assert type(data) is dict, 'Data to parse must be an dict!'
        fake = Faker()
        for item_key, item_data in data.items():
            generated_data = None
            if type(item_data) is tuple:
                generate_func_type, generate_func_args = item_data
                func_name = 'generate_%s' % generate_func_type
                assert hasattr(self, func_name), 'There is no generator %s' % func_name
                generated_data = getattr(self, func_name)(fake, *generate_func_args)
            elif type(item_data) is list:
                generated_data = []
                for list_item_data in item_data:
                    generated_data.append(self.generate(list_item_data))
            elif type(item_data) is dict:
                generated_data = self.generate(item_data)
            elif type(item_data) is type(None):
                generated_data = None
            else:
                raise Exception('Invalid type for data generation - %s' % type(item_data))
            result[item_key] = generated_data

        return result

    @staticmethod
    def generate_integer(fake, *args):
        return fake.random_int(min=1, max=2000)

    @staticmethod
    def generate_string(fake, *args):
        return fake.name()

    @staticmethod
    def generate_null(fake, *args):
        return None
