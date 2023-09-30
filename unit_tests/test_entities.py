import unittest
from functions.entity import EntityManager
from Models.models import *
import json
from mongoengine import connect, disconnect


def runScript():
    connect('mongoenginetest', host='mongomock://localhost')
    # connect(alias='default', db='vaaas',
    #         username='vaaas',
    #         password='vaaas',
    #         host='10.0.1.220:27017',
    #         retryWrites=False)


runScript()
entity_instance = EntityManager()


class TestCases(unittest.TestCase):
    def test_mongodb(self):
        result = entity_instance.getAllEntities()
        self.assertEqual('GET_ALL_ENTITIES_SUCCESS', result['result'])

    def test_entity(self):
        result1 = entity_instance.storeEntity(payload)
        print(payload)
        self.assertEqual('CREATE_ENTITY_SUCCESS', result1['result'])

        entityid = result1['items'][0]['_id']['$oid']

        result3 = entity_instance.updateEntity(payload, entityid)
        self.assertEqual('UPDATE_ENTITY_SUCCESS', result3['result'])

        result4 = entity_instance.getEntity(entityid)
        self.assertEqual('GET_ENTITY_SUCCESS', result4['result'])

        result2 = entity_instance.deleteEntity(entityid)
        self.assertEqual('DELETE_ENTITY_SUCCESS', result2['result'])

    def test_search_entity(self):
        result1 = entity_instance.storeEntity(payload)
        print(payload)
        self.assertEqual('CREATE_ENTITY_SUCCESS', result1['result'])

        result2 = entity_instance.searchInstance({"ip": "10.0.255.223"})
        self.assertEqual('SEARCH_ENTITY_SUCCESS', result2['result'])


payload = {
    "name": "KeasdasdafPC2",
    "description": "Best PC EVAH",
    "assetType": "persosadasdsanalpc",
    "assessed": False,
    "status": True,
    "cvss": 5.5,
    "sensitivity": 1,
    "location": "pasiphaeeasdasde main room",
    "owner": "Kefalofffukos",
    "backupLocation": "nohhne",
    "dependedservices": "12",
    "value": 7,
    "active": True,
    "ip": "10.0.255.223",
    "mac": "FF:FF:FF:FF:F8:FF",
    "assetValue": 10
}
