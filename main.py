from PyQt5 import uic, QtWidgets
from tkinter import messagebox
import tkinter as tk
import sqlite3
import conexao_bd
from backup import backup

root = tk.Tk()

root.overrideredirect(1)  # para nao abrir um janela (TK)
root.withdraw()

banco = sqlite3.connect('database.db')
cursor = banco.cursor()


def abrir_inserir_cadastro():
    inserir_cadastro.show()


def abrir_tela_excluir():
    tela_excluir.show()


def abrir_diminuir_total():
    diminuir_total.show()


def add_divida():
    nome = inserir_cadastro.lineEdit.text()
    numero = inserir_cadastro.lineEdit_4.text()
    item = inserir_cadastro.lineEdit_2.text()
    valor = inserir_cadastro.lineEdit_3.text()

    if valor.isdigit():
        if len(nome) >= 2 and len(numero) >= 2 and len(item) >= 2:
            try:
                cursor.execute(
                    "INSERT INTO clientes Values('" + nome + "','" + numero + "','" + item + "','" + valor + "') ")
                banco.commit()
                tela_cadastro.radioButton_5.setChecked(True)
                pesquisar()
                messagebox.showinfo("showinfo", "Venda adicionado com sucesso!")
                inserir_cadastro.close()
                total_receber()
            except:
                messagebox.showwarning("showwarning", "Este nome ja existe no banco de dados!")
        else:
            messagebox.showwarning("showwarning", "Digite em todos campos")
    else:
        messagebox.showwarning("showwarning", "Digite numeros no valor total!")

    inserir_cadastro.lineEdit.setText('')
    inserir_cadastro.lineEdit_2.setText('')
    inserir_cadastro.lineEdit_3.setText('')
    inserir_cadastro.lineEdit_4.setText('')


def diminuir_valor():
    pagador = diminuir_total.lineEdit.text()
    try:
        cursor.execute("SELECT valor FROM clientes WHERE nome ='" + pagador + "'")
        valor_atual = cursor.fetchall()[0][0]
        removimento = diminuir_total.lineEdit_3.text()

        if removimento.isdigit():

            if diminuir_total.radioButton_2.isChecked():
                novo_valor = int(valor_atual) + int(removimento)
            if diminuir_total.radioButton.isChecked():
                novo_valor = int(valor_atual) - int(removimento)

            novo_valor = str(novo_valor)

            if int(valor_atual) >= int(removimento):
                cursor.execute("UPDATE clientes SET valor = '" + novo_valor + "' WHERE nome = '" + pagador + "'")
                messagebox.showinfo("showinfo", "Venda atualizada com sucesso!")
                diminuir_total.lineEdit.setText('')
                diminuir_total.lineEdit_3.setText('')
                diminuir_total.close()

                banco.commit()
                tela_cadastro.radioButton_5.setChecked(True)
                pesquisar()
            else:
                messagebox.showinfo("showwarning", "O valor pago nao pode ser maior que o total da divida")
        else:
            messagebox.showinfo("showwarning", "Adicione numeros na opçao (Valor)")
    except:
        messagebox.showinfo("showwarning", "Nome nao encontrado no banco de dados")


def excluir_dados():
    try:
        nome = tela_excluir.lineEdit.text()

        cursor.execute("SELECT valor FROM clientes WHERE nome ='" + nome + "'")
        valor_atual = cursor.fetchall()[0][0]

        cursor.execute("SELECT total FROM faturamento WHERE mes ='agosto'")
        atualmente = cursor.fetchall()[0][0]

        novo_valor = valor_atual + atualmente
        novo_valor = str(novo_valor)

        cursor.execute("UPDATE faturamento SET total = '" + novo_valor + "' WHERE mes = 'agosto'")

        cursor.execute("DELETE FROM clientes WHERE nome='" + nome + "';")

        messagebox.showinfo("showinfo", "Parabens por mais uma venda! Sunga Imports")

        tela_excluir.lineEdit.setText('')

        tela_excluir.close()
        total_receber()
        banco.commit()
        tela_cadastro.radioButton_5.setChecked(True)
        pesquisar()
    except:
        messagebox.showinfo("showwarning", "Nome não encontrado no banco de dados")


def total_receber():
    cursor.execute("SELECT valor FROM clientes")  # check valor total
    dividas = cursor.fetchall()

    x = 0
    for i in dividas:
        x = x + i[0]

    tela_cadastro.pushButton.setText(f'Ola Leandro voce tem R${x} para receber ainda.')


