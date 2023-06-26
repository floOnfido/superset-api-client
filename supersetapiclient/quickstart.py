from client import SupersetClient

client = SupersetClient(
    host="",
    username="",
    password="",
)

chart = client.charts.find_one(slice_name="Image Quality Fail Reasons")
data = chart.get_row_count(True)
print(data)