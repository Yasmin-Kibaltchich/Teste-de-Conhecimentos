from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import sqlite3
import dateparser as date_parser
import re


app = FastAPI()


class Cliente (BaseModel):
    cdCliente: int
    cdStatus: int
    nome: str
    telefone: str
    cpf: str
    endereco: str
    email: str
    dataCadastro: datetime


class Vaga (BaseModel):
    cdVaga: int
    cdStatus: int
    dataCadastro: datetime
    ufVaga: str
    salario: float


class Empresa (BaseModel):
    cdEmpresa: int   
    cdStatus: int
    nome: str
    endereco: str
    telefone: str
    cnpj: str
    dataCadastro: datetime

def validate_email(email):
    padrao = r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"
    return re.match(padrao, email) is not None


def validate_telefone(str):
    padrao = r"\(\d{2}\) \d{5}-\d{4}"
    return re.findall(padrao, str)
    

def validate_cpf(cpf):
    padrao = r"\d{3}\.\d{3}\.\d{3}-\d{2}"
    return re.match(padrao, cpf) is not None


def validate_cnpj(cnpj):
    padrao = r"\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}"
    return re.match(padrao, cnpj) is not None    


email = "exemplo@exemplo.com" or "exemplo@exemplo.com.br"
telefone = "Exemplo de texto números de telefone: (23) 98456-7890, (87) 98654-3210."
cpf = "123.456.789-09"
cnpj = "12.345.678/0001-90"

print("E-mail válido:", validate_email(email))
print("Números de telefone:", validate_telefone(telefone))
print("CPF válido:", validate_cpf(cpf))
print("CNPJ válido:", validate_cnpj(cnpj))



@app.get('/GetVagas')
def GetVagas():
    conn = sqlite3.connect("Vaga.db")
    cursor = conn.cursor()
    sql = "SELECT * FROM Vaga"
    cursor.execute(sql)
    fetchall = cursor.fetchall()
    listaVagas = []
    for vaga in fetchall:
        listaVagas.append(vaga)

    print (listaVagas)    
    cursor.close()
    return listaVagas


@app.get('/GetClientes')
def GetClientes():
    conn = sqlite3.connect("Vaga.db")
    cursor = conn.cursor()
    sql = "SELECT * FROM Cliente"
    cursor.execute(sql)
    fetchall = cursor.fetchall()
    listaClientes = []
    for cliente in fetchall:
        listaClientes.append(cliente)

    print(listaClientes)    
    cursor.close()
    return listaClientes


@app.get('/GetEmpresas')
def GetEmpresas():
    conn = sqlite3.connect("Vaga.db")
    cursor = conn.cursor()
    sql = "SELECT * FROM Empresa"
    cursor.execute(sql)
    fetchall = cursor.fetchall()
    listaEmpresas = []
    for empresa in fetchall:
        listaEmpresas.append(empresa)

    print(listaEmpresas)    
    cursor.close()
    return listaEmpresas


@app.post('/CreateClientes')
def CreateClientes(info: Cliente):
    conn = sqlite3.connect("Vaga.db")
    cursor = conn.cursor()
    dataCadastro = datetime.utcnow()
    print (dataCadastro)

    if not validate_email(info.email):
        return {'Mensagem': 'E-mail inválido'}

    if not validate_cpf(info.cpf):
        return {'Mensagem': 'CPF inválido'}
    
    if not validate_telefone(info.telefone):
        return {'Mensagem': 'Telefone inválido'}

    
    cursor.execute("INSERT INTO cliente (CdStatus, Nome, Telefone, Cpf, Endereco, Email, DataCadastro) VALUES (?,?,?,?,?,?,?)",(int(info.cdStatus), str(info.nome) , str (info.telefone), str(info.cpf), str(info.endereco), str(info.email), str(info.dataCadastro)))  
    
    conn.commit()
    
    cursor.close()
    return {'Mensagem': 'Sucesso'}


@app.post('/CreateVagas')
def CreateVagas(info: Vaga):
    conn = sqlite3.connect("Vaga.db")
    cursor = conn.cursor()
    dataCadastro = datetime.utcnow()
    print (dataCadastro)
    cursor.execute("INSERT INTO Vaga (CdStatus, DataCadastro, UFVaga, Salario) VALUES (?,?,?,?)",(int(info.cdStatus), str(info.dataCadastro) ,str(info.ufVaga), float(info.salario)))
    
    conn.commit()
    cursor.close()
    return {'Mensagem': 'Sucesso'}
    

@app.post('/CreateEmpresas')    
def CreateEmpresas(info: Empresa):
   conn = sqlite3.connect("Vaga.db")
   cursor = conn.cursor()
   dataCadastro = datetime.utcnow()
   print (dataCadastro)

   if not validate_telefone(info.telefone):
        return {'Mensagem': 'Telefone inválido'}

   if not validate_cnpj(info.cnpj):
        return {'Mensagem': 'CNPJ inválido'}

   cursor.execute("INSERT INTO Empresa (CdStatus, Nome, Endereco, Telefone, Cnpj, DataCadastro) values (?,?,?,?,?,?)",(int(info.cdStatus), str(info.nome), str(info.endereco), str(info.telefone), str(info.cnpj), str(dataCadastro)))

   conn.commit()
   cursor.close() 
   return {'Mensagem': 'Sucesso'}



