__author__ = 'abdul'

from carbonio_client.client import CarbonIOClient

client = CarbonIOClient("http://localhost:8888")
ep = client.get_endpoint("hello")

print ep.get()