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
    print(response)
    assert response["name"] == domain_name, "The domain should be named in the response"
    assert isinstance(
        response["created"], int
    ), "The domain should be named in the response"

    domains = client.list_managed_domains()
    assert len(domains) == (num_domains + 1), "One domain should have been created"
    # TODO probably iterate over the domains and make sure at least one of them matches the new one

    response = client.delete_managed_domain(domain_name)
    print(response)
    # TODO figure out the asserts here once I actually CAN delete the domain
    # The problem is that domains seems to stay "creating" (and thus can't be deleted) for
    # A While, at least, which will make testing more difficult
