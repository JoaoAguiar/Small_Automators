# Internet Speed tester
# pip install speedtest-cli
import speedtest as st

# Set Best Server
server = st.Speedtest()
server.get_best_server()

# Location of the Server
location = server.results.server['name']
print(f"Server Location: {location}")

# ISP Name
isp = server.results.client['isp']
print(f"ISP Name: {isp}")

# Test Download Speed
down = server.download()
down = down / 1000000
print(f"Download Speed: {down} Mb/s")

# Test Upload Speed
up = server.upload()
up = up / 1000000
print(f"Upload Speed: {up} Mb/s")

# Test Ping
ping = server.results.ping
print(f"Ping Speed: {ping}")