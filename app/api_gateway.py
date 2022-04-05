import asyncio
from cmath import log
from crypt import methods
from flask import flash, make_response, request
import grpc

import sys
sys.path.insert(0,'/home/chandradhar/Projects/CTY/AlwaysObservableWebApp/microservices/auth_svc/src')
import user_pb2_grpc,user_pb2

from flask import Flask,render_template,request
app = Flask(__name__)
app.secret_key = 'abc'

'''
GRPC client side functions
'''
async def signup(username,password):
    print(f"********{username},{password}********")
    async with grpc.aio.insecure_channel('localhost:50051') as channel:
        success = {'success': False}
        try:
            stub = user_pb2_grpc.userServiceStub(channel)
            success = await stub.createAccount(user_pb2.aUser(username=username,password=password))
            print(success)
        except Exception as e:
            print(f"[ERROR]: {e}")
        finally:
            print(f"Success {success}")
            return success

async def signin(username,password):
    print(f"********{username},{password}********")
    async with grpc.aio.insecure_channel('localhost:50051') as channel:
        success = {'success':0,'msg':'','token':'','timelimit':''}
        try:
            stub = user_pb2_grpc.userServiceStub(channel)
            success = await stub.login(user_pb2.aUser(username=username,password=password))
            print(success)
            return success
        except Exception as e:
            print(f'[ERROR]: {e}')
        finally:
            print(f"success {success}")


@app.route("/",methods=['GET'])
def homePage():
    return render_template('login.html')

@app.route("/createAccount",methods=['POST','GET'])
async def createAccount():
    if request.method=='POST':
        success = await signup(request.form.get('username'),request.form.get('password'))
        if success.success:
            #render success page and redirect to login UI
            flash(success.msg)
            return render_template('login.html')
        else:
            #render the create Account page again
            flash(success.msg)
            return render_template('signup.html')
    elif request.method=='GET':
        return render_template('signup.html')

@app.route("/login",methods=['POST','GET'])
async def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method=='POST':
        success = await  signin(request.form.get('username'),request.form.get('password'))
        if success.success:
            flash(success.msg)
            response = make_response(render_template('homepage.html'))
            response.headers.set("jwt_token",success.token)
            return response
        else:
            flash(success.msg)
            response = make_response(render_template('login.html'))
            response.headers.set("jwt_token",'')
            return response

if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0',port=5000)