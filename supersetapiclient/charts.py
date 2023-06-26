"""Charts."""
from dataclasses import dataclass, field
from typing import List, Optional

from supersetapiclient.base import Object, ObjectFactories, default_string, json_field
from urllib.parse import urlencode
from base import raise_for_status

@dataclass
class ChartData(Object):
    JSON_FIELDS = ["applied_template_filters","annotation_data"]
    cache_key:str = default_string()
    cache_timeout:int = None
    applied_template_filters:dict = json_field()
    annotation_data:dict = json_field()
    error:str = None
    is_cached:bool = None
    query:str = None
    status:str = None
    stacktrace:str = None
    rowcount:int = None



@dataclass
class Chart(Object):
    JSON_FIELDS = ["params"]

    id: Optional[int] = None
    description: str = default_string()
    slice_name: str = default_string()
    params: dict = json_field()
    datasource_id: Optional[int] = None
    datasource_type: str = default_string()
    viz_type: str = ""
    dashboards: List[int] = field(default_factory=list)

    def to_json(self, columns):
        o = super().to_json(columns)
        o["dashboards"] = self.dashboards
        return o

    def get_row_count(self,force):
        client = self._parent.client
        url = client.join_urls(self.base_url,"data/")
        encoded_params = urlencode({"force":force})
        response = client.get(f"{url}?{encoded_params}")
        raise_for_status(response)
        response = response.json()

        object_json = response.get("result")[0]
        return ChartData().from_json(object_json).rowcount
    



class Charts(ObjectFactories):
    endpoint = "chart/"
    base_object = Chart

    @property
    def add_columns(self):
        # Due to the design of the superset API,
        # get /chart/_info only returns 'slice_name'
        # For chart adds to work,
        # we require the additional attributes:
        #   'datasource_id',
        #   'datasource_type'
        return [
            "datasource_id",
            "datasource_type",
            "slice_name",
            "params",
            "viz_type",
            "description",
        ]
