import mock
import pytest
from pyramid.testing import DummyRequest

from pyramid_swagger.api import build_api_declaration_view
from pyramid_swagger.api import register_swagger_endpoints
from pyramid_swagger.ingest import API_DOCS_FILENAME
from pyramid_swagger.ingest import ApiDeclarationNotFoundError
from pyramid_swagger.ingest import ResourceListingNotFoundError
from tests.acceptance.response_test import get_registry


def test_basepath_rewriting():
    resource_json = {'basePath': 'bar'}
    view = build_api_declaration_view(resource_json)
    request = DummyRequest(application_url='foo')
    result = view(request)
    assert result['basePath'] == request.application_url
    assert result['basePath'] != resource_json['basePath']


def build_config(schema_dir):
    return mock.Mock(
        registry=get_registry({'pyramid_swagger.schema_directory': schema_dir})
    )


def test_proper_error_on_missing_resource_listing():
    with pytest.raises(ResourceListingNotFoundError) as exc:
        register_swagger_endpoints(
            build_config('tests/sample_schemas/missing_resource_listing/'),
        )
    assert(
        'tests/sample_schemas/missing_resource_listing/api_docs.json'
        in str(exc)
    )
    assert 'must be named {0}'.format(API_DOCS_FILENAME) in str(exc)


def test_proper_error_on_missing_api_declaration():
    with pytest.raises(ApiDeclarationNotFoundError) as exc:
        register_swagger_endpoints(
            build_config('tests/sample_schemas/missing_api_declaration/'),
        )
    assert (
        'tests/sample_schemas/missing_api_declaration/missing.json'
        in str(exc)
    )
