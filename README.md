# DNSMadeEasyAsPy

Python 3 library for DNSMadeEasy API v2.0 (currently **very much** a work in progress)

Inspiration taken from [atl/dnsmadeeasy-python](https://github.com/atl/dnsmadeeasy-python)

## Usage

```python
from dme import DMECLient

client = DMEClient("API_KEY", "SECRET_KEY")
domains = client.list_domains()
print(domains)

```

## Development

If you want to develop on this project, reading [this doc](https://dnsmadeeasy.com/pdf/API-Docv2.pdf) is a good place to start. You'll want to set up a DME [sandbox account](http://sandbox.dnsmadeeasy.com/account/new) for testing.

### Running the tests

To run the tests with your local changes, you can run:

```sh
pip install .
py.test
```

Make sure you have a valid `DME_API_KEY` and `DME_SECRET_KEY` set in your environment.