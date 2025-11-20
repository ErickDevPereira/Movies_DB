import ui
import movie_abstraction
import custom_ERROR
from typing import Any, List, Dict
import data_transformation as DT
import DB.ddl as ddl

try:
    db: Any = ddl.create_everything('root', 'Ichigo007*')
except Exception as err:
    print(err)
else:
    loggin: ui.Login_Register = ui.Login_Register(db)
    loggin.open_window()