import sys
import mysql.connector
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox, QWidget, QCalendarWidget
from PyQt5.uic import loadUi

connection = mysql.connector.connect(host='localhost',
                                     database='db_pythonproject',
                                     user='root',
                                     password='root')

no_wid = 0


class Login(QDialog):

    def __init__(self):
        super(Login, self).__init__()
        loadUi('gui/loginGui.ui', self)
        self.loginButton.clicked.connect(self.checkData)
        self.mW = MainWindow()
        self.widget.setPixmap(QPixmap("image/logo.PNG"))

    def accepted(self):
        self.mW.show()

    def messagebox(self):
        QMessageBox.warning(self, 'Komunikat', 'Podane dane są nieprawidłowe lub nie istnieją w bazie.')

    def messagebox_emptyscope(self):
        QMessageBox.warning(self, 'Komunikat', 'Wszystkie pola muszą być uzupełnione.')

    def checkData(self):

        login = self.loginline.text()
        password = self.passwordline.text()

        if login and password != '':
            cur = connection.cursor()
            query = "select count(login) from login where login = " + "'" + login + "'" + " and password = " + "'" + password + "'" + ";"
            cur.execute(query)
            countlogin = cur.fetchall()

            cur = connection.cursor()
            query1 = "select idLogin from login where login = " + "'" + login + "'" + " and password = " + "'" + password + "'" + ";"
            cur.execute(query1)
            id_user = cur.fetchall()

            for row in id_user:
                id_user = row[0]

            for row in countlogin:
                countlogin = row[0]

            if countlogin == 1:
                global now_id
                now_id = id_user
                self.accepted()

            if countlogin == 0:
                self.messagebox()

            cur.close()
            self.close()

        else:
            self.messagebox_emptyscope()


class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi('gui/mainWindowGui.ui', self)
        self.AddPatientButton.clicked.connect(self.patient)
        self.registerButton.clicked.connect(self.register)
        self.endButton.clicked.connect(self.end)
        self.showPatientsButton.clicked.connect(self.showPatients)
        self.VisitsButton.clicked.connect(self.registervisit)
        self.p = Patients()
        self.r = Register()
        self.s = ShowPatients()
        self.w = RegisterVisit()

    def registervisit(self):
        self.w.show()

    def patient(self):
        self.p.show()

    def register(self):
        self.r.show()

    def end(self):
        buttonReply = QMessageBox.question(self, 'Question', "Czy napewno chcesz wyjść?",
                                           QMessageBox.Yes | QMessageBox.No,
                                           QMessageBox.Yes)
        if buttonReply == QMessageBox.Yes:
            app.closeAllWindows()

    def showPatients(self):
        self.s.show()


class Patients(QDialog):
    def __init__(self):
        super(Patients, self).__init__()
        loadUi('gui/AddPatientsGui.ui', self)
        self.saveButton.clicked.connect(self.insertToDatabase)
        self.cancelButton.clicked.connect(self.cancel)

    def cancel(self):
        buttonReply = QMessageBox.question(self, 'Question', "Czy napewno chcesz anulować dodawanie pacjenta?",
                                           QMessageBox.Yes | QMessageBox.No,
                                           QMessageBox.Yes)
        if buttonReply == QMessageBox.Yes:
            self.close()

    def messagebox(self):
        QMessageBox.information(self, 'Komunikat', 'Pacjent dodany poprawnie.')
        self.close()

    def messageboxSex(self):
        QMessageBox.information(self, 'Komunikat', 'Wybierz płeć.')

    def messageboxWrongPesel(self):
        QMessageBox.information(self, 'Komunikat', 'Pesel niepoprawny. Pesel musi posiadać 11 cyfr.')

    def insertToDatabase(self):
        name = self.nameEditText.text()
        surname = self.surnameEditText.text()
        pesel = self.peselEditText.text()
        birthdate = self.birthDateEditText.text()
        street = self.streetEditText.text()
        houseNumer = self.houseNumerEditText.text()
        city = self.cityEditText.text()
        postCode = self.postCodeEditText.text()
        flat = self.numberFlatEditText.text()
        phone = self.phoneEditText.text()
        email = self.emailEditText.text()
        nameAuthorizedPerson = self.nameAuthorizedPersonEditText.text()
        surnameAuthorizedPerson = self.surnameAuthorizedPersonEditText.text()
        peselAuthorizedPerson = self.peselAuthorizedPersonEditText.text()
        phoneAuthorizedPerson = self.phoneAuthorizedPersonEditText.text()

        print(len(pesel))

        if len(pesel) != 11 or len(peselAuthorizedPerson) != 11:
            self.messageboxWrongPesel()
        else:
            if self.womanRadioButton.isChecked():
                sex = 'kobieta'
            elif self.menRadioButton.isChecked():
                sex = 'mężczyzna'

            cur = connection.cursor()
            cur.execute("Insert into patients(Name, Surname, Pesel, BirthDate, Street, House, Flat, City, PostCode, Phone, Mail, NameAuthorizedPerson, SurnameAuthorizedPerson, PeselAuthorizedPerson, PhoneAuthorizedPerson, Sex) values('" + name + "', '" + surname + "', '" + pesel + "', '" + birthdate + "', '" + street + "', '" + houseNumer + "', '" + flat + "', '" + city + "', '" + postCode + "', '" + phone + "', '" + email + "', '" + nameAuthorizedPerson + "', '" + surnameAuthorizedPerson + "', '" + peselAuthorizedPerson + "', '" + phoneAuthorizedPerson + "', '" + sex + "')")
            connection.commit()
            self.messagebox()


