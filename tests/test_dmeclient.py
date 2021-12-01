from dme import DMEClient

import os
import petname


def test_managed_domains():
    """Tests API calls to add, list, and delete domains"""

    client = DMEClient(os.getenv("DME_API_KEY"), os.getenv("DME_SECRET_KEY"))
    domains = client.list_managed_domains()
    num_domains = len(domains)
    # Get the initial number here since people might not start with 0 domains

    domain_name = f"test-{petname.Generate(3)}.com"

    response = client.create_managed_domain(domain_name)
    assert response["name"] == domain_name, "The domain should be named in the response"
    assert isinstance(
        response["created"], int
    ), "The domain should be named in the response"

    domains = client.list_managed_domains()
    assert len(domains) == (num_domains + 1), "One domain should have been created"
    domain_id = client.get_domain_id(domain_name)
    assert type(domain_id) == int, "The domain ID should exist and be numeric"

    response = client.delete_managed_domain(domain_name)
    assert response == {}, "There should be no output on successful delete"

    domain = client.get_domain_by_name(domain_name)
    assert domain["pendingActionId"] == 3, "The pending action should be deletion"


def test_records():
    """Tests API calls to create, modify, and delete records"""

    client = DMEClient(os.getenv("DME_API_KEY"), os.getenv("DME_SECRET_KEY"))
    domain_name = f"test-{petname.Generate(3)}.com"
    client.create_managed_domain(domain_name)

    response = client.create_record(
        domain_name, name="testhost", record_type="A", value="10.1.1.1", ttl=500
    )

    assert response["failed"] == False, "Record creation should be false"

    records = client.list_records(domain_name)
    assert (
        records["data"][0]["name"] == "testhost"
    ), "The created record should be listed"
    assert (
        records["data"][0]["value"] == "10.1.1.1"
    ), "The created record should have the correct value"

    records = client.get_records_by_name(domain_name, "testhost")
    assert (
        records["data"][0]["name"] == "testhost"
    ), "The created record should be returned from the search"
    record_id = records["data"][0]["id"]

    response = client.update_record(
        domain_name,
        record_id,
        name="testhost",
        record_type="A",
        value="10.1.2.3",
        ttl=3600,
    )
    assert response == {}, "There should be no output on a successful update"

    response = client.delete_record(domain_name, record_id)
    assert response == {}, "There should be no output on a successful delete"

    records = client.get_records_by_name(domain_name, "testhost")
    assert len(records["data"]) == 0, "The record should have been deleted"

    client.delete_managed_domain(domain_name)
