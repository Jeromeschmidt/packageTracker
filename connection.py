#!/usr/bin/python
import mysql.connector
from flask import request
from flask import Flask
from flask import render_template, json
app = Flask(__name__)
cnx = mysql.connector.connect(user='jschmidt', password='x9fvED',
                              host='cse.unl.edu',
                              database='jschmidt')

cursor = cnx.cursor(buffered=True)
query = ("SELECT * FROM Packages")
cursor.execute(query)
for (droneID) in cursor:
    print("{}".format(droneID))

@app.route("/", methods=['GET','POST'])
def home():
    return render_template("index.html")

@app.route("/customer", methods=['GET','POST'])
def customer():
    return render_template("index-customer.html")

@app.route("/staff", methods=['GET','POST'])
def staff():
    return render_template("index-staff.html")

# This part is for dropping off the package (Staff)
@app.route("/dropPackage")
def dropPackage():
    return render_template("index-staff-drop-package.html")

@app.route("/dropPackage", methods=['POST'])
def dropPackagepost():
    if request.method == 'POST':
        droneID = request.form['did']
        droneIDtable = droneID.upper()
        packageID = request.form['pid']
        packageIDtable = packageID.upper()
        timeOfDelivery = request.form['time']
        timeOfDeliverytable = timeOfDelivery.upper()
        query = ("UPDATE Packages SET TimeDelivered = \"{}\" WHERE PackageID = \"{}\"".format(timeOfDeliverytable, packageIDtable))
        cursor.execute(query)
        cnx.commit()

        query = ("UPDATE Packages SET DroneID = NULL WHERE PackageID = \"{}\"".format(packageIDtable))
        cursor.execute(query)
        cnx.commit()
        return "The package# {} has been dropped off at its destination".format(packageID)

# This part is for picking up the package (Staff)
@app.route("/pickUpPackage")
def pickUpPackage():
    return render_template("index-staff-pick-up-package.html")

@app.route("/pickUpPackage",methods=['POST'])
def pickUpPackagepost():
    if request.method == 'POST':
        droneID = request.form['did']
        droneIDtable = droneID.upper()
        packageID = request.form['pid']
        packageIDtable = packageID.upper()
        timeOfDispatchment = request.form['time']
        timeOfDispatchmenttable = timeOfDispatchment.upper()

        query = ("SELECT * FROM Packages WHERE DroneID = \"{}\"".format(droneIDtable))
        cursor.execute(query)
        cursor.fetchall()
        rowcount = cursor.rowcount

        query = ("SELECT * FROM Drones WHERE DroneID=\"{}\"".format(droneIDtable))
        cursor.execute(query)
        rows = cursor.fetchall()

        if rows[0][2] == 1:
            return "The drone {} is a MongoDrone, please use the MongoDrone interface for picking up packages with this drone!".format(droneIDtable)
        if rowcount > 0:
            return "You already have a package aboard {}, please drop this package off before attempting to pick up another one!".format(droneIDtable)
        else:
            query = ("UPDATE Packages SET TimePickedUp = \"{}\" WHERE PackageID = \"{}\"".format(timeOfDispatchmenttable, packageIDtable))
            cursor.execute(query)
            cnx.commit()
            query = ("UPDATE Packages SET DroneID = \"{}\" WHERE PackageID = \"{}\"".format(droneIDtable, packageIDtable))
            cursor.execute(query)
            cnx.commit()
            return "A drone has been sent to pick up the package# {}".format(packageIDtable)

@app.route("/mongoPackage")
def mongoPackage():
    return render_template("index-staff-pick-up-package-mongoD.html")

