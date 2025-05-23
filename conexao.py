import pyodbc

def obter_conexao():
    conexao = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=sql_des;'
        'DATABASE=des_estagio;'
        'UID=user_all;'
        'PWD=t1c0ml8r@'
    )
    return conexao
