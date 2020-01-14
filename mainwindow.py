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
        self.backgroundLabel.setPixmap(QPixmap("image/logo.PNG"))

    def accepted(self):
        self.mW.show()

    def messagebox(self):
        QMessageBox.warning(self, 'Komunikat', 'Podane dane są nieprawidłowe lub nie istnieją w bazie.')

    def messagebox_emptyscope(self):
        QMessageBox.warning(self, 'Komunikat', 'Wszystkie pola muszą być uzupełnione.')

    def checkData(self):

        login = self.loginEditLine.text()
        password = self.passwordEditLine.text()

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
                cur.close()
                self.close()

            if countlogin == 0:
                self.messagebox()
                self.loginEditLine.setText("")
                self.passwordEditLine.setText("")


        else:
            self.messagebox_emptyscope()
            self.loginEditLine.setText("")
            self.passwordEditLine.setText("")


class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi('gui/mainWindowGui.ui', self)
        self.registerPatientButton.clicked.connect(self.patient)
        self.registerUserButton.clicked.connect(self.register)
        self.endButton.clicked.connect(self.end)
        self.showPatientsButton.clicked.connect(self.showPatients)
        self.registerVisitButton.clicked.connect(self.registervisit)
        self.addDoctorButton.clicked.connect(self.addDoctor)
        self.showVisitButton.clicked.connect(self.showVisit)
        self.widget.setPixmap(QPixmap("image/logo1.PNG"))
        self.p = Patients()
        self.r = Register()
        self.s = ShowPatients()
        self.w = RegisterVisit()
        self.d = AddDoctor()
        self.sv = ShowVisits()

    def showVisit(self):
        self.sv.show()

    def addDoctor(self):
        self.d.show()

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
        loadUi('gui/registerPatientGui.ui', self)
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

    def messageboxEmpty(self):
        QMessageBox.information(self, 'Komunikat', 'Muszą zostać uzupełnione wszystkie wymagane pola.')

    def insertToDatabase(self):
        name = self.nameEditText.text()
        print(name)
        surname = self.surnameEditText.text()
        print(surname)
        pesel = self.peselEditText.text()
        print(pesel)
        birthdate = self.birthDateEditText.text()
        print(birthdate)
        street = self.streetEditText.text()
        print(street)
        houseNumer = self.houseNumerEditText.text()
        print(houseNumer)
        flat = self.numberFlatEditText.text()
        print(flat)
        city = self.cityEditText.text()
        print(city)
        postCode = self.postCodeEditText.text()
        print(postCode)
        phone = self.phoneEditText.text()
        print(phone)
        email = self.emailEditText.text()
        print(email)
        nameAuthorizedPerson = self.nameAuthorizedPersonEditText.text()
        print(nameAuthorizedPerson)
        surnameAuthorizedPerson = self.surnameAuthorizedPersonEditText.text()
        print(surnameAuthorizedPerson)
        peselAuthorizedPerson = self.peselAuthorizedPersonEditText.text()
        print(peselAuthorizedPerson)
        phoneAuthorizedPerson = self.phoneAuthorizedPersonEditText.text()
        print(phoneAuthorizedPerson)

        if self.womanRadioButton.isChecked():
            sex = 'kobieta'
        elif self.menRadioButton.isChecked():
            sex = 'mężczyzna'

        dane = [name, surname, pesel, birthdate, street, houseNumer, flat, city, postCode, phone, email,
                nameAuthorizedPerson, surnameAuthorizedPerson, peselAuthorizedPerson, phoneAuthorizedPerson, sex]

        empty = 0
        for x in dane:
            if x != "":
                empty = 1
            else:
                empty = 2

        if name and surname and pesel != '':
         if empty == 1:
                    cur = connection.cursor()
                    cur.execute(
                    "Insert into patients(Name, Surname, Pesel, BirthDate, Street, House, Flat, City, PostCode, Phone, Mail, NameAuthorizedPerson, SurnameAuthorizedPerson, PeselAuthorizedPerson, PhoneAuthorizedPerson, Sex) values('" + name + "', '" + surname + "', '" + pesel + "', '" + birthdate + "', '" + street + "', '" + houseNumer + "', '" + flat + "', '" + city + "', '" + postCode + "', '" + phone + "', '" + email + "', '" + nameAuthorizedPerson + "', '" + surnameAuthorizedPerson + "', '" + peselAuthorizedPerson + "', '" + phoneAuthorizedPerson + "', '" + sex + "')")
                    connection.commit()
                    self.messagebox()
                    self.nameEditText.setText("")
                    self.surnameEditText.setText("")
                    self.peselEditText.setText("")
                    self.streetEditText.setText("")
                    self.houseNumerEditText.setText("")
                    self.numberFlatEditText.setText("")
                    self.cityEditText.setText("")
                    self.postCodeEditText.setText("")
                    self.phoneEditText.setText("")
                    self.emailEditText.setText("")
                    self.nameAuthorizedPersonEditText.setText("")
                    self.surnameAuthorizedPersonEditText.setText("")
                    self.peselAuthorizedPersonEditText.setText("")
                    self.phoneAuthorizedPersonEditText.setText("")

        else:
            self.messageboxEmpty()


