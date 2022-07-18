import pandas as pd
import numpy as np
import pyodbc

connections = {'azure':{}}

def connect_azure_read(database='datascience-neogrid'):
    server = 'datascience-neogrid.database.windows.net'
    username='rerodrigues'
    password = 'Analytics2021'
    driver = 'ODBC Driver 17 for SQL Server'
    string_conexao = 'DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password+';'
    return pyodbc.connect(driver = driver, server=server, user=username, password=password, database=database)  

def connect_azure_write(database='datascience-neogrid'):
    import urllib
    from sqlalchemy import create_engine
    server = 'datascience-neogrid.database.windows.net'
    username='rerodrigues'
    password = 'Analytics2021'
    driver = 'ODBC Driver 17 for SQL Server'
    params = urllib.parse.quote_plus(
        'DRIVER=' + driver + ';' +
        'SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
    return create_engine("mssql+pyodbc:///?odbc_connect=%s" % params).connect()    

def connect_azure_sri(database='az-sri-data-lake-prd'):
    server = 'az-sri-data-lake-prd.database.windows.net'
    username = 'sri-data-lake-admin'
    password = 'fR2%7-xE3=KHP@St'
    driver= 'SQL Server Native Client 11.0'
    return pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password+';READONLY=True;')


def connect_azure_sqldw(database='azr-eu2-plat-sqldw-01'):
    server = 'azr-eu2-plat-sqldw-01.database.windows.net'
    username = 'data_quality'
    password = 'k(bsYX5hGIquQL'
    driver= 'ODBC Driver 17 for SQL Server'
    return pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password+';READONLY=True;')

def connect_azure_poc(database):
    server = 'neogrid-srv.database.windows.net'
    username = 'neogrid-login'
    password = 'N30@grid'
    driver= 'SQL Server Native Client 11.0'
    return pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password+';READONLY=True;')
#database: neogrid-db
#table [17:46] Diego Machado Garcia
#    ITEM_CATEGORIZED_FULL

#    neogrid-srv.database.windows.net
#login: neogrid-login
#senha: N30@grid
#

def connect_dw(database, server):
    server = server+'.ri.tic,1040'
    username = 'arq.gdaru'
    password = 'Lzk@@*4001'
    driver = 'SQL Server Native Client 11.0'
    return pyodbc.connect(
        'DRIVER=' + driver + ';SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD='
        + password + ';READONLY=True;domain=viveiro;Trusted_Connection=yes;')




def cdm_list_azure(database='azr-eu2-plat-sqldw-01'):
    with connect_azure_sqldw(database) as cnxn:
        cursor = cnxn.cursor()
        tables = pd.DataFrame(cursor.tables())
        tables.columns=['Infos']
        tables['Schema']=tables.Infos.apply(lambda x: x[1])
        tables['Tabela']=tables.Infos.apply(lambda x: x[2])
        tables['Tipo']=tables.Infos.apply(lambda x: x[3])
        tables['Produto'] = tables.Schema.apply(lambda x: x.split('_')).apply(lambda x: x[0])
    return tables[tables.Produto=='CDM'].Schema.unique()

def rdw_list_azure(database='azr-eu2-plat-sqldw-01'):
    with connect_azure_sqldw(database) as cnxn:
        cursor = cnxn.cursor()
        tables = pd.DataFrame(cursor.tables())
        tables.columns = ['Infos']
        tables['Schema'] = tables.Infos.apply(lambda x: x[1])
        tables['Tabela'] = tables.Infos.apply(lambda x: x[2])
        tables['Tipo'] = tables.Infos.apply(lambda x: x[3])
        tables['Produto'] = tables.Schema.apply(lambda x: x.split('_')).apply(lambda x: x[0])
    return tables[tables.Produto == 'RDW'].Schema.unique()


def connect_ghdaru_database(database):
    import urllib
    from sqlalchemy import create_engine
    server = 'datascienceneogrid.database.windows.net'
    username = 'ghdaru'
    password = 'TempCurso$'
    driver = 'ODBC Driver 13 for SQL Server'
    params = urllib.parse.quote_plus(
        'DRIVER=' + driver + ';' +
        'SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
    return create_engine("mssql+pyodbc:///?odbc_connect=%s" % params).connect()


def connect_ghdaru_database_2(database):
    import pyodbc
    server = 'datascienceneogrid.database.windows.net'
    username = 'ghdaru'
    password = 'TempCurso$'
    driver= 'ODBC Driver 13 for SQL Server'
    return pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)

def connect_local(database):
    server = 'BR-PRD-DQL-01'
    driver= 'SQL Server'
    conn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';Trusted_Connection=yes;')
    return conn
def make_string(banco, dialeto, driver, porta, server, odbc_connect, database, adicional):
    string = banco + '+' +  dialeto + ":///"
    string += 'odbc_connect=' + odbc_connect
    string += ''
    return string

#engine = create_engine("mssql+pyodbc://USERNAME:PASSWORD@HOST_IP:PORT/DATABASENAME?driver=SQL+Server+Native+Client+11.0")
def make_url(database):
    server = 'dwe.ri.tic'
    driver= 'SQL+Server+Native+Client+11.0'
    user = 'viveiro/arq.gdaru'
    password = 'Lzk@@*4001'
    domain = 'viveiro'
    string = 'mssql+pyodbc://'
    string += user +':' + password + '@' + server + ',1040' +'/' + database + '?driver=' + driver #+ '&domain=' +  domain
    return string

#Origem: https://docs.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-python
class neo_azure():
    connection = {'datascience':"DefaultEndpointsProtocol=https;AccountName=dataqualitystoragedir;AccountKey=fJIP8SnBEad/kO11dV2wmeDI1PMWcbSLoR1qHi4H6/6m/WzGxg7UMeIyWD8c2OaWnJznq3ZiAPK5DMVXM7e2xg==;EndpointSuffix=core.windows.net"
        ,'sri':None}
    def __init__(self,blob='datascience'):
        from azure.storage.blob import BlobServiceClient
        self.connection_string = self.connection[blob]
        self.blob = BlobServiceClient.from_connection_string(self.connection_string)

    def get_containers(self):
        all = list(self.blob.list_containers(include_metadata=True))
        return [a['name'] for a in all]

    def write(self,file,container):
        import os
        #https://stackoverflow.com/questions/17057544/how-can-i-extract-the-folder-path-from-file-path-in-python
        filedata = os.path.split(os.path.abspath(file))
        blob_client = self.blob.get_blob_client(container=container, blob=filedata[-1])
        # Upload the created file
        with open(file, "rb") as data:
            blob_client.upload_blob(data)

    def read(self, file, container):
        import os
        filedata = os.path.split(os.path.abspath(file))
        blob_client = self.blob.get_blob_client(container=container, blob=filedata[-1])
        return blob_client.download_blob().readall()

    def ls(self,container):
        container_client = self.blob.get_container_client(container)
        blob_list = [ a['name'] for a in list(container_client.list_blobs())]
        return blob_list






