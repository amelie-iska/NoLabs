# coding: utf-8

"""
    Conformations api

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)

    The version of the OpenAPI document: 0.1.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json


from typing import Any, ClassVar, Dict, List, Optional, Union
from pydantic import BaseModel, StrictFloat, StrictInt, StrictStr
from conformations_microservice.models.integrators import Integrators
try:
    from typing import Self
except ImportError:
    from typing_extensions import Self

class RunGromacsSimulationsRequest(BaseModel):
    """
    RunGromacsSimulationsRequest
    """ # noqa: E501
    job_id: StrictStr
    top: StrictStr
    gro: StrictStr
    temperature_k: Optional[Union[StrictFloat, StrictInt]] = 273.15
    friction_coeff: Optional[Union[StrictFloat, StrictInt]] = 1.0
    step_size: Optional[Union[StrictFloat, StrictInt]] = 0.002
    integrator: Optional[Integrators] = None
    take_frame_every: Optional[StrictInt] = 1000
    total_frames: Optional[StrictInt] = 10000
    __properties: ClassVar[List[str]] = ["job_id", "top", "gro", "temperature_k", "friction_coeff", "step_size", "integrator", "take_frame_every", "total_frames"]

    model_config = {
        "populate_by_name": True,
        "validate_assignment": True,
        "protected_namespaces": (),
    }


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of RunGromacsSimulationsRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        _dict = self.model_dump(
            by_alias=True,
            exclude={
            },
            exclude_none=True,
        )
        return _dict

    @classmethod
    def from_dict(cls, obj: Dict) -> Self:
        """Create an instance of RunGromacsSimulationsRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "job_id": obj.get("job_id"),
            "top": obj.get("top"),
            "gro": obj.get("gro"),
            "temperature_k": obj.get("temperature_k") if obj.get("temperature_k") is not None else 273.15,
            "friction_coeff": obj.get("friction_coeff") if obj.get("friction_coeff") is not None else 1.0,
            "step_size": obj.get("step_size") if obj.get("step_size") is not None else 0.002,
            "integrator": obj.get("integrator"),
            "take_frame_every": obj.get("take_frame_every") if obj.get("take_frame_every") is not None else 1000,
            "total_frames": obj.get("total_frames") if obj.get("total_frames") is not None else 10000
        })
        return _obj