class Register(QDialog):

    def __init__(self):
        super(Register, self).__init__()
        loadUi('gui/registerUserGui.ui', self)
        self.registerButton.clicked.connect(self.register)
        self.cancelButton.clicked.connect(self.cancel)

    def cancel(self):
        buttonReply = QMessageBox.question(self, 'Question', "Czy napewno chcesz anulować rejestrację użytkownika?",
                                           QMessageBox.Yes | QMessageBox.No,
                                           QMessageBox.Yes)
        if buttonReply == QMessageBox.Yes:
            self.close()
            self.userNameEditText.setText("")
            self.passwordEditText.setText("")
            self.passwordAgainEditText.setText("")

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
                    self.userNameEditText.setText("")
                    self.passwordEditText.setText("")
                    self.passwordAgainEditText.setText("")

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
        self.valueFindComboboxButton.clicked.connect(self.comboBoxFilters)
        self.closeButton.clicked.connect(self.closeWindow)

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
            if (rowCount[0]) == 0:
                self.listWidget.addItem("BRAK DANYCH W BAZIE")
            if (rowCount[0]) != 0:
                for row in value:
                    self.listWidget.addItem(str(row[0]) + " " + str(row[1]) + " " + str(row[2]))

    def valueFind(self):
        self.listWidget.clear()
        valueFind = self.valueFindEditText.text()
        print(valueFind)
        cur = connection.cursor()
        if valueFind == "":
            query = "select Pesel, Surname, Name from patients;"
        else:
            query = "select Pesel, Surname, Name from patients where Surname = '" + valueFind + "' OR Name = '" + valueFind + "' OR Pesel = '" + valueFind + "' OR City = '" + valueFind + "' OR PostCode = '" + valueFind + "' OR Phone = '" + valueFind + "' OR Street = '" + valueFind + "' OR Mail = '" + valueFind + "'"
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

    def closeWindow(self):
        self.close()
        self.valueFindEditText.setText("")

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
        if valueFind == "":
            query = "select Pesel, Surname, Name from patients " + dod
        else:
            query = "select Pesel, Surname, Name from patients where Surname = '" + valueFind + "' OR Name = '" + valueFind + "' OR Pesel = '" + valueFind + "' OR City = '" + valueFind + "' OR PostCode = '" + valueFind + "' OR Phone = '" + valueFind + "' OR Street = '" + valueFind + "' OR Mail = '" + valueFind + "'" + dod

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


class RegisterVisit(QDialog):
    def __init__(self):
        super(RegisterVisit, self).__init__()
        loadUi('gui/registerVisitGui.ui', self)
        self.saveButton.clicked.connect(self.datechoose)
        self.cancelButton.clicked.connect(self.closeWindow)

        cur = connection.cursor()
        queryCount = "select surname, name, specjalization from doctors;"
        cur.execute(queryCount)
        count = cur.fetchall()

        for row in count:
            self.comboBox.addItem(str(row[0]))

    def closeWindow(self):
        buttonReply = QMessageBox.question(self, 'Question', "Czy napewno chcesz anulować?",
                                           QMessageBox.Yes | QMessageBox.No,
                                           QMessageBox.Yes)
        if buttonReply == QMessageBox.Yes:
            self.close()

    def messageboxEmptyPatient(self):
        QMessageBox.information(self, 'Komunikat', 'Podany pesel nie istnieje w bazie.')

    def messageboxEmptyPesel(self):
        QMessageBox.information(self, 'Komunikat', 'Pole Pesel nie może być puste.')

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
        time = self.timeEdit.time().toString()

        cur = connection.cursor()
        query = "select idpatients from patients where Pesel like '" + pesel + "';"
        cur.execute(query)
        idPatient = cur.fetchall()

        for row2 in idPatient:
            idPatient = row2[0]
        if str(idPatient) == '[]':
            self.messageboxEmptyPatient()
        else:
            if pesel != "":
                cur = connection.cursor()
                cur.execute("Insert into visitt(iddoctor, idpatient, date, time) values('" + str(idDoctor) + "', '" + str(idPatient) + "', '" + str(choosedata) + "', '" + str(time) + "');")
                connection.commit()
                QMessageBox.information(self, 'Komunikat', 'Wizyta w dniu ' + str(choosedata) + ' o godzinie ' + str(time) + ' dodana poprawnie.')
                self.close()
                self.lineEdit.setText("")
            else:
                self.messageboxEmptyPesel()


