from ...graphql_old.core.enums import to_enum
from ...shipping import ShippingMethodType

ShippingMethodTypeEnum = to_enum(ShippingMethodType, type_name="ShippingMethodTypeEnum")
