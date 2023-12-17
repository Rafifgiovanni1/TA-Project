from flask import abort,flash,redirect,url_for
from flask_login import current_user
from functools import wraps
import pandas as pd
import re

def is_admin(func):
    """check if user email is admin"""

    @wraps(func)
    def check(*args, **kwargs):
        print(current_user.role)
        if (
            current_user.is_authenticated and not current_user.role == "admin"
        ) or not current_user.is_authenticated:
            return abort(404)
        return func(*args, **kwargs)

    return check

def to_tables(sqlquerylist: list,drop_column = [],reorder_column = [],rename_column = {},link_id = True,escape = False,index = False,capitalize_columns = [],id_url = "",url_id="id"):
    query: pd.DataFrame = pd.DataFrame([query.__dict__ for query in sqlquerylist])

    if len(query) <= 0:
        return query.to_html(classes=["table","table-hover"],table_id="table")

    if id_url:
        query[url_id] = query[url_id].apply(lambda x: f"<a href='{url_for(id_url,id=x)}' class='text-decoration-none'>{x}</a>")

    for column in capitalize_columns:
        query[column] = query[column].str.upper()

    query = query.drop(drop_column,axis=1).reindex(reorder_column,axis=1).rename(rename_column,axis=1)
    return query.to_html(classes=["table","table-hover"],index=index,escape=escape,table_id="table")

def check_files(files,filename_pattern: str,pattern_not_match_msg=""):
    pattern = filename_pattern
    
    if not re.match(pattern,files.filename):
        return False,pattern_not_match_msg
            
    if files.content_type != "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
        return False,"File harus berbentuk file excel"

    return True,None
