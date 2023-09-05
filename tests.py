import unittest

from peewee import SqliteDatabase

from contracts.funcs import create_contract, sign_contract
from exceptions import ProjectConditionError
from models import Contract, Project
from projects.funcs import (add_contract, create_project,
                            finish_project_contract)

MODELS = [Project, Contract]
test_db = SqliteDatabase(":memory:")


class TestStringMethods(unittest.TestCase):
    def setUp(self):
        # Bind model classes to test db. Since we have a complete list of
        # all models, we do not need to recursively bind dependencies.
        test_db.bind(MODELS, bind_refs=True, bind_backrefs=True)

        test_db.connect()
        test_db.create_tables(MODELS)

    def tearDown(self):
        # Not strictly necessary since SQLite in-memory databases only live
        # for the duration of the connection, and in the next step we close
        # the connection...but a good practice all the same.
        test_db.drop_tables(MODELS)
        test_db.close()

    def test_contract_default_draft_status(self):
        contract = create_contract("TestContract")
        self.assertEqual(contract.status, "draft")

    def test_contract_sign_date_assign(self):
        contract = create_contract("TestContract")
        self.assertEqual(contract.status, "draft")
        self.assertIs(contract.signed_at, None)
        sign_contract(contract)
        self.assertEqual(contract.status, "active")
        self.assertIsNot(contract.signed_at, None)

    def test_project_cant_add_same_contract(self):
        contract = create_contract("TestContract")
        sign_contract(contract)
        project = create_project("TestProject")
        add_contract(project, contract)
        self.assertRaises(ValueError, add_contract, project, contract)

    def test_project_add_only_active_contracts(self):
        contract = create_contract("TestContract")
        self.assertRaises(ProjectConditionError, create_project, "TestProject")
        sign_contract(contract)
        project = create_project("TestProject")
        contract2 = create_contract("TestContract2")
        self.assertRaises(ValueError, add_contract, project, contract2)
        add_contract(project, contract)

    def test_project_add_only_one_active_contract(self):
        contract = create_contract("TestContract")
        contract2 = create_contract("TestContract2")
        sign_contract(contract)
        sign_contract(contract2)
        project = create_project("TestProject")
        add_contract(project, contract)
        self.assertRaises(ValueError, add_contract, project, contract2)

    def test_project_finish_own_contract(self):
        contract = create_contract("TestContract")
        contract2 = create_contract("TestContract2")
        sign_contract(contract)
        sign_contract(contract2)
        project = create_project("TestProject")
        project2 = create_project("TestProject2")
        add_contract(project, contract)
        add_contract(project2, contract2)

        self.assertRaises(ValueError, finish_project_contract, project, contract2)

    def test_project_cant_add_foreign_contract(self):
        contract = create_contract("TestContract")
        contract2 = create_contract("TestContract2")
        sign_contract(contract)
        sign_contract(contract2)
        project = create_project("TestProject")
        project2 = create_project("TestProject2")
        add_contract(project, contract)
        self.assertRaises(ValueError, add_contract, project2, contract)
        

    def test_contract_project_field_while_adding(self):
        contract = create_contract("TestContract")        
        sign_contract(contract)
        self.assertIsNone(contract.project)
        project = create_project("TestProject")        
        add_contract(project, contract)
        self.assertIsNotNone(contract)

        


if __name__ == "__main__":
    unittest.main()
