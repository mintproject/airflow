# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
"""
   webserver_config
   Referencies
     - https://flask-appbuilder.readthedocs.io/en/latest/security.html#authentication-oauth
"""
import os
import logging
import jwt
from flask import redirect, session
from flask_appbuilder import expose
from flask_appbuilder.security.manager import AUTH_OAUTH
from flask_appbuilder.security.views import AuthOAuthView
from airflow.www.security import AirflowSecurityManager


basedir = os.path.abspath(os.path.dirname(__file__))
log = logging.getLogger(__name__)

MY_PROVIDER = 'keycloak'
CLIENT_ID = 'airflow'
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
KEYCLOAK_BASE_URL = 'https://auth.mint.isi.edu/auth/realms/production/protocol/openid-connect/'
KEYCLOAK_TOKEN_URL = 'https://auth.mint.isi.edu/auth/realms/production/protocol/openid-connect/token'
KEYCLOAK_AUTH_URL = 'https://auth.mint.isi.edu/auth/realms/production/protocol/openid-connect/auth'

AUTH_TYPE = AUTH_OAUTH
AUTH_ROLES_SYNC_AT_LOGIN = True

AUTH_USER_REGISTRATION = True
AUTH_USER_REGISTRATION_ROLE = "Public"
PERMANENT_SESSION_LIFETIME = 1800
AUTH_ROLES_MAPPING = {
  "airflow_admin": ["Admin"],
  "airflow_op": ["Op"],
  "airflow_user": ["User"],
  "airflow_viewer": ["Viewer"],
  "airflow_public": ["Public"],
}
OAUTH_PROVIDERS = [
  {
   'name': 'keycloak',
   'icon': 'fa-circle-o',
   'token_key': 'access_token', 
   'remote_app': {
     'client_id': CLIENT_ID,
     'client_secret': CLIENT_SECRET,
     'client_kwargs': {
       'scope': 'email profile'
     },
     'api_base_url': KEYCLOAK_BASE_URL,
     'request_token_url': None,
     'access_token_url': KEYCLOAK_TOKEN_URL,
     'authorize_url': KEYCLOAK_AUTH_URL,
    },
  },
]

class CustomAuthRemoteUserView(AuthOAuthView):
  @expose("/logout/")
  def logout(self):
    """Delete access token before logging out."""
    return super().logout()
  
class CustomSecurityManager(AirflowSecurityManager):
  authoauthview = CustomAuthRemoteUserView
  def oauth_user_info(self, provider, response):
    if provider == MY_PROVIDER:
      token = response["access_token"]
      me = jwt.decode(token, algorithms="RS256", verify=False)
      # sample of resource_access
      # {
      #   "resource_access": { "airflow": { "roles": ["airflow_admin"] }}
      # }
      groups = me["resource_access"]["airflow"]["roles"] # unsafe
      # log.info("groups: {0}".format(groups))
      if len(groups) < 1:
        groups = ["airflow_public"]
      else:
        groups = [str for str in groups if "airflow" in str]
        userinfo = {
        "username": me.get("preferred_username"),
        "email": me.get("email"),
        "first_name": me.get("given_name"),
        "last_name": me.get("family_name"),
        "role_keys": groups,
      }
      log.info("user info: {0}".format(userinfo))
      return userinfo
    else:
      return {}
SECURITY_MANAGER_CLASS = CustomSecurityManager
APP_THEME = "simplex.css"
