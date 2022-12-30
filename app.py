# DELETE LATER
# note to self: household budgeting api
# several accounts, family main account, family members as users
# can add money to balance - add
# can pay money out of balance - transfer
# check balance - balance
# can take loan from parents/family account - takeloan
# debt vs cash, changes update both
# register account
# make payments on loan - payloan
# verify if enough money in account before payment completes

# parameters
# login/reg - username, password
# add - username, password, amount to be added
# transfer - username, password, username of person receiving money, amount to be paid
# balance - username, password
# takeloan - username, password, amount of loan
# payloan - username, password, amount to be deducted from loan due

# method
# get info from server
# post info to server

# status codes
# 200 success
# invalid user/pwd 301/302
# 303 insufficient funds
# 304 invalid monetary input (neg)

# flask, mongo, bcrypt
# revisit
from flask import Flask, render_template, url_for, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt

########################################################################
app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.MoneyManagementDB
users = db["Users"]
########################################################################


########################################################################

# note to self: register account
# define UserExist: name of account, verify input
def UserExist(username):
    if users.find({"Username":username}).count() == 0:
        return False
    else:
        return True

# class Register: post to server
# input data(json), username, password
class Register(Resource):
    def post(self):
        postedData = request.get_json()
        username = postedData["Username"]
        password = postedData["Password"]
# if username exists, status, error message        
        if UserExist(username):
            retJson = {
                'Status':301,
                'Message': 'Invalid Username'
            }
            return jsonify(retJson)
# password not visible
        hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
# user input: username, password, balance, debt
        users.insert({
            "Username": username,
            "Password": hashed_pw,
            "Current Balance":0,
            "Money Currently Owed":0
        })
        retJson = {
            "status": 200,
            "msg": "You are now registered."
        }
        return jsonify(retJson)
########################################################################

# authroization
# verify password, match to username
def verifyPw(username, password):
    if not UserExist(username):
        return False
    hashed_pw = users.find({
        "Username":username
    })[0]["Password"]
    if bcrypt.hashpw(password.encode('utf8'), hashed_pw) == hashed_pw:
        return True
    else:
        return False

########################################################################

# define current balance
def balanceUser(username):
    cash = users.find({
        "Username":username
    })[0]["Current Balance"]
    return cash

# define money owed
def debtUser(username):
    debt = users.find({
        "Username":username
    })[0]["Amount Currently Owed"]
    return debt

########################################################################

# return resulting status/msg as json, display
def genReturnDict(status, msg):
    retJson = {
        "Status": status,
        "Message": msg
    }
    return retJson

########################################################################

# verify username and password
# if true invalid username
# if false wrong pwd
def verifyCred(username, password):
    if not UserExist(username):
        return genReturnDict(301, "Invalid Username"), True
    correct_pw = verifyPw(username, password)
    if not correct_pw:
        return genReturnDict(302, "Incorrect Password"), True
    return None, False

########################################################################

# update user account balance
# use later for transfers in/out
def updateAccount(username, balance):
    users.update({
        "Username": username
    },{
        "$set":{
            "Current Balance": balance
        }
    })

########################################################################

# update user account money owed
# use later for payments on loans etc. 
def updateDebt(username, balance):
    users.update({
        "Username": username
    },{
        "$set":{
            "Money Currently Owed": balance
        }
    })

########################################################################

# classes
# add, transfer, balance, takeloan, payloan

# add -> post to server
# input username/pwd/amount, verify input
class Add(Resource):
    def post(self):
        postedData = request.get_json()
        username = postedData["Username"]
        password = postedData["Password"]
        money = postedData["Amount to be Added"]
        retJson, error = verifyCred(username, password)
# error if money less than zero
        if error:
            return jsonify(retJson)
        if money<=0:
            return jsonify(genReturnDict(304, "Please enter an amount greater than 0.00"))
# update user balance after add
# update family balance after add        
        cash = balanceUser(username)
        money-= 1
        family_cash = balanceUser("Household")
        updateAccount("Household", family_cash+1)
        updateAccount(username, cash+money)
        return jsonify(genReturnDict(200, "Added to Account"))

# transfer -> post to server
# username, pwd, transfer to, transfer amount, verify
class Transfer(Resource):
    def post(self):
        postedData = request.get_json()
        username = postedData["Username"]
        password = postedData["Password"]
        to       = postedData["Transfer to"]
        money    = postedData["Amount to Transfer"]
        retJson, error = verifyCred(username, password)
# error
# if balance available less than zero
# if transfer amount input less than zero
# if transfer to user who doesn't exist
        if error:
            return jsonify(retJson)
        cash = balanceUser(username)
        if cash <= 0:
            return jsonify(genReturnDict(303, "Transfer Failed: Insufficient Funds"))
        if money<=0:
            return jsonify(genReturnDict(304, "Please enter an amount greater than 0.00"))
        if not UserExist(to):
            return jsonify(genReturnDict(301, "This user does not exist"))
# update all accounts following transfer
# household, user sending money, user receiving money
        cash_from = balanceUser(username)
        cash_to   = balanceUser(to)
        family_cash = balanceUser("Household")
        updateAccount("Household", family_cash+1)
        updateAccount(to, cash_to+money-1)
        updateAccount(username, cash_from - money)
# display message following successful transfer        
        retJson = {
            "Status":200,
            "Message": "Transfer Successful"
        }
        return jsonify(genReturnDict(200, "Transfer Successful"))

# balance -> post to server
# note to self: return to this one later, check notes
class Balance(Resource):
    def post(self):
        postedData = request.get_json()
        username = postedData["Username"]
        password = postedData["Password"]
        retJson, error = verifyCred(username, password)
        if error:
            return jsonify(retJson)
        retJson = users.find({
            "Username": username
        },{
            "Password": 0,
            "_id":0
        })[0]
        return jsonify(retJson)

# takeloan -> post
# username, password, borrowing x amount, verify
class TakeLoan(Resource):
    def post(self):
        postedData = request.get_json()
        username = postedData["Username"]
        password = postedData["Password"]
        money    = postedData["Amount"]
        retJson, error = verifyCred(username, password)
# error
        if error:
            return jsonify(retJson)
# update accounts following transaction        
        cash = balanceUser(username)
        debt = debtUser(username)
        updateAccount(username, cash+money)
        updateDebt(username, debt + money)
# display message following transaction
        return jsonify(genReturnDict(200, "Borrowed Funds Added to Account"))

# payloan -> post
# username, password, amount of payment, verify
class PayLoan(Resource):
    def post(self):
        postedData = request.get_json()
        username = postedData["Username"]
        password = postedData["Password"]
        money    = postedData["Payment Amount"]
        retJson, error = verifyCred(username, password)
# error
# if balance insufficient
        if error:
            return jsonify(retJson)
        cash = balanceUser(username)
        if cash < money:
            return jsonify(genReturnDict(303, "Insufficient Funds"))
# update each account following payment
        debt = debtUser(username)
        updateAccount(username, cash-money)
        updateDebt(username, debt - money)
# display message following successful payment
        return jsonify(genReturnDict(200, "Payment on Loan Successful"))

########################################################################

# housekeeping
api.add_resource(Register, '/register')
api.add_resource(Add, '/add')
api.add_resource(Transfer, '/transfer')
api.add_resource(Balance, '/balance')
api.add_resource(TakeLoan, '/takeloan')
api.add_resource(PayLoan, '/payloan')

# host vm
# note to self: double-check ip later
if __name__=="__main__":
    app.run(host='0.0.0.0')