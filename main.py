import sys
import bottle
import json

import os
import requests

import server_code.FirebaseAPI.firebaseAPI as fire

from server_code.parse_login.parse_login import parse_email
from server_code import client_validator
from server_code.FirebaseAPI.Registration import registerUser
import server_code.FirebaseAPI.firebase_queue as fire_q


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000

    @bottle.route('/')
    def ret_html():
        return bottle.static_file("index.html", ".")

    @bottle.route('/<filename>')
    def ret_html_2(filename):
        return bottle.static_file(filename, ".") if ".html" in filename else None

    @bottle.route('/assets/<filename:path>')
    def ret_assets(filename):
        return bottle.static_file(filename, "./assets")


    @bottle.post('/userRegistration')
    def validate_registration():
        response = bottle.request.body.read().decode()
        decoded_response = client_validator.sanitize_input(response)
        # check if registering
        if client_validator.contains(decoded_response, ['email', 'name', 'password', 'typeofUser']):
            valid_state = parse_email(decoded_response['email'], 'buffalo.edu')
            if valid_state != 'valid':
                return json.dumps({
                    'valid': valid_state
                })
            valid_state = registerUser(decoded_response)
            return json.dumps({
                'valid': valid_state
            })
        else:
            return json.dumps({
                'valid': 'invalid!'
            })

    @bottle.post('/queuedata')
    def return_queue():
        response = bottle.request.body.read().decode()
        decoded_response = client_validator.sanitize_input(response)
        try:
            fire.auth.get_account_info(decoded_response['token'])
        except requests.HTTPError:
            return json.dumps({'valid': 'invalid'})
        try:
            cse220 = fire_q.access_queue('cse220')
        except fire_q.QueueDoesNotExist:
            cse220 = ({}, 0)
        try:
            cse250 = fire_q.access_queue('cse250')
        except fire_q.QueueDoesNotExist:
            cse250 = ({}, 0)
        try:
            cse354 = fire_q.access_queue('cse354')
        except fire_q.QueueDoesNotExist:
            cse354 = ({}, 0)
        return json.dumps({
            'CSE220': {'queue': cse220[0], 'length': cse220[1]},
            'CSE250': {'queue': cse250[0], 'length': cse250[1]},
            'CSE354': {'queue': cse354[0], 'length': cse354[1]},
            'valid': 'valid'
        })

    bottle.run(host="0.0.0.0", port=port)
