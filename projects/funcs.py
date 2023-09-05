from models import Project, Contract
from datetime import datetime
from contracts.funcs import list_contracts
from color_print import ColorPrint as cprint
from peewee import PeeweeException


def is_no_projects():
    projects = Project.select()
    return len(projects) == 0


def create_project():
    active_contracts = Contract.select().where(Contract.status == "active")
    if not active_contracts:
        cprint.print_fail("!Add active contracts")
        return
    while True:
        name = input("Type project name(or 0 to cancel): ")
        if name == "0":
            return
        if not name:
            cprint.print_fail("!Empty data")
            continue
        try:
            project = Project.create(title=name, created_at=datetime.now())
            cprint.print_info(f"Project {project.id} created")
            break
        except Exception as e:
            cprint.print_fail(e.message)


def choose_project():
    if is_no_projects():
        cprint.print_fail("!No projects created")
        return
    list_projects()
    while True:
        _id = input("Type project id: ")
        if not _id:
            cprint.print_fail("!Empty data")
            continue
        try:
            project = Project.get(id=_id)
            return project
        except Exception as e:
            cprint.print_fail(e.message)


def add_contract():
    contracts = Contract.select()
    if not contracts:
        cprint.print_fail("No contracts...")
        return
    
    project = choose_project()
    if not project:
        cprint.print_fail("Not found Project")
        return
    
    if project.active_contracts:
        cprint.print_fail("!Project has contract")
        return

    list_contracts()
    while True:
        _id = input("Type contract id (or 0 to go back): ")
        if _id == "0":
            return
        if not _id:
            cprint.print_fail("!Empty data")
            continue
        try:
            contract = Contract.get(id=_id)
            if contract.project:
                cprint.print_fail("This contract already in use")
                continue
            elif contract.status != "active":
                cprint.print_fail("This contract already in use")
                continue
            contract.project = project
            contract.save()
            cprint.print_pass("Contract added")
            break
        except Exception as e:
            cprint.print_fail(e.message)


def list_active_contracts(project):
    cprint.print_warn(f"[Project Active contracts]")
    for i in project.active_contracts:
        cprint.print_info(f"{i.id} - {i.title}")


def finish_project_contract():
    project = choose_project()
    if not project:
        cprint.print_fail("Not found project")
        return
    if not project.active_contracts:
        cprint.print_fail("Project has active contracts")
        return

    while True:
        list_active_contracts(project)
        _id = input("Type contract id (or 0 to go back): ")
        if _id == "0":
            return
        if not _id:
            cprint.print_fail("Empty data")
            continue
        try:
            contract = Contract.get(id=_id)
            if contract.project != project:
                cprint.print_fail("Different project contract")
                continue
            if contract.status != "active":
                cprint.print_fail("Not an active project")
                continue
            contract.status = "finished"
            contract.save()
            cprint.print_pass("Contract finished")
        except Exception as e:
            cprint.print_fail("Cant find contract")



def list_projects():
    projects = Project.select()
    if not len(projects):
        cprint.print_fail("No projects created")
    else:
        cprint.print_pass("--- Data ---")
        for prj in projects:
            cprint.print_info(f"{prj.id} - {prj.title}")
