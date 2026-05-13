from pydantic import BaseModel


class MetaComponent(BaseModel):
    component_key: str
    display_name: str
    unit: str | None = None
    data_type: str


class MetaSource(BaseModel):
    source_code: str
    category: str
    location: str | None = None
    components: list[MetaComponent]


class MetaModule(BaseModel):
    module_key: str
    display_name: str
    sources: list[MetaSource]


class MetaResponse(BaseModel):
    modules: list[MetaModule]
