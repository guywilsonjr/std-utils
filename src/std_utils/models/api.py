import http
from functools import cache
from typing import Any, Literal, Optional

import aiohttp
import requests
from pydantic import BaseModel, ConfigDict, Field, HttpUrl, Json
from requests import Session


DEFAULT_HEADERS = {'Content-Type': 'application/json'}
JsonPrimValue = str | bool | int | float | None


@cache
def get_default_headers() -> dict[str, str]:
    return DEFAULT_HEADERS


@cache
def get_empty_json() -> Json[Any]:
    return {}


class APIHeaders(BaseModel):
    """
    Model that represents a generic API headers.
    """
    model_config = ConfigDict(extra='allow')
    content_type: Literal['application/json'] = Field(
        alias='Content-Type',
        default='application/json',
        serialization_alias='Content-Type')


class APIResponse(BaseModel):
    """
    Model that represents a generic API response.
    """

    status_code: int
    headers: dict = Field(default_factory=get_empty_json)
    data: dict = Field(default_factory=get_empty_json)
    error: Optional[str] = None


class APIRequest(BaseModel):
    """
    Model that represents a generic API request.
    """
    endpoint: HttpUrl
    method: http.HTTPMethod
    headers: dict = Field(default_factory=get_default_headers)
    query_params: dict = Field(default_factory=get_empty_json)
    body: dict = Field(default_factory=get_empty_json)

    def send(self, session: Optional[Session] = None, **kwargs) -> Any:
        full_args = {
            'method': self.method,
            'url': self.endpoint.unicode_string(),
            'headers': self.headers,
            'params': self.query_params,
            'json': self.body
        }
        # Allow overriding the default values
        full_args.update(kwargs)
        if session:
            return session.request(
                **full_args)
        return requests.request(**full_args)

    async def async_send(
        self, client_session: Optional[aiohttp.ClientSession] = None, **kwargs
    ) -> Any:
        full_args = {
            'method': self.method,
            'url': self.endpoint.unicode_string(),
            'headers': self.headers,
            'params': self.query_params,
            'json': self.body
        }
        full_args.update(kwargs)

        if client_session:
            return await self.async_send_with_session(
                client_session, **full_args)
        else:
            async with aiohttp.ClientSession() as client_session:
                return await self.async_send_with_session(
                    client_session, **full_args)

    async def async_send_with_session(
        self, client_session: aiohttp.ClientSession, **kwargs
    ) -> Any:
        full_args = {
            'method': self.method,
            'url': self.endpoint.unicode_string(),
            'headers': self.headers,
            'params': self.query_params,
            'json': self.body
        }
        full_args.update(kwargs)
        if self.method == http.HTTPMethod.GET:
            return await client_session.get(**full_args)
        elif self.method == http.HTTPMethod.POST:
            return await client_session.post(**full_args)
        elif self.method == http.HTTPMethod.PUT:
            return await client_session.put(**full_args)
        elif self.method == http.HTTPMethod.DELETE:
            return await client_session.delete(**full_args)
        elif self.method == http.HTTPMethod.PATCH:
            return await client_session.patch(**full_args)
