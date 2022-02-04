from supersetapiclient.client import SupersetClient

client = SupersetClient(
    host="http://localhost:8080",
    username="admin",
    password="admin",
)

dashboard = client.dashboards.find(dashboard_title="Example")[0]
client.dashboards.export(id=dashboard.id, name=dashboard.dashboard_title)