@app.put('/UpdateVagas/{cdVaga}')
def UpdateVagas(cdVaga: int, info: Vaga):
    conn = sqlite3.connect('Vaga.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Vaga WHERE CdVaga = ?", (cdVaga,))
    existe_pedido = cursor.fetchone()
    
    if not existe_pedido:
        raise FastAPI.HTTPException(status_code=404, detail='Vaga não encontrada')
    

    dataconvertida = info.dataCadastro

    

    cursor.execute(""" 
                   UPDATE Vaga
                   SET CdVaga = ?, CdStatus = ?, DataCadastro = ?, UfVaga = ?, Salario = ? 
                   WHERE CdVaga = ?
                   """, (info.cdVaga, info.cdStatus, dataconvertida, info.ufVaga, info.salario, cdVaga))

    conn.commit()
    cursor.close()
    return {'Mensagem': 'Vaga atualizada com sucesso'}


@app.put('/UpdateClientes/{cdCliente}')
def UpdateClientes(cdCliente: int, info: Cliente):
    conn = sqlite3.connect('Vaga.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Cliente WHERE CdCliente = ?", (cdCliente,))
    existe_cliente = cursor.fetchone()
    
    if not existe_cliente:
        raise FastAPI.HTTPException(status_code=404, detail='Cliente não encontrado')
    
    dataconvertida = info.dataCadastro

    cursor.execute(""" 
                   UPDATE Cliente
                   SET CdCliente = ?, CdStatus = ?, Nome = ?, Telefone = ?, Cpf = ?, Endereco = ?, Email = ?, DataCadastro = ?
                   WHERE CdCliente = ?
                   """, (info.cdCliente, info.cdStatus, info.nome, info.telefone, info.cpf, info.endereco, info.email, dataconvertida, cdCliente))

    conn.commit()
    cursor.close()
    return {'Mensagem': 'Cliente atualizado com sucesso'}    


@app.put('/UpdateEmpresas/{cdEmpresa}')
def UpdateEmpresas(cdEmpresa: int, info: Empresa):
    conn = sqlite3.connect('Vaga.db')
    cursor = conn.cursor()

    
    cursor.execute("SELECT * FROM Empresa WHERE CdEmpresa = ?", (cdEmpresa,))
    existe_empresa = cursor.fetchone()
    
    if not existe_empresa:
        raise FastAPI.HTTPException(status_code=404, detail='Empresa não encontrada')

   
    dataconvertida = info.dataCadastro

  
    cursor.execute(""" 
                   UPDATE Empresa
                   SET CdEmpresa = ?, CdStatus = ?, Nome = ?, Endereco = ?, Telefone = ?, Cnpj = ?, DataCadastro = ?
                   WHERE CdEmpresa = ?
                   """, (info.cdEmpresa, info.cdStatus, info.nome, info.endereco, info.telefone, info.cnpj, dataconvertida, cdEmpresa))

    conn.commit()
    cursor.close()
    return {'Mensagem': 'Cadastro atualizado com sucesso'}
 


@app.delete('/DeleteVagas/{cdVaga}')
def DeleteVagas(cdVaga: int):
    conn = sqlite3.connect('Vaga.db')
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Vaga WHERE CdVaga = ?", str(cdVaga))
        cursor.execute("DELETE FROM Vaga WHERE CdVaga = {}".format(cdVaga))

    except:
        return {'Ocorreu um erro': cdVaga}
    finally:
        conn.commit()

    cursor.close()    
    return {'Mensagem': 'Vaga deletada com sucesso'}


@app.delete('/DeleteClientes/{cdCliente}')
def DeleteClientes(cdCliente: int):
    conn = sqlite3.connect('Vaga.db')
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Cliente WHERE CdCliente = ?", str(cdCliente))
        cursor.execute("DELETE FROM Cliente WHERE CdCliente = {}".format(cdCliente))

    except:
        return {'Ocorreu um erro': cdCliente}
    finally:
        conn.commit()

    cursor.close()    
    return {'Mensagem': 'Cliente deletado com sucesso'}
    

@app.delete('/DeleteEmpresas/{cdEmpresa}')
def DeleteClientes(cdEmpresa: int):
    conn = sqlite3.connect('Vaga.db')
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Empresa WHERE CdEmpresa = ?",str(cdEmpresa))
        cursor.execute("DELETE FROM Empresa WHERE CdEmpresa = {}".format(cdEmpresa))

    except:
        return {'Ocorreu um erro': cdEmpresa}
    finally:
        conn.commit()

    cursor.close()    
    return {'Mensagem': 'Empresa deletada com sucesso'}    
