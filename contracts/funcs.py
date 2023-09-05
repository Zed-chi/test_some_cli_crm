from datetime import datetime

from color_print import ColorPrint as cprint
from models import Contract
from exceptions import CancelException
from peewee import IntegrityError


def list_contracts(status=None):
    if status is None:
        contracts = Contract.select()
    else:
        contracts = Contract.select().where(Contract.status == status)
    if not contracts:
        cprint.print_fail("No contracts")
        return
    cprint.print_pass("--- Data ---")
    cprint.print_info(f"id\tstatus\ttitle")
    for i in contracts:
        cprint.print_info(f"{i.id}\t{i.status}\t{i.title}")


def create_contract(name=None):
    if not name:
        while True:
            name = input("Type contract name: ")
            if name:
                break
        
    try:
        contract = Contract.create(
            title=name, created_at=datetime.now(), status="draft"
        )
        return contract
        cprint.print_pass(f"Contract {contract.id} created")
    except IntegrityError:
        cprint.print_fail("Name in use")
    except Exception as e:
        cprint.print_fail(e)


def sign_contract(contract=None):
    list_contracts(status="draft")
    if not contract:
        try:
            contract = get_contract_from_cli_id()
        except CancelException:
            return
    contract.status = "active"
    contract.signed_at = datetime.now()
    contract.save()
    cprint.print_pass("Contract signed")


def get_contract_from_cli_id():
    while True:
        _id = input("Type contract id to sign (or 0 to go back): ")
        if _id == "0":
            raise CancelException()
        if not _id:
            cprint.print_fail("Empty data")
            continue
        try:
            contract = Contract.get(id=_id)
            return contract
        except Exception as e:
            cprint.print_fail(e)

def finish_contract():
    while True:
        _id = input("Type contract id to complete (or 0 to go back): ")
        if _id == "0":
            return
        if not _id:
            cprint.print_fail("Empty data")
            continue
        try:
            contract = Contract.get(id=_id)
            contract.status = "finish"
            contract.save()
            cprint.print_pass("Contract finished")
            break
        except Exception as e:
            cprint.print_fail(e.__str__)
        except:
            cprint.print_fail("fok")
