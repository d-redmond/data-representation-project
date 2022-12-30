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
from flask import Flask, jsonify, request
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
        return genReturnDicty(302, "Incorrect Password"), True
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
