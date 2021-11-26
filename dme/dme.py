import requests
import hmac
import hashlib

from time import strftime, gmtime


class DMEClient:
    def __init__(self, api_key, secret_key):
        if api_key == None:
            raise KeyError("api_key missing")
        if secret_key == None:
            raise KeyError("secret_key missing")
        self.api_key = api_key
        self.secret_key = secret_key
        self.base_url = "http://api.sandbox.dnsmadeeasy.com/V2.0"
        # self.base_url = "http://api.dnsmadeeasy.com/V2.0"
        # TODO uncomment this after testing

    def _headers(self):
        now = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        date_hash = self._create_hash(now)
        headers = {
            "x-dnsme-apiKey": self.api_key,
            "x-dnsme-hmac": date_hash,
            "x-dnsme-requestDate": now,
            "content-type": "application/json",
            "accept": "application/json",
        }
        return headers

    def _create_hash(self, now):
        return hmac.new(
            self.secret_key.encode(), now.encode(), hashlib.sha1
        ).hexdigest()

    def _get_request(self, resource):
        response = requests.get(f"{self.base_url}/{resource}", headers=self._headers())
        if response.status_code == 200 or response.status_code == 201:
            if response != None:
                return response.json()
        else:
            raise Exception(
                f"Error talking to DNSMadeEasy: {response.status_code} - {response.text}"
            )

    def _put_request(self, resource):
        pass

    def _post_request(self, resource, json_body):
        response = requests.post(
            f"{self.base_url}/{resource}",
            headers=self._headers(),
            json=json_body,
        )
        if response.status_code == 200 or response.status_code == 201:
            if response != None:
                return response.json()
        else:
            raise Exception(
                f"Error talking to DNSMadeEasy: {response.status_code} - {response.text}"
            )

    def _delete_request(self, resource):
        response = requests.delete(
            f"{self.base_url}/{resource}",
            headers=self._headers(),
        )
        if response.status_code == 200 or response.status_code == 201:
            if response != None:
                return response.json()
        else:
            raise Exception(
                f"Error talking to DNSMadeEasy: {response.status_code} - {response.text}"
            )

    ### Managed domains

    def list_managed_domains(self):
        domains = []
        json_response = self._get_request("dns/managed")
        for domain in json_response["data"]:
            domains.append(domain)
        return domains

    def create_managed_domain(self, domain):
        data = {"name": domain}
        json_response = self._post_request("dns/managed/", data)
        return json_response

    def delete_managed_domain(self, domain):
        domain_id = self.get_domain_id(domain)
        json_response = self._delete_request(f"dns/managed/{domain_id}")
        return json_response

    def get_domain_id(self, domain):
        json_response = self._get_request(f"dns/managed/name?domainname={domain}")
        return json_response["id"]

    ### Domain records

    def create_record(self, domain, type, value, ttl, gtdLocation):
        pass
        # TODO next up