@app.route("/mongoPackage",methods=['POST'])
def mongoPackagepost():
    if request.method == 'POST':
        droneID = request.form['did']
        droneIDtable = droneID.upper()
        packageIDFirst = request.form['fpid']
        packageIDFirsttable = packageIDFirst.upper()
        packageIDSecond = request.form['spid']
        packageIDSecondtable = packageIDSecond.upper()
        packageIDThird = request.form['tpid']
        packageIDThirdtable = packageIDThird.upper()
        timeOfDispatchment = request.form['time']
        timeOfDispatchmenttable = timeOfDispatchment.upper()

        query = ("SELECT * FROM Packages WHERE DroneID = \"{}\"".format(droneIDtable))
        cursor.execute(query)
        cursor.fetchall()
        rowcount = cursor.rowcount

        query = ("SELECT * FROM Drones WHERE DroneID=\"{}\"".format(droneIDtable))
        cursor.execute(query)
        rows = cursor.fetchall()

        if rows[0][2] == 0:
            return "The drone {} is a regular drone, not a MongoDrone! Please use the regular drone interface for picking up packages with this drone!".format(droneIDtable)
        if rowcount >= 3:
            return "You have {} packages aboard {}, please drop some packages off before attempting to pick up any more!".format(rowcount, droneIDtable)
        elif rowcount == 2 and packageIDSecondtable:
            return "You have 2 packages aboard {}, please drop at least 1 of these packages off before attempting to pick up 2 more!".format(droneIDtable)
        elif rowcount == 1 and packageIDThirdtable:
            return "You have a package aboard {}, please drop this package off before attempting to pick up 3 more!".format(droneIDtable)
        else:
            query = ("UPDATE Packages SET TimePickedUp = \"{}\" WHERE PackageID = \"{}\"".format(timeOfDispatchmenttable, packageIDFirsttable))
            cursor.execute(query)
            cnx.commit()
            query = ("UPDATE Packages SET TimePickedUp = \"{}\" WHERE PackageID = \"{}\"".format(timeOfDispatchmenttable, packageIDSecondtable))
            cursor.execute(query)
            cnx.commit()
            query = ("UPDATE Packages SET TimePickedUp = \"{}\" WHERE PackageID = \"{}\"".format(timeOfDispatchmenttable, packageIDThirdtable))
            cursor.execute(query)
            cnx.commit()
            query = ("UPDATE Packages SET DroneID = \"{}\" WHERE PackageID = \"{}\"".format(droneIDtable, packageIDFirsttable))
            cursor.execute(query)
            cnx.commit()
            query = ("UPDATE Packages SET DroneID = \"{}\" WHERE PackageID = \"{}\"".format(droneIDtable, packageIDSecondtable))
            cursor.execute(query)
            cnx.commit()
            query = ("UPDATE Packages SET DroneID = \"{}\" WHERE PackageID = \"{}\"".format(droneIDtable, packageIDThirdtable))
            cursor.execute(query)
            cnx.commit()
            return "A MongoDrone has been sent to pick up the packages {} {} {}.".format(packageIDFirsttable, packageIDSecondtable, packageIDThirdtable)

# This part is for checking the information of the package (Staff)
@app.route("/checkPackageStaff")
def checkPackageStaff():
    return render_template("index-staff-check-package-info.html")

@app.route("/checkPackageStaff", methods=['POST'])
def checkPackageStaffpost():
     if request.method == 'POST':
      packageID = request.form['packageID']
      packageIDTable = packageID.upper()
      query = ("SELECT * FROM Packages WHERE PackageID=\"{}\"".format(packageIDTable))
      cursor.execute(query)
      rows = cursor.fetchall()
      # print(rows[0][0])
      # return "SUCCESS"
      return "The Customer {} {}'s package contains {}".format(rows[0][6],rows[0][7],rows[0][3])

# This part is for checking the status of the package (Staff)
@app.route("/checkStatusStaff")
def checkStatusStaff():
    return render_template("index-staff-check-status.html")

@app.route("/checkStatusStaff", methods=['POST'])
def checkStatusStaffpost():
    if request.method == 'POST':
        packageID = request.form['pid']
        packageIDTable = packageID.upper()
        query = ("SELECT * FROM Packages WHERE PackageID=\"{}\"".format(packageIDTable))
        cursor.execute(query)
        rows = cursor.fetchall()
        if rows[0][8] is None:
          return "The customer {} {}'s package {} has not left the " \
                 "warehouse".format(rows[0][6], rows[0][7], rows[0][3])

        elif rows[0][9] is None:
          return "The customer {} {}'s package {} is in transit aboard the drone {} as " \
                 "of {}{}".format(rows[0][6], rows[0][7], rows[0][3], rows[0][5], rows[0][8], rows[0][10])

        else:
          return "The customer {} {}'s package {} was picked up from {} at {}{}" \
             ", and delivered to {} at {}".format(rows[0][6], rows[0][7], rows[0][3], rows[0][1],rows[0][8], rows[0][10],rows[0][2],rows[0][9])

