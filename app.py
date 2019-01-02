
from flask import Flask,request,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, \
    login_user, logout_user, current_user, login_required
import datetime

app = Flask(__name__ , static_url_path='/static')
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database.db'
db = SQLAlchemy(app)




class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    logs = db.relationship("LogItem", backref="user")

class LogItem(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    Date = db.Column(db.String, nullable=False)
    AircraftType = db.Column(db.String)
    AircraftIdent = db.Column(db.String)
    From = db.Column(db.String(4))
    To = db.Column(db.String(4))
    Takeoff = db.Column(db.Integer)
    landings = db.Column(db.Integer)
    FlightTime = db.Column(db.String)
    Remks = db.Column(db.String)
    UserId = db.Column(db.Integer, db.ForeignKey('user.id'))

app.config['SECRET_KEY'] = 'Welcome'
login_manager = LoginManager(app)
login_manager.init_app(app)

@login_manager.user_loader
def load_user(uid):
    user = User.query.get(uid)
    return user


@app.route('/login', methods=["POST"])
def login():
    Logusername = request.form['Username']
    password = request.form['Password']
    Logger = User.query.filter_by(username=Logusername).first()
    if(Logger != None):
        LogPass = Logger.password
        if(LogPass == password):
            login_user(Logger)

            id = current_user.id

            Date = []
            AirType = []
            AirIden = []
            Dep = []
            Arr = []
            NoT = []
            NoL = []
            Time = []
            remarks = []
            Did = []
            outList = list(LogItem.query.filter_by(UserId=id))

            for item in outList:
                Date.append(item.Date)
                AirType.append(item.AircraftType)
                AirIden.append(item.AircraftIdent)
                Dep.append(item.From)
                Arr.append(item.To)
                NoT.append(item.Takeoff)
                NoL.append(item.landings)
                Time.append(item.FlightTime)
                remarks.append(item.Remks)
                Did.append(item.Id)

            return render_template("Logbook.html", data=outList, Date=Date, AirType=AirType, AirIden=AirIden, Dep=Dep,
                                   Arr=Arr
                                   , NoT=NoT, NoL=NoL, Time=Time, remarks=remarks, Did=Did)


        else:
            return render_template("account.html", Message="Incorrect Login Information/Account dosen't exist")
    return render_template("index.html")

@app.route('/createUser', methods=['POST'])
def CreateUser():
    username = request.form['Username']
    name = request.form['Name']
    password = request.form['Password']
    VerifyPassword = request.form['PassVerify']
    if(password == VerifyPassword):
        from app import db, User
        user = User(username=username, name = name, password = password)
        db.session.add(user)
        db.session.commit()
        login_user(user)

        id = current_user.id

        Date = []
        AirType = []
        AirIden = []
        Dep = []
        Arr = []
        NoT = []
        NoL = []
        Time = []
        remarks = []
        Did = []
        outList = list(LogItem.query.filter_by(UserId=id))

        for item in outList:
            Date.append(item.Date)
            AirType.append(item.AircraftType)
            AirIden.append(item.AircraftIdent)
            Dep.append(item.From)
            Arr.append(item.To)
            NoT.append(item.Takeoff)
            NoL.append(item.landings)
            Time.append(item.FlightTime)
            remarks.append(item.Remks)
            Did.append(item.Id)

        return render_template("Logbook.html", data=outList, Date=Date, AirType=AirType, AirIden=AirIden, Dep=Dep,
                               Arr=Arr
                               , NoT=NoT, NoL=NoL, Time=Time, remarks=remarks, Did=Did)

    else:
        return render_template("account.html", username = username, name = name, CreateMessage="Passwords dont match")

@app.route("/createLog", methods=['POST'])
@login_required
def createLog():
    Date = request.form["Date"]
    AirType = request.form['AirType']
    AirIden = request.form['AirIdent']
    Dep = request.form['From']
    Arr = request.form['To']
    NoT = request.form['Takeoff']
    NoL = request.form['Landing']
    Time = request.form['FlightTime']
    remarks = request.form['Rmk']

    from app import db, User, LogItem

    item = LogItem(Date = Date, AircraftType=AirType, AircraftIdent=AirIden,
                   From=Dep,To=Arr,Takeoff=NoT,landings=NoL,FlightTime=Time,Remks= remarks)

    item.UserId
    user = current_user
    item.UserId = current_user.id

    db.session.add(item)
    db.session.commit()

    id = current_user.id

    Date = []
    AirType = []
    AirIden = []
    Dep = []
    Arr = []
    NoT = []
    NoL = []
    Time = []
    remarks = []
    Did = []
    outList = list(LogItem.query.filter_by(UserId=id))

    for item in outList:
        Date.append(item.Date)
        AirType.append(item.AircraftType)
        AirIden.append(item.AircraftIdent)
        Dep.append(item.From)
        Arr.append(item.To)
        NoT.append(item.Takeoff)
        NoL.append(item.landings)
        Time.append(item.FlightTime)
        remarks.append(item.Remks)
        Did.append(item.Id)

    return render_template("Logbook.html", data=outList, Date=Date, AirType=AirType, AirIden=AirIden, Dep=Dep, Arr=Arr
                           , NoT=NoT, NoL=NoL, Time=Time, remarks=remarks, Did=Did)



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template("index.html", message="You have been logged out")

@app.route("/NavAcc")
def NavAcc():
    return render_template("account.html")

@app.route("/NavLog")
@login_required
def viewlog():
    id = current_user.id

    Date = []
    AirType =[]
    AirIden = []
    Dep = []
    Arr = []
    NoT = []
    NoL = []
    Time = []
    remarks = []
    Did = []
    outList = list(LogItem.query.filter_by(UserId=id))

    for item in outList:
        Date.append(item.Date)
        AirType.append(item.AircraftType)
        AirIden.append(item.AircraftIdent)
        Dep.append(item.From)
        Arr.append(item.To)
        NoT.append(item.Takeoff)
        NoL.append(item.landings)
        Time.append(item.FlightTime)
        remarks.append(item.Remks)
        Did.append(item.Id)

    return render_template("Logbook.html", data=outList, Date=Date, AirType = AirType, AirIden = AirIden, Dep = Dep, Arr = Arr
                           , NoT = NoT, NoL = NoL, Time=Time, remarks=remarks, Did = Did)

@app.route("/Delete", methods=["POST"])
def Delete():
        Did = request.form["Ident"]
        print(Did)

        remove = LogItem.query.filter_by(Id=Did).first()
        db.session.delete(remove)
        db.session.commit()

        id = current_user.id

        Date = []
        AirType = []
        AirIden = []
        Dep = []
        Arr = []
        NoT = []
        NoL = []
        Time = []
        remarks = []
        Did = []
        outList = list(LogItem.query.filter_by(UserId=id))

        for item in outList:
            Date.append(item.Date)
            AirType.append(item.AircraftType)
            AirIden.append(item.AircraftIdent)
            Dep.append(item.From)
            Arr.append(item.To)
            NoT.append(item.Takeoff)
            NoL.append(item.landings)
            Time.append(item.FlightTime)
            remarks.append(item.Remks)
            Did.append(item.Id)

        return render_template("Logbook.html", data=outList, Date=Date, AirType=AirType, AirIden=AirIden, Dep=Dep,
                               Arr=Arr
                               , NoT=NoT, NoL=NoL, Time=Time, remarks=remarks, Did=Did)

@app.route('/Update', methods=["POST"])
def Update():
    Did = request.form["Ident"]
    update = LogItem.query.filter_by(Id=Did).first()
    Date = update.Date
    AirType = update.AircraftType
    AirIden = update.AircraftIdent
    Dep = update.From
    Arr = update.To
    NoT = update.Takeoff
    NoL = update.landings
    Time = update.FlightTime
    Rmks = update.Remks


    return render_template("Update.html", Date=Date, AirType=AirType, AirIden=AirIden, Dep=Dep,
                               Arr=Arr, NoT=NoT, NoL=NoL, Time=Time, remarks=Rmks, Did=Did)
@app.route("/DBUpdate" , methods=["POST"])
@login_required
def DBUpdate():


    ident = request.form["ident"]
    Date = request.form["Date"]
    AirType = request.form['AirType']
    AirIden = request.form['AirIdent']
    Dep = request.form['From']
    Arr = request.form['To']
    NoT = request.form['Takeoff']
    NoL = request.form['Landing']
    Time = request.form['FlightTime']
    remarks = request.form['Rmk']

    update = LogItem.query.filter_by(Id=ident).first()

    update.Date = Date
    update.AircraftType = AirType
    update.AircraftIdent = AirIden
    update.From = Dep
    update.To = Arr
    update.Takeoff = NoT
    update.landings = NoL
    update.Time = Time
    update.Remks = remarks

    id = current_user.id

    db.session.commit()
    Date = []
    AirType = []
    AirIden = []
    Dep = []
    Arr = []
    NoT = []
    NoL = []
    Time = []
    remarks = []
    Did = []
    outList = list(LogItem.query.filter_by(UserId=id))

    for item in outList:
        Date.append(item.Date)
        AirType.append(item.AircraftType)
        AirIden.append(item.AircraftIdent)
        Dep.append(item.From)
        Arr.append(item.To)
        NoT.append(item.Takeoff)
        NoL.append(item.landings)
        Time.append(item.FlightTime)
        remarks.append(item.Remks)
        Did.append(item.Id)

    return render_template("Logbook.html", data=outList, Date=Date, AirType=AirType, AirIden=AirIden, Dep=Dep,
                           Arr=Arr, NoT=NoT, NoL=NoL, Time=Time, remarks=remarks, Did=Did)




@app.route("/NavCross")
def NavCross():
    return render_template("CrosswindCal.html")

@app.route("/NavCreLog", methods=["POST"])
@login_required
def NavCreLog():
    return render_template("CreateLog.html")


@app.errorhandler(404)
def err404(err):
    return render_template('404.html',err=err)

@app.errorhandler(400)
def err400(err):
    return render_template('400.html',err=err)

@app.errorhandler(401)
def err401(err):
    return render_template('401.html',err=err)

@app.errorhandler(403)
def err403(err):
    return render_template('403.html',err=err)

@app.errorhandler(502)
def err502(err):
    return render_template('502.html',err=err)

@app.route('/')
def hello_world():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)
