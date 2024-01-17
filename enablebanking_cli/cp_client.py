import json
import http.client
import urllib.parse


class CpClient:
    def __init__(self, cp_domain, auth_data_path=None):
        self.cp_domain = cp_domain
        self.auth_data_path = auth_data_path
        self.auth_data = None

    def _request(self, *args, **kwargs):
        conn = http.client.HTTPSConnection(self.cp_domain)
        conn.request(*args, **kwargs)
        return conn.getresponse()

    def _load_auth_data(self):
        if self.auth_data_path is None:
            raise Exception("Auth data path is not available")
        with open(self.auth_data_path, "r") as f:
            self.auth_data = json.loads(f.read())
        return self.auth_data

    def _save_auth_data(self):
        with open(self.auth_data_path, "w") as f:
            f.write(json.dumps(self.auth_data))

    def auth(endpoint_method):
        def wrapper(self, *args, **kwargs):
            if self.auth_data is None:
                self._load_auth_data()
            response = endpoint_method(self, *args, **kwargs)
            if response.status == 401:
                r = self.make_token()
                if r.status != 200:
                    raise Exception(f"Unable to refresh token: {r.read().decode()}")
                token = json.loads(r.read())
                self.auth_data["idToken"] = token["id_token"]
                self.auth_data["refreshToken"] = token["refresh_token"]
                self.auth_data["expiresIn"] = token["expires_in"]
                self._save_auth_data()
                response = endpoint_method(self, *args, **kwargs)
            return response
        return wrapper

    def make_token(self):
        return self._request(
            "POST",
            "/api/token",
            urllib.parse.urlencode({
                "grant_type": "refresh_token",
                "refresh_token": self.auth_data["refreshToken"],
            }),
            {
                "content-type": "application/x-www-form-urlencoded",
            },
        )

    def get_oob_confirmation_code(self, email, callback_port):
        return self._request(
            "POST",
            "/api/relyingparty/getOobConfirmationCode",
            json.dumps({
                "requestType": "EMAIL_SIGNIN",
                "email": email,
                "continueUrl": f"http://localhost:{callback_port}/",
                "canHandleCodeInApp": True,
            }),
            {
                "content-type": "application/json",
            },
        )

    def make_email_link_signin(self, email, oob_code):
        return self._request(
            "POST",
            "/api/relyingparty/emailLinkSignin",
            json.dumps({
                "oobCode": oob_code,
                "email": email,
            }),
            {
                "content-type": "application/json",
            },
        )

    @auth
    def register_application(self, app_data):
        return self._request(
            "POST",
            "/api/applications",
            json.dumps({k: v for k, v in app_data.items() if v is not None}),
            {
                "content-type": "application/json",
                "authorization": f"Bearer {self.auth_data['idToken']}",
            },
        )

    @auth
    def fetch_requests(
            self,
            app_id,
            account_id=None,
            aspsp_country=None,
            aspsp_name=None,
            auth_approach=None,
            auth_method=None,
            authorization_id=None,
            endpoint_name=None,
            payment_id=None,
            psu_type=None,
            response_code=None,
            session_id=None,
            session_status=None,
    ):
        params = {
            "appId": app_id,
        }
        if account_id:
            params["accountId"] = account_id
        if aspsp_country:
            params["country"] = aspsp_country
        if aspsp_name:
            params["brand"] = aspsp_name
        if auth_approach:
            params["authApproach"] = auth_approach
        if auth_method:
            params["authMethod"] = auth_method
        if authorization_id:
            params["autorizationId"] = authorization_id
        if endpoint_name:
            params["endpoint"] = endpoint_name
        if payment_id:
            params["paymentId"] = payment_id
        if psu_type:
            params["psuType"] = psu_type
        if response_code:
            params["responseCode"] = response_code
        if session_id:
            params["sessionId"] = session_id
        if session_status:
            params["sessionStatus"] = session_status
        query = urllib.parse.urlencode(params)
        return self._request(
            "GET",
            f"/api/requests?{query}",
            None,
            {
                "authorization": f"Bearer {self.auth_data['idToken']}",
            },
        )