class AddDoctor(QDialog):
    def __init__(self):
        super(AddDoctor, self).__init__()
        loadUi('gui/addDoctorGui.ui', self)
        self.registerButton.clicked.connect(self.register)
        self.cancelButton.clicked.connect(self.cancel)

    def messageboxEmpty(self):
        QMessageBox.information(self, 'Komunikat', 'Pola nie mogą być puste.')

    def register(self):
        name = self.doctorNameEditText.text()
        surname = self.doctorSurnameEditText.text()
        specjalization = self.doctorSpecjalizationEditText.text()
        if name and surname and specjalization != '':
            cur = connection.cursor()
            cur.execute("Insert into doctors(name, surname, specjalization) values('" + name + "', '" + surname + "', '" + specjalization + "')")
            connection.commit()
            QMessageBox.information(self, 'Komunikat', 'Doktor ' + str(surname) + ' ' + str(name) + ' został/a poprawnie dodany.')
            self.close()
            self.doctorNameEditText.setText("")
            self.doctorSurnameEditText.setText("")
            self.doctorSpecjalizationEditText.setText("")
        else:
            self.messageboxEmpty()

    def cancel(self):
        buttonReply = QMessageBox.question(self, 'Question', "Czy napewno chcesz anulować operację dodawania lekarza?",
                                           QMessageBox.Yes | QMessageBox.No,
                                           QMessageBox.Yes)
        if buttonReply == QMessageBox.Yes:
            self.close()
            self.doctorNameEditText.setText("")
            self.doctorSurnameEditText.setText("")
            self.doctorSpecjalizationEditText.setText("")


class ShowVisits(QDialog):

    def __init__(self):
        super(ShowVisits, self).__init__()
        loadUi('gui/showVisitsGui.ui', self)
        self.closeButton.clicked.connect(self.closeWindow)
        self.valueFindButton.clicked.connect(self.comboBoxFilters)
        self.comboBox.addItem("Lekarzy")
        self.comboBox.addItem("Pacjentów")
        self.listWidget.clear()

    def messageboxEmpty2(self):
        QMessageBox.information(self, 'Komunikat', 'Brak danych w bazie.')

    def comboBoxFilters(self):

        filter = self.EditText.text()
        combotext = self.comboBox.currentText()
        date1 = self.dateEdit.text()
        date2 = self.dateEdit_2.text()

        if combotext == 'Lekarzy':
            dod = 'd.surname'
        elif combotext == 'Pacjentów':
            dod = 'p.Pesel'

        self.listWidget.clear()
        cur = connection.cursor()
        query="SELECT p.Name, p.Surname, p.Pesel, d.name, d.surname, v.date, v.time  FROM patients p join visitt v on p.idpatients=v.idpatient join doctors d on d.iddoctors=v.iddoctor where " + dod + " = '" + filter + "' and v.date between '" + date1 + "' and '" + date2 + "';"
        cur.execute(query)
        value = cur.fetchall()

        queryCount = "select count(idvisitt) FROM patients p join visitt v on p.idpatients=v.idpatient join doctors d on d.iddoctors=v.iddoctor where " + dod + " = '" + filter + "' and v.date between '" + date1 + "' and '" + date2 + "';"
        cur.execute(queryCount)
        count = cur.fetchall()

        for rowCount in count:
            if (rowCount[0]) == 0:
                self.messageboxEmpty2()
            elif (rowCount[0]) != 0:
                for row in value:
                    self.listWidget.addItem(str(row[0]) + " " + str(row[1]) + " " + str(row[2]) + " " + str(row[3]) + " " + str(row[4]) + " " + str(row[5]) + " " + str(row[6]))

    def closeWindow(self):
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Login()
    window.setWindowTitle('MedApp')
    window.show()
    sys.exit(app.exec())

