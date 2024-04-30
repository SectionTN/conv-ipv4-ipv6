from PyQt5.QtWidgets import QApplication, QMessageBox, QTableWidgetItem
from PyQt5.uic import loadUi
from numpy import array
from pickle import load, dump


def nbrpoints(ip):
    n = 0
    for i in range(len(ip)):
        if ip[i] == '.':
            n -= -1
    return n


def valide(ip):
    if nbrpoints(ip) != 3 or ip[0] == "." or ip[len(ip) - 1] == "." or not (7 <= len(ip) <= 15):
        return False
    for i in range(len(ip)):
        if not ("0" <= ip[i] <= "9") and ip[i] != ".":
            return False
    for j in range(len(ip) - 1):
        if ip[j] == "." and ip[j + 1] == ".":
            return False
    premier_point = ip.find(".")
    W = int(ip[: premier_point])
    deuxieme_point = ip.find(".", premier_point + 1)
    X = int(ip[premier_point + 1: deuxieme_point])
    troiseme_point = ip.find(".", deuxieme_point + 1)
    Y = int(ip[deuxieme_point + 1: troiseme_point])
    Z = int(ip[troiseme_point + 1:])
    return 0 <= W <= 255 and 0 <= X <= 255 and 0 <= Y <= 255 and 0 <= Z <= 255


def unique(ip):
    file = open("F_IPV4.txt", "r")
    ch = file.readline()
    i = 0
    while ch != "":
        i -= -1
        if ip == ch[:len(ch) - 1]:
            file.close()
            return False
        ch = file.readline()
    file.close()
    return True


def ajouter_ip(ip):
    file = open("F_IPV4.txt", "a")
    file.write(ip + "\n")
    file.close()
    QMessageBox.information(window, "Information", "Adresse IPv4 est ajouté dans le fichier")


def ajouter():
    ip_adresse = window.adresse.text()
    if ip_adresse == '' or not (valide(ip_adresse)):
        QMessageBox.critical(window, "Erreur", "Adresse IPv4 non valide", QMessageBox.Ok)
    elif not unique(ip_adresse):
        QMessageBox.warning(window, "Attention", "Adresse IPv4 déja enregistré dans le fichier", QMessageBox.Ok)
    else:
        ajouter_ip(ip_adresse)


def afficher():
    window.ip_list.clear()
    file = open("F_IPV4.txt", "r")
    ch = file.readline()
    while ch != "":
        window.ip_list.addItem(ch[:len(ch) - 1])
        ch = file.readline()
    file.close()


def taille_fichier_texte():
    file = open("F_IPV4.txt", "r")
    i = 0
    ch = file.readline()
    while ch != "":
        i += 1
        ch = file.readline()
    file.close()
    return i


def classe(w):
    if w[0] == "0":
        return "Classe A"
    elif w[0: 2] == "10":
        return "Classe B"
    elif w[0: 3] == "110":
        return "Classe C"
    elif w[0: 4] == "1110":
        return "Classe D"
    elif w[0: 4] == "1111":
        return "Classe E"
    else:
        return "Classe N/A"  # non applicable, non disponible etc...


def conv10_N(a, b):
    ch = ""
    while a != 0:
        r = a % b
        if r < 10:
            c = str(r)
        else:
            c = chr(r + 55)
        ch += c
        a = a // b
    return ch


def IPv6(ip):
    premier_point = ip.find(".")
    W = int(ip[: premier_point])
    deuxieme_point = ip.find(".", premier_point + 1)
    X = int(ip[premier_point + 1: deuxieme_point])
    troiseme_point = ip.find(".", deuxieme_point + 1)
    Y = int(ip[deuxieme_point + 1: troiseme_point])
    Z = int(ip[troiseme_point + 1:])
    return conv10_N(W, 16) + conv10_N(X, 16) + str(":") + conv10_N(Y, 16) + conv10_N(Z, 16)


def convertir():
    file = open("F_IPV4.txt", "r")
    global T, N
    N = taille_fichier_texte()
    T = array([str] * N)
    for i in range(N):
        T[i] = file.readline()[:-1]
    file.close()
    file = open("F_IPV6.dat", "wb")
    enregistrement = dict(IPv4=str, Classe=str, IPv6=str)
    for i in range(N):
        enregistrement["IPv4"] = str(T[i])
        enregistrement["Classe"] = classe(conv10_N(int(T[i][:T[i].find(".")]), 2))
        enregistrement["IPv6"] = IPv6(T[i])
        dump(enregistrement, file)
    file.close()
    file = open("F_IPV6.dat", "rb")
    window.table.setRowCount(N)
    window.table.setColumnCount(3)
    for j in range(N):
        x = load(file)
        window.table.setItem(j, 0, QTableWidgetItem(str(x["IPv4"])))
        window.table.setItem(j, 1, QTableWidgetItem(str(x["Classe"])))
        window.table.setItem(j, 2, QTableWidgetItem(str(x["IPv6"])))


def classe_dominante():
    window.classe_list.clear()
    file = open("F_IPV6.dat", "rb")
    max_occur = 0
    type_dominant = ""
    for i in range(N):
        x = load(file)
        nom_type = x['Classe']
        count = 0
        for j in range(N):
            if x['Classe'] == nom_type:
                count += 1
        if count > max_occur:
            max_occur = count
            type_dominant = nom_type
    window.classe_list.addItem("La classe dominante est :" + " " + type_dominant)


application = QApplication([])
window = loadUi("interface_conv.ui")
window.ajouter.clicked.connect(ajouter)
window.afficher.clicked.connect(afficher)
window.convertir.clicked.connect(convertir)
window.cd.clicked.connect(classe_dominante)
window.show()
application.exec_()