class Register(QDialog):

    def __init__(self):
        super(Register, self).__init__()
        loadUi('gui/registerGui.ui', self)
        self.registerButton.clicked.connect(self.register)
        self.cancelButton.clicked.connect(self.cancel)

    def cancel(self):
        buttonReply = QMessageBox.question(self, 'Question', "Czy napewno chcesz anulować rejestrację użytkownika?",
                                           QMessageBox.Yes | QMessageBox.No,
                                           QMessageBox.Yes)
        if buttonReply == QMessageBox.Yes:
            self.close()

    def messageboxWrongPasswords(self):
        QMessageBox.warning(self, 'Komunikat', 'Hasła są różne.')

    def messageboxEmptyScope(self):
        QMessageBox.warning(self, 'Komunikat', 'Wszystkie pola muszą być uzupełnione.')

    def messagebox(self):
        QMessageBox.information(self, 'Komunikat', 'Rejestracja zakończona powodzeniem.')
        self.close()

    def messageboxExist(self):
        QMessageBox.information(self, 'Komunikat', 'Użytkownik z takim loginem już istnieje w bazie.')

    def register(self):
        login = self.userNameEditText.text()
        password = self.passwordEditText.text()
        passwordAgain = self.passwordAgainEditText.text()

        cur = connection.cursor()
        query = "select count(login) from login where login = " + "'" + login + "'" + ";"
        cur.execute(query)
        countlogin = cur.fetchall()

        for row in countlogin:
            countlogin = row[0]
            print(countlogin)

        if countlogin == 0:
            if password == passwordAgain:
                if login and password and passwordAgain != '':
                    cur = connection.cursor()
                    cur.execute("Insert into login(login, password) values('" + login + "', '" + password + "')")
                    connection.commit()
                    self.messagebox()

                else:
                    self.messageboxEmptyScope()
            else:
                self.messageboxWrongPasswords()
        else:
            self.messageboxExist()


