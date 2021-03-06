# Author: Zane Miller
# Date: 05/02/2022
# Email: millzane@oregonstate.edu
# Description: Application to generate QR Codes that communicate with Google Authenticator
import datetime
import time

import pyotp
import pyqrcode


def generate_secret_key():
	""" Generates a 32 character base32 secret, compatible with Google Authenticator """
	secret_key = pyotp.random_base32()

	return secret_key


def encode_uri():
	"""
	Encodes the provisioning uri to parse for Google Authenticator
	otpauth://TYPE/LABEL?PARAMETERS
	LABEL: label = accountname / issuer (“:” / “%3A”) *”%20” accountname
	"""
	account_name = 'HAL9000@2001.SpaceOdyssey.com'
	issuer_name = 'Discovery 1'

	encoded_uri = pyotp.totp \
		.TOTP('MYU6T2VU4MEEUI3QIF4QZWZXD6GPJBSE') \
		.provisioning_uri(
			name=account_name,
			issuer_name=issuer_name)

	return encoded_uri


def generate_qr():
	"""
	Generates a QR code that encodes the URI GA expects. URI contains secret keys along with the
	user id required for the TOTP algorithm.
	"""
	# get the encoded URI
	uri = encode_uri()
	# Create QR Code
	qr_code = pyqrcode.create(uri)
	# print the QR Code
	print(qr_code.terminal(quiet_zone=1))


def get_otp():
	"""
	Generates an OTP which will match the OTP generated by the Google Authenticator in 30 second
	intervals.
	"""
	# get OTP for specified secret_key
	totp = pyotp.TOTP("MYU6T2VU4MEEUI3QIF4QZWZXD6GPJBSE")
	# calculate the remaining time before OTP refreshes
	time_remaining = totp.interval - datetime.datetime.now().timestamp() % totp.interval // 1
	# print the OTP when get_otp() first called
	print('Current OTP:', totp.now())
	# Sleep until first OTP expires and begin infinite loop
	time.sleep(time_remaining)
	# loop on a 30-second interval starting when the OTP first refreshes after initial call
	while True:
		print('New OTP:', totp.now())
		time.sleep(30)
		break


def verify_password(passcode):
	""" Verifies the user's passcode against the current OTP """
	# get OTP for specified secret_key
	totp = pyotp.TOTP("MYU6T2VU4MEEUI3QIF4QZWZXD6GPJBSE")

	return totp.verify(passcode)


if __name__ == '__main__':
	user_pass_code = input("Please enter your passcode: ")
	if verify_password(user_pass_code):
		print("Success!")
	else:
		print("Failure!")
	generate_qr()
	while True:
		get_otp()