def atualiza_tabela_principal():
    # Setando numero de linhas, colunas e nome das colunas
    tela_cadastro.tableWidget.setRowCount(len(conexao_bd.read_all()))
    tela_cadastro.tableWidget.setColumnCount(len(conexao_bd.read_all()[0]))
    tela_cadastro.tableWidget.setHorizontalHeaderLabels(
        ["Nome do Cliente", "Numero Cliente", "Item vendido", "Valor restante"])

    # Inserindo os dados na tabela
    rows = conexao_bd.read_all()

    for i in range(len(rows)):  # linha
        for j in range(len(rows[0])):  # coluna
            item = QtWidgets.QTableWidgetItem(f"{rows[i][j]}")
            tela_cadastro.tableWidget.setItem(i, j, item)


def pesquisar():
    try:
        if tela_cadastro.radioButton_5.isChecked():  # check tudo
            tela_cadastro.lineEdit.setText('')
            atualiza_tabela_principal()
            return

        # Verificando se o texto da caixa pesquisa esta vazio
        pesquisa = tela_cadastro.lineEdit.text()
        if pesquisa == '':
            QtWidgets.QMessageBox.about(tela_cadastro, 'Alerta', 'Por favor digite um valor para a pesquisa')
            return

        if tela_cadastro.radioButton_6.isChecked():  # check nome
            pesquisa = tela_cadastro.lineEdit.text()
            rows = conexao_bd.read_nome(pesquisa)

            limpa_tabela(len(rows))
            for i in range(len(rows)):  # linha
                for j in range(len(rows[0])):  # coluna
                    item = QtWidgets.QTableWidgetItem(f"{rows[i][j]}")
                    tela_cadastro.tableWidget.setItem(i, j, item)

        if tela_cadastro.radioButton_3.isChecked():  # check numero
            pesquisa = tela_cadastro.lineEdit.text()
            rows = conexao_bd.read_numero(pesquisa)
            print('chego')
            limpa_tabela(len(rows))
            for i in range(len(rows)):  # linha
                for j in range(len(rows[0])):  # coluna
                    item = QtWidgets.QTableWidgetItem(f"{rows[i][j]}")
                    tela_cadastro.tableWidget.setItem(i, j, item)

        if tela_cadastro.radioButton_4.isChecked():  # check item
            pesquisa = tela_cadastro.lineEdit.text()
            rows = conexao_bd.read_item(pesquisa)

            limpa_tabela(len(rows))
            for i in range(len(rows)):  # linha
                for j in range(len(rows[0])):  # coluna
                    item = QtWidgets.QTableWidgetItem(f"{rows[i][j]}")
                    tela_cadastro.tableWidget.setItem(i, j, item)
    except:
        ...


def limpa_tabela(valor):
    # Valor é o valor de linhas que terá a tabela
    if valor == 1:
        tela_cadastro.tableWidget.setRowCount(1)
        tela_cadastro.tableWidget.setColumnCount(len(conexao_bd.read_all()[0]))
        tela_cadastro.tableWidget.setHorizontalHeaderLabels(
            ["Nome do cliente", "Numero do cliente", "Item vendido", "Valor Restante"])
    else:
        tela_cadastro.tableWidget.setRowCount(valor)
        tela_cadastro.tableWidget.setColumnCount(len(conexao_bd.read_all()[0]))
        tela_cadastro.tableWidget.setHorizontalHeaderLabels(
            ["Nome do cliente", "Numero do cliente", "Item vendido", "Valor Restante"])


app = QtWidgets.QApplication([])
tela_cadastro = uic.loadUi("ui\\tela_cadastro.ui")
inserir_cadastro = uic.loadUi("ui\\atualizar_dados.ui")
diminuir_total = uic.loadUi("ui\\diminuir_total.ui")
tela_excluir = uic.loadUi("ui\\tela_excluir.ui")
tela_cadastro.pushButton_2.clicked.connect(abrir_inserir_cadastro)
tela_cadastro.pushButton_5.clicked.connect(backup)
tela_cadastro.pushButton_3.clicked.connect(abrir_diminuir_total)
tela_cadastro.pushButton_4.clicked.connect(abrir_tela_excluir)
inserir_cadastro.pushButton.clicked.connect(add_divida)
diminuir_total.pushButton.clicked.connect(diminuir_valor)
tela_excluir.pushButton.clicked.connect(excluir_dados)

tela_cadastro.pushButton_7.clicked.connect(pesquisar)

tela_cadastro.show()
total_receber()
tela_cadastro.radioButton_5.setChecked(True)
diminuir_total.radioButton.setChecked(True)
pesquisar()
app.exec()
