import unittest
from models import Project, Contract
from contracts.funcs import sign_contract, create_contract
from peewee import SqliteDatabase

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
        project = create_contract
        add_contract_to_project(project, contract)
        assertRaises(ValueError, add_contract_to_project, [project,contract1] ) 

    def test_project_add_only_active_contracts(self):
        pass

    def test_project_add_only_only_one_active_contract(self):
        pass

    def test_project_finish_own_contract(self):
        pass

    def test_project_cant_add_foreign_contract(self):
        pass

    def test_contract_project_field_while_adding(self):
        pass


if __name__ == "__main__":
    unittest.main()