class ShowPatients(QDialog):

    def __init__(self):
        super(ShowPatients, self).__init__()
        loadUi('gui/showPatientsGui.ui', self)
        self.valueFindButton.clicked.connect(self.valueFind)
        self.comboboxButton.clicked.connect(self.comboBoxFilters)

        self.comboBox.addItem("-")
        self.comboBox.addItem("daty urodzenia rosnąco")
        self.comboBox.addItem("daty urodzenia malejąco")
        self.comboBox.addItem("nazwiska od a do z")
        self.comboBox.addItem("nazwiska od z do a")
        self.comboBox.addItem("pesel rosnąco")
        self.comboBox.addItem("pesel malejąco")

        self.listWidget.clear()
        cur = connection.cursor()
        query = "select Pesel, Surname, Name from patients;"
        cur.execute(query)
        value = cur.fetchall()

        queryCount = "select count(Pesel) from patients;"
        cur.execute(queryCount)
        count = cur.fetchall()

        patients = []

        for rowCount in count:
            if(rowCount[0]) == 0:
                self.listWidget.addItem("BRAK DANYCH W BAZIE")
            if (rowCount[0]) != 0:
                for row in value:

                    self.listWidget.addItem(str(row[0]) + " " + str(row[1]) + " " + str(row[2]))


    def valueFind(self):
        self.listWidget.clear()
        valueFind = self.valueFindEditText.text()
        print(valueFind)
        cur = connection.cursor()
        if valueFind is not None:
            query = "select Pesel, Surname, Name from patients where Surname = '" + valueFind + "' OR Name = '" + valueFind + "' OR Pesel = '" + valueFind + "' OR City = '" + valueFind + "' OR PostCode = '" + valueFind + "' OR Phone = '" + valueFind + "' OR Street = '" + valueFind + "' OR Mail = '" + valueFind + "'"
        else:
            query = "select Pesel, Surname, Name from patients"
        cur.execute(query)
        value = cur.fetchall()

        queryCount = "select count(Pesel) from patients;"
        cur.execute(queryCount)
        count = cur.fetchall()

        for rowCount in count:
            if (rowCount[0]) == 0:
                self.listWidget.addItem("BRAK DANYCH W BAZIE")
            if (rowCount[0]) != 0:
                for row in value:
                    self.listWidget.addItem(str(row[0]) + " " + str(row[1]) + " " + str(row[2]))

    def comboBoxFilters(self):
        valueFind = self.valueFindEditText.text()
        combotext = self.comboBox.currentText()
        if combotext == '-':
            dod = ''
        elif combotext == 'daty urodzenia rosnąco':
            dod = 'order by birthDate ASC'
        elif combotext == 'daty urodzenia malejąco':
            dod = 'order by birthDate DESC'
        elif combotext == 'nazwiska od a do z':
            dod = 'order by Surname ASC'
        elif combotext == 'nazwiska od z do a':
            dod = 'order by Surname DESC'
        elif combotext == 'pesel rosnąco':
            dod = 'order by Pesel ASC'
        elif combotext == 'pesel malejąco':
            dod = 'order by Pesel DESC'
        else:
            dod = ''

        self.listWidget.clear()
        cur = connection.cursor()
        if valueFind is not None:
            query = "select Pesel, Surname, Name from patients where Surname = '" + valueFind + "' OR Name = '" + valueFind + "' OR Pesel = '" + valueFind + "' OR City = '" + valueFind + "' OR PostCode = '" + valueFind + "' OR Phone = '" + valueFind + "' OR Street = '" + valueFind + "' OR Mail = '" + valueFind + "'" + dod
        else:
            query = "select Pesel, Surname, Name from patients " + dod
        cur.execute(query)
        value = cur.fetchall()

        queryCount = "select count(Pesel) from patients;"
        cur.execute(queryCount)
        count = cur.fetchall()

        for rowCount in count:
            if(rowCount[0]) == 0:
                self.listWidget.addItem("BRAK DANYCH W BAZIE")
            if (rowCount[0]) != 0:
                for row in value:

                    self.listWidget.addItem(str(row[0]) + " " + str(row[1]) + " " + str(row[2]))


class RegisterVisit(QDialog):
    def __init__(self):
        super(RegisterVisit, self).__init__()
        loadUi('gui/RegisterVisit.ui', self)
        self.saveButton.clicked.connect(self.datechoose)

        cur = connection.cursor()
        queryCount = "select surname, name, specjalization from doctors;"
        cur.execute(queryCount)
        count = cur.fetchall()

        for row in count:
            self.comboBox.addItem(str(row[0]))

    def messagebox(self):
        QMessageBox.information(self, 'Komunikat', 'Podany pesel nie istnieje w bazie')
        self.close()

    def datechoose(self):
        nameDoctor = self.comboBox.currentText()
        cur = connection.cursor()
        query = "select iddoctors from doctors where surname like '" + nameDoctor + "';"
        cur.execute(query)
        idDoctor = cur.fetchall()

        for row1 in idDoctor:
            idDoctor = row1[0]

        choosedata = self.calendarWidget.selectedDate().toString('yyyy-MM-dd')
        pesel = self.lineEdit.text()

        cur = connection.cursor()
        query = "select idpatients from patients where Pesel like '" + pesel + "';"
        cur.execute(query)
        idPatient = cur.fetchall()

        for row2 in idPatient:
            idPatient = row2[0]


        #time = self.timeEdit.time()
        #print(time)

        # Poprawić - wyświetlanie pacjentów
        # Dodawanie wizyty - komunikaty, dodanie godziny wizyty.
        # Ostatni moduł - wyświetl szczegoły wizyty - analogicznie do wyswietlania pacjentow
        # Połączyć tablice - Pesel | Nazwisko | Imię | Data | Godzina | Lekarz
        # table Patients - Pesel, Surname, name
        # table Visit - Date, Time, Doktor (table Doctors)


        print(idPatient)
        print(choosedata)
        print(idDoctor)

        cur = connection.cursor()
        cur.execute("Insert into visit(idDoctor, idPatient, dateVisit) values('" + str(idDoctor) + "', '" + str(idPatient) + "', '" + str(choosedata) + "');")
        connection.commit()


