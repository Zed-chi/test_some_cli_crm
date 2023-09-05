from datetime import datetime

from peewee import IntegrityError
from terminaltables import DoubleTable

from color_print import ColorPrint as cprint
from contracts.funcs import get_contract_from_cli_id, list_contracts
from exceptions import CancelException, ProjectConditionError
from models import Contract, Project


def is_no_projects():
    projects = Project.select()
    return len(projects) == 0


def get_project_name():
    while True:
        name = input("Type project name(or 0 to cancel): ")
        if name == "0":
            raise CancelException()
        if not name:
            cprint.print_fail("!Empty data")
            continue
        return name


def create_project(name=None):
    active_contracts = Contract.select().where(Contract.status == "active")
    if not active_contracts:
        raise ProjectConditionError("Add at leats one active contract")
    if not name:
        name = get_project_name()
    try:
        project = Project.create(title=name, created_at=datetime.now())
        cprint.print_info(f"Project {project.id} created")
        return project
    except IntegrityError:
        cprint.print_fail("Name in use")


def choose_project():
    if is_no_projects():
        raise ValueError("!No projects created")
    list_projects()
    while True:
        _id = input("Type project id: ")
        if not _id:
            raise ValueError("!Empty data")
        try:
            project = Project.get(id=_id)
            return project
        except Exception:
            raise ValueError("Project Not found")


def add_contract(project=None, contract=None):
    contracts = Contract.select()
    if not contracts:
        raise ValueError("No available contracts...")

    if not project:
        project = choose_project()

    if project.active_contracts:
        raise ValueError("!Project has active contract")

    if not contract:
        list_contracts()
        contract = get_contract_from_cli_id()
    if contract.project:
        raise ValueError("This contract already in use")
    elif contract.status != "active":
        raise ValueError("This contract is not an active")
    contract.project = project
    contract.save()
    cprint.print_pass("Contract added")


def list_active_contracts(project):
    cprint.print_warn("[Project Active contracts]")
    for i in project.active_contracts:
        cprint.print_info(f"{i.id} - {i.title}")


def finish_project_contract(project=None, contract=None):
    if not project:
        project = choose_project()

    if not project.active_contracts:
        raise ValueError("Project has no active contracts")

    if not contract:
        list_active_contracts(project)
        contract = get_contract_from_cli_id()
    if contract.project != project:
        raise ValueError("Different project contract")

    if contract.status != "active":
        raise ValueError("Not an active project")
    contract.status = "finished"
    contract.save()
    cprint.print_pass("Contract finished")


def list_projects():
    projects = Project.select()
    if not len(projects):
        cprint.print_fail("No projects created")
    else:
        data = [
            [i.id, i.title, (len(i.active_contracts)>0), len(i.contracts)]
            for i in projects
        ]
        data.insert(0, ["id", "title", "has act contract", "all contracts"])
        table = DoubleTable(data)
        table.title = "Projects List"
        print(table.table)
