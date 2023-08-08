from fastapi import FastAPI, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from models import ModelEmployee
from database import Base, engine, get_db

app = FastAPI()


@app.on_event("startup")
# create table
def create_table():
    Base.metadata.create_all(bind=engine)


@app.get("/employees/")
# return table
def get_employees(db: Session = Depends(get_db)):
    """
    Retrieve a list of all employees from the database.
    This endpoint queries the database to retrieve a list of all employees
    present in the 'employee' table.
    """
    employees = db.query(ModelEmployee).all()
    if not employees:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Employee not found")
    return {"status": "success", "employees": employees}


@app.post("/employees/")
# insert data into the table
def create_employees(name: str, department: str, db: Session = Depends(get_db)):
    """
    Insert a new employee record into the database.
    This endpoint adds a new employee record to the 'employee' table in the database.
    """
    try:
        employee = ModelEmployee(name=name, department=department)
        db.add(employee)
        db.commit()
        return {"Successfully added an employee with the name": employee.name}
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@app.get("/employees/{emp_id}")
# return table based on employee id
def get_employees(emp_id: str, db: Session = Depends(get_db)):
    """
    Retrieve employee details based on employee ID.

    This endpoint queries the database to retrieve the details of an employee based
    on the provided employee ID.

    """
    employee = db.query(ModelEmployee).filter(
        ModelEmployee.id == emp_id).first()
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Coultnot get the employee with employee id{emp_id}")

    return {"status_code": status.HTTP_200_OK, "employee": employee}


@app.put("/employees/{emp_id}/{field}/{new_value}")
# update the table using employeeid and set new value of a field
def update_employee(emp_id: str, field: str, new_value: str, db: Session = Depends(get_db)):
    """
    Update a specific field of an employee based on employee ID.

    This endpoint updates a specified field of an employee record in the 'employee' table
    based on the provided employee ID. The specified field is updated with the new value.

    """
    employee_query = db.query(ModelEmployee).filter(
        ModelEmployee.id == emp_id)
    emp_db = employee_query.first()
    print(emp_db, "<=============================================== Employee")
    if not emp_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Coultnot get the employee with employee id{emp_id}")

    setattr(emp_db, field, new_value)
    db.add(emp_db)
    db.commit()
    db.refresh(emp_db)

    return {"status": "Employe detail updated successfully", "employee": emp_db}


@app.delete("/employees/{emp_id}")
# delete data from a table using employee_id
def delete_employee(emp_id: str, db: Session = Depends(get_db)):
    """
    Delete an employee record based on employee ID.

    This endpoint deletes an employee record from the 'employee' table based on the provided
    employee ID.

    """
    employee_query = db.query(ModelEmployee).filter(
        ModelEmployee.id == emp_id)
    emp_db = employee_query.first()
    if not emp_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Employee with {emp_id} not found")

    employee_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
