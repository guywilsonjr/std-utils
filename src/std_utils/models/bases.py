from pydantic import BaseModel, ConfigDict


class StdBaseModel(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        extra='forbid',
        revalidate_instances='always',
        validate_default=True,
        validate_assignment=True,
        regex_engine='python-re',
        validation_error_cause=True
)
