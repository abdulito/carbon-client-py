__author__ = 'abdul'

from carbon_client.client import CarbonClient

client = CarbonClient("http://localhost:8888")
ep = client.get_endpoint("hello")

print ep.get()