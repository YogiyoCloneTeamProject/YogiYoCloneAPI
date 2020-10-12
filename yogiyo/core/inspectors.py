
from drf_yasg import openapi
from drf_yasg.inspectors import SerializerInspector

from drf_yasg.utils import swagger_settings
from drf_yasg.inspectors import SwaggerAutoSchema


class ExampleInspector(SerializerInspector):
    def process_result(self, result, method_name, obj, **kwargs):
        # obj.Meta.examples 에 접근할 수 없다면 예시를 넣을 수 없습니다.
        has_examples = hasattr(obj, 'Meta') and hasattr(obj.Meta, 'examples')
        if isinstance(result, openapi.Schema.OR_REF) and has_examples:
            schema = openapi.resolve_ref(result, self.components)
            # properties가 정의되지 않은 경우엔 할 수 있는게 없습니다.
            if 'properties' in schema:
                properties = schema['properties']
                for name in properties.keys():
                    # 예시를 정해둔 필드만 손댑니다.
                    try:
                        if name in obj.Meta.examples:
                            properties[name]['example'] = obj.Meta.examples[name]
                    except NotImplementedError:
                        pass

        # schema를 return하면 안 됩니다.
        # 위에서 schema를 수정해도 reference되어서 result에 반영됩니다.
        return result


class MyAutoSchema(SwaggerAutoSchema):
    field_inspectors = [
                           ExampleInspector,
                       ] + swagger_settings.DEFAULT_FIELD_INSPECTORS