# This part is for dispatching the drone (Staff)
@app.route("/dispatchDroneStaff")
def dispatchDroneStaff():
    return render_template("index-staff-dispatch-drone.html")

@app.route("/dispatchDroneStaff", methods=['POST'])
def dispatchDroneStaffpost():
    if request.method == 'POST':
        droneID = request.form['droneid']
        droneIDtable = droneID.upper()
        to = request.form['to']
        totable = to.upper()
        timeOfDispatchment = request.form['time']
        timeOfDispatchmenttable = timeOfDispatchment.upper()

        query = ("UPDATE Drones SET DepotID = \"{}\" WHERE DroneID = \"{}\"".format(totable, droneIDtable))
        cursor.execute(query)
        cnx.commit()

        query = ("SELECT * FROM Packages WHERE DroneID=\"{}\"".format(droneIDtable))
        cursor.execute(query)
        rows = cursor.fetchall()

        numPackages = len(rows)
        i = 0
        while i < numPackages:
            newVisit = ", moved to {} at {}".format(totable, timeOfDispatchmenttable)
            if rows[i][10] is None:
                newPackageVisitations = newVisit
            else:
                currentPackageVisitations = rows[i][10]
                newPackageVisitations = currentPackageVisitations + newVisit

            query = ("UPDATE Packages SET PackageVisited = \"{}\" WHERE PackageID = \"{}\"".format(newPackageVisitations, rows[i][0]))
            cursor.execute(query)
            cnx.commit()
            i+=1

        return "{} has been dispatched to {} at current time {}.".format(droneIDtable, totable, timeOfDispatchmenttable)

# This part is for checking the delivery status of the package (Customer)
@app.route("/deliveryStatusCustomer")
def deliveryStatusCustomer():
    return render_template("index-customer-delivery-status.html")

@app.route("/deliveryStatusCustomer", methods=['POST'])
def deliveryStatusCustomerpost():
    if request.method == 'POST':
      packageID = request.form['packageID']
      packageIDTable = packageID.upper()
      query = ("SELECT * FROM Packages WHERE PackageID=\"{}\"".format(packageIDTable))
      cursor.execute(query)

      rows = cursor.fetchall()
      if rows[0][8] is None:
          return "{} {}, your package {} has not left the " \
                 "warehouse".format(rows[0][6], rows[0][7], rows[0][3])

      elif rows[0][9] is None:
          return "{} {} ,your package {} is in transit as " \
                 "of {}".format(rows[0][6], rows[0][7], rows[0][3], rows[0][8])

      else:
           return "{} {}, your package {} was picked up from {} at {}" \
             " and delivered to {} at {}".format(rows[0][6], rows[0][7], rows[0][3], rows[0][1],rows[0][8],rows[0][2],rows[0][9])

# This part is for ordering a delivery request (Customer)
@app.route("/orderDeliveryRequestCustomer")
def orderDeliveryRequestCustomer():
    return render_template("index-order-delivery-request.html")

@app.route("/orderDeliveryRequestCustomer", methods=['POST'])
def orderDeliveryRequestCustomerpost():
    if request.method == 'POST':
        firstName = request.form['fname']
        firstNameTable = firstName.upper()
        lastName = request.form['lname']
        lastNameTable = lastName.upper()
        origin = request.form['origin']
        originTable = origin.upper()
        to = request.form['dest']
        totable = to.upper()
        contents = request.form['contents']
        contentsTable = contents.upper()
        query = ("INSERT INTO Packages (OriginAddress, DeliveryAddress, PackageName, FirstName, LastName) VALUES (\"{}\",\"{}\",\"{}\",\"{}\",\"{}\")".format(originTable,totable,
                                                                                                                                                              contentsTable,firstNameTable,lastNameTable))
        cursor.execute(query)
        cnx.commit()
        cursor.execute("SELECT FirstName, COUNT(*) FROM Packages WHERE FirstName = \"{}\"".format(firstNameTable))
        row_count = cursor.rowcount
        print("Number of affected rows: {}".format(row_count))
        if row_count == 0 and row_count < 0:
            return "Could not order a delivery request"
        else:
            return "Order successfully placed"

if __name__ == "__main__":
    app.run(debug=True)
    request.get_json(force=True)

cursor.close()
cnx.close()