class ShowVisits(QDialog):

    def __init__(self):
        super(ShowVisits, self).__init__()
        loadUi('gui/showVisitsGui.ui', self)
        self.valueFindButton.clicked.connect(self.valueFind)
        self.comboboxButton.clicked.connect(self.comboBoxFilters)

        self.comboBox.addItem("-")
        self.comboBox.addItem("daty urodzenia rosnąco")
        self.comboBox.addItem("daty urodzenia malejąco")
        self.comboBox.addItem("nazwiska od a do z")
        self.comboBox.addItem("nazwiska od z do a")
        self.comboBox.addItem("pesel rosnąco")
        self.comboBox.addItem("pesel malejąco")

        self.listWidget.clear()
        cur = connection.cursor()
        query = "select Pesel, Surname, Name from patients;"
        cur.execute(query)
        value = cur.fetchall()

        queryCount = "select count(Pesel) from patients;"
        cur.execute(queryCount)
        count = cur.fetchall()

        for rowCount in count:
            if(rowCount[0]) == 0:
                self.listWidget.addItem("BRAK DANYCH W BAZIE")
            if (rowCount[0]) != 0:
                for row in value:

                    self.listWidget.addItem(str(row[0]) + " " + str(row[1]) + " " + str(row[2]))

    def valueFind(self):
        self.listWidget.clear()
        valueFind = self.valueFindEditText.text()
        print(valueFind)
        cur = connection.cursor()
        if valueFind is not None:
            query = "select Pesel, Surname, Name from patients where Surname = '" + valueFind + "' OR Name = '" + valueFind + "' OR Pesel = '" + valueFind + "' OR City = '" + valueFind + "' OR PostCode = '" + valueFind + "' OR Phone = '" + valueFind + "' OR Street = '" + valueFind + "' OR Mail = '" + valueFind + "'"
        else:
            query = "select Pesel, Surname, Name from patients"
        cur.execute(query)
        value = cur.fetchall()

        queryCount = "select count(Pesel) from patients;"
        cur.execute(queryCount)
        count = cur.fetchall()

        for rowCount in count:
            if (rowCount[0]) == 0:
                self.listWidget.addItem("BRAK DANYCH W BAZIE")
            if (rowCount[0]) != 0:
                for row in value:
                    self.listWidget.addItem(str(row[0]) + " " + str(row[1]) + " " + str(row[2]))

    def comboBoxFilters(self):
        valueFind = self.valueFindEditText.text()
        combotext = self.comboBox.currentText()
        if combotext == '-':
            dod = ''
        elif combotext == 'daty urodzenia rosnąco':
            dod = 'order by birthDate ASC'
        elif combotext == 'daty urodzenia malejąco':
            dod = 'order by birthDate DESC'
        elif combotext == 'nazwiska od a do z':
            dod = 'order by Surname ASC'
        elif combotext == 'nazwiska od z do a':
            dod = 'order by Surname DESC'
        elif combotext == 'pesel rosnąco':
            dod = 'order by Pesel ASC'
        elif combotext == 'pesel malejąco':
            dod = 'order by Pesel DESC'
        else:
            dod = ''

        self.listWidget.clear()
        cur = connection.cursor()
        if valueFind is not None:
            query = "select Pesel, Surname, Name from patients where Surname = '" + valueFind + "' OR Name = '" + valueFind + "' OR Pesel = '" + valueFind + "' OR City = '" + valueFind + "' OR PostCode = '" + valueFind + "' OR Phone = '" + valueFind + "' OR Street = '" + valueFind + "' OR Mail = '" + valueFind + "'" + dod
        else:
            query = "select Pesel, Surname, Name from patients " + dod
        cur.execute(query)
        value = cur.fetchall()

        queryCount = "select count(Pesel) from patients;"
        cur.execute(queryCount)
        count = cur.fetchall()

        for rowCount in count:
            if(rowCount[0]) == 0:
                self.listWidget.addItem("BRAK DANYCH W BAZIE")
            if (rowCount[0]) != 0:
                for row in value:

                    self.listWidget.addItem(str(row[0]) + " " + str(row[1]) + " " + str(row[2]))



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Login()
    window.setWindowTitle('MedApp')
    window.show()
    sys.exit(app.exec())
