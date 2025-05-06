# Copyright (c) 2024, phamos GmbH and contributors
# For license information, please see license.txt

import json
import frappe
import requests
from frappe import _
from frappe.utils import cstr
from frappe.model.document import Document

class RemoteServerConnector(Document):
	def __init__(self, *args, **kwargs):
		super(RemoteServerConnector, self).__init__(*args, **kwargs)
		if self.url and self.usr and self.pwd:
			self.authenticate()

	def authenticate(self):
		url = f"{self.url}/api/method/login"

		payload = {
			"usr": self.usr,
			"pwd": self.get_password(fieldname="pwd")
		}
		headers = {
			"Content-Type": "application/json",
		}

		response = requests.request("POST", url, json=payload, headers=headers)
		if response.ok and response.status_code == 200:
			cookies = response.cookies.get_dict()
			self.cookies = "; ".join([f"{key}={value}" for key, value in cookies.items()])
			self.cookie_headers = {"cookie": self.cookies}

		else:
			frappe.throw(_("Authentication Failed"))

	def fetch_work_summary(self, from_date, to_date):
		url = f"{self.url}/api/method/frappe.desk.reportview.get"

		filters = json.dumps([["Timesheet","owner","=",self.usr],["Timesheet Detail","to_time","Between",[from_date,to_date]]])

		data = {
			'doctype': 'Timesheet',
			'fields': '["`tabTimesheet`.`name`","`tabTimesheet Detail`.`project`","`tabTimesheet`.`total_hours`"]',
			'filters': filters,
			'start': 0,
			'page_length': 200,
			'view': 'Report',
			'with_comment_count': 'false'
		}

		response = requests.request("POST", url, headers=self.cookie_headers, data=data)
		if response.ok and response.status_code == 200:
			message = response.json().get("message")
			if isinstance(message, dict):
				work_summary = message.get("values")
			elif isinstance(message, list):
				work_summary = message
			else:
				work_summary = []

			return work_summary
		else:
			frappe.throw(_("Something went wrong"))

	def fetch_project(self, project):
		url = f"{self.url}/api/resource/Project/{project}"
		response = requests.request("GET", url, headers=self.cookie_headers)
		if response.ok and response.status_code == 200:
			response_json = response.json().get("data") or {}
			return response_json
		else:
			frappe.throw(_("Something went wrong"))
