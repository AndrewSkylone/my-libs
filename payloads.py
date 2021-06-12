import copy


def get_payload(operationName, variables={}) -> dict:
    payload_vars = copy.deepcopy(VARIABLES[operationName])
    payload_vars.update(variables)

    payload = {
        'operationName' : operationName,
        'variables' : payload_vars,
        'query' : QUERIES[operationName]
        }

    return payload

def get_autorization_payload(email, password) -> dict:
    return get_payload(operationName='UserCreateAccessToken', variables={"input":{"email":email,"password":password}})

def get_orders_payload(orders_num, orderLabelId='', orderStatus='') -> dict:
    variables = {}

    if orderLabelId:
        variables.update({'ordersFirst': orders_num, 'orderLabelId' : orderLabelId})
    if orderStatus:
        variables.update({'ordersFirst': orders_num, 'orderStatus' : orderStatus})
    
    return get_payload(operationName='OrderList', variables=variables)

def get_SearchOrdersAndProduct_payload(order_number : str) -> dict:
    return get_payload('SearchOrdersAndProduct', {'ordersQuery' : '%' + order_number, 'productQuery' : order_number})

def get_orderStatuses_payload() -> dict:
    return get_payload(operationName='OrderStatuses')

def get_orderLabels_payload() -> dict:
    return get_payload(operationName='OrderLabels')

def get_OrderNode_payload(order_id : str) -> dict:
    return get_payload(operationName='OrderNode', variables={'id' : order_id})

VARIABLES = {
    'OrderList' : {"includeOrderLabels":False,"includeCustomerAddresses":False,"includeOrderLineItems":False,"includeProductDescription":False,"includeOrderEvents":False},
    'UserCreateAccessToken' : {"includeUser":True},
    'OrderStatuses' : {},
    'OrderLabels' : {'includeOrderCount': True, 'orderLabelsFirst': 15},
    'OrderNode' : {"includeOrderLabels":True,"includeCustomerAddresses":True,"includeOrderLineItems":True,"includeProductDescription":False,"includeOrderEvents":True,"includeShipments":True,"orderLineItemsFirst":10,"orderLabelsFirst":15,"orderEventsFirst":10,"shipmentsFirst":10},
    'SearchOrdersAndProduct' : {"includeProductDescription":False,"ordersFirst":15}
}

QUERIES = {
'OrderList' : "query OrderList($orderStatus: OrderStatus, $orderFulfillmentStatus: OrderFulfillmentStatus, $orderLabelId: ID, $includeOrderLabels: Boolean = true, $includeCustomerAddresses: Boolean = false, $includeOrderLineItems: Boolean = false, $includeProductDescription: Boolean = false, $includeOrderEvents: Boolean = false, $ordersFirst: Int, $ordersLast: Int, $ordersBefore: String, $ordersAfter: String, $orderLabelsFirst: Int, $orderLabelsLast: Int, $orderLabelsBefore: String, $orderLabelsAfter: String, $orderLineItemsFirst: Int, $orderLineItemsLast: Int, $orderLineItemsBefore: String, $orderLineItemsAfter: String, $orderEventsFirst: Int, $orderEventsLast: Int, $orderEventsBefore: String, $orderEventsAfter: String, $orderShopId: ID) {\n  orders(\n    first: $ordersFirst\n    last: $ordersLast\n    before: $ordersBefore\n    after: $ordersAfter\n    status: $orderStatus\n    fulfillmentStatus: $orderFulfillmentStatus\n    orderLabelId: $orderLabelId\n    shopId: $orderShopId\n  ) {\n    pageInfo {\n      ...PageInfo\n      __typename\n    }\n    edges {\n      node {\n        ...Order\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment PageInfo on PageInfo {\n  hasNextPage\n  hasPreviousPage\n  startCursor\n  endCursor\n  __typename\n}\n\nfragment Order on Order {\n  id\n  status\n  fulfillmentStatus\n  name\n  customerName\n  customerEmail: email\n  shop {\n    ...Shop\n    __typename\n  }\n  shopifyOrder {\n    id\n    legacyResourceId\n    __typename\n  }\n  customer {\n    ...Customer\n    __typename\n  }\n  shippingAddress {\n    ...Address\n    __typename\n  }\n  formattedShippingAddress {\n    ...Address\n    __typename\n  }\n  orderLineItems(\n    first: $orderLineItemsFirst\n    last: $orderLineItemsLast\n    before: $orderLineItemsBefore\n    after: $orderLineItemsAfter\n  ) @include(if: $includeOrderLineItems) {\n    pageInfo {\n      ...PageInfo\n      __typename\n    }\n    edges {\n      node {\n        ...OrderLineItem\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  orderEvents(\n    first: $orderEventsFirst\n    last: $orderEventsLast\n    before: $orderEventsBefore\n    after: $orderEventsAfter\n  ) @include(if: $includeOrderEvents) {\n    ...OrderEventConnection\n    __typename\n  }\n  orderLabels(\n    first: $orderLabelsFirst\n    last: $orderLabelsLast\n    before: $orderLabelsBefore\n    after: $orderLabelsAfter\n  ) @include(if: $includeOrderLabels) {\n    pageInfo {\n      ...PageInfo\n      __typename\n    }\n    edges {\n      node {\n        ...OrderLabel\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  orderLinks {\n    ...OrderLink\n    __typename\n  }\n  discountCode\n  currency\n  subtotalPrice\n  totalDiscount\n  totalShipping\n  totalPrice\n  usdSubtotalPrice: subtotalPrice(currency: \"USD\")\n  usdTotalShipping: totalShipping(currency: \"USD\")\n  usdTotalPrice: totalPrice(currency: \"USD\")\n  insertedAt\n  updatedAt\n  __typename\n}\n\nfragment Shop on Shop {\n  id\n  currencyCode\n  displayName\n  ecomPlatform\n  ecomPlatformId\n  storefrontHost\n  insertedAt\n  updatedAt\n  __typename\n}\n\nfragment Customer on Customer {\n  id\n  email\n  phone\n  firstName\n  lastName\n  defaultAddress {\n    ...Address\n    __typename\n  }\n  addresses @include(if: $includeCustomerAddresses) {\n    ...Address\n    __typename\n  }\n  __typename\n}\n\nfragment Address on Address {\n  id\n  address1\n  address2\n  city\n  province\n  provinceCode\n  zip\n  country\n  countryCode\n  phone\n  name\n  firstName\n  lastName\n  cpf\n  company\n  __typename\n}\n\nfragment OrderLineItem on OrderLineItem {\n  id\n  price\n  totalPrice\n  barcode\n  quantity\n  status\n  fulfillmentStatus\n  shopifyOrderLineItem {\n    ...ShopifyOrderLineItem\n    __typename\n  }\n  marketplaceOrders {\n    ...MarketplaceOrder\n    __typename\n  }\n  product {\n    ...Product\n    __typename\n  }\n  productVariant {\n    ...ProductVariant\n    __typename\n  }\n  cancelledAt\n  insertedAt\n  updatedAt\n  usdPrice: price(currency: \"USD\")\n  usdTotalPrice: totalPrice(currency: \"USD\")\n  __typename\n}\n\nfragment ShopifyOrderLineItem on ShopifyOrderLineItem {\n  id\n  name\n  __typename\n}\n\nfragment MarketplaceOrder on MarketplaceOrder {\n  id\n  quantity\n  status\n  marketplaceOrderStatus\n  marketplaceLogisticsStatus\n  currency\n  price\n  subtotalPrice\n  totalPrice\n  shippingFee\n  shippingMethod\n  retailCurrency\n  retailPrice\n  retailShippingFee\n  retailSubtotalPrice\n  retailTotalPrice\n  marketplace\n  marketplaceId\n  marketplaceAccountId\n  marketplaceError\n  marketplaceErrorMessage\n  payloadOverrides {\n    ...MarketplaceOrderPayload\n    __typename\n  }\n  shippingAddress {\n    ...Address\n    __typename\n  }\n  shipments(first: 5) {\n    pageInfo {\n      ...PageInfo\n      __typename\n    }\n    edges {\n      node {\n        ...Shipment\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  processedAt\n  lastRefetchAt\n  insertedAt\n  updatedAt\n  __typename\n}\n\nfragment MarketplaceOrderPayload on MarketplaceOrderPayload {\n  accountEmail\n  force\n  itemId\n  propertyValueIds\n  productUrl\n  quantity\n  retailProductPriceCents\n  shippingFeeCents\n  address {\n    ...MarketplaceOrderPayloadAddress\n    __typename\n  }\n  __typename\n}\n\nfragment MarketplaceOrderPayloadAddress on MarketplaceOrderPayloadAddress {\n  address1\n  address2\n  city\n  zip\n  province\n  countryCode\n  mobileNumber\n  mobileNumberCountryPrefix\n  __typename\n}\n\nfragment Shipment on Shipment {\n  id\n  trackingNumber\n  lastMileCarrierTrackingNumber\n  shippingMethodHandle\n  shippingDays\n  lastEventDescription\n  lastEventStatus\n  lastRefetchAt\n  insertedAt\n  updatedAt\n  __typename\n}\n\nfragment Product on Product {\n  id\n  publishStatus\n  publishError\n  marketplaceProductUrl\n  deletedAt\n  deleteNote\n  deleteReason\n  quarantineType\n  quarantinedAt\n  insertedAt\n  updatedAt\n  productCompareAtPriceRange {\n    ...ProductPriceRange\n    __typename\n  }\n  productPriceRange {\n    ...ProductPriceRange\n    __typename\n  }\n  productTranslations {\n    ...ProductTranslation\n    __typename\n  }\n  productImages {\n    ...ProductImage\n    __typename\n  }\n  __typename\n}\n\nfragment ProductPriceRange on ProductPriceRange {\n  minVariantPrice\n  maxVariantPrice\n  __typename\n}\n\nfragment ProductTranslation on ProductTranslation {\n  id\n  language\n  title\n  description @include(if: $includeProductDescription)\n  __typename\n}\n\nfragment ProductImage on ProductImage {\n  id\n  src: marketplaceSrc\n  imageSrc\n  position\n  __typename\n}\n\nfragment ProductVariant on ProductVariant {\n  id\n  marketplaceId\n  position\n  sku\n  barcode\n  price\n  compareAtPrice\n  stockLevel\n  productImage {\n    ...ProductImage\n    __typename\n  }\n  updatedAt\n  insertedAt\n  __typename\n}\n\nfragment OrderEventConnection on OrderEventConnection {\n  edges {\n    node {\n      ...OrderEvent\n      __typename\n    }\n    __typename\n  }\n  pageInfo {\n    ...PageInfo\n    __typename\n  }\n  __typename\n}\n\nfragment OrderEvent on OrderEvent {\n  ...OrderFormattedShippingAddressEvent\n  ...OrderCommentEvent\n  ...OrderLabelEvent\n  ...MarketplaceOrderEvent\n  ...MarketplaceOrderFailedEvent\n  ...OrderLineItemEvent\n  __typename\n}\n\nfragment OrderFormattedShippingAddressEvent on OrderFormattedShippingAddressEvent {\n  id\n  type\n  value {\n    pre {\n      ...Address\n      __typename\n    }\n    post {\n      ...Address\n      __typename\n    }\n    __typename\n  }\n  orderFormattedShippingAddressActor: actor {\n    ...User\n    __typename\n  }\n  insertedAt\n  updatedAt\n  __typename\n}\n\nfragment User on User {\n  id\n  email\n  name\n  roles\n  updatedAt\n  insertedAt\n  __typename\n}\n\nfragment OrderCommentEvent on OrderCommentEvent {\n  id\n  type\n  value {\n    message\n    __typename\n  }\n  orderCommentActor: actor {\n    ...User\n    __typename\n  }\n  insertedAt\n  updatedAt\n  __typename\n}\n\nfragment OrderLabelEvent on OrderLabelEvent {\n  id\n  type\n  value {\n    action\n    orderLabel {\n      ...OrderLabel\n      __typename\n    }\n    __typename\n  }\n  orderLabelActor: actor {\n    ...User\n    __typename\n  }\n  insertedAt\n  updatedAt\n  __typename\n}\n\nfragment OrderLabel on OrderLabel {\n  id\n  color\n  handle\n  title\n  insertedAt\n  updatedAt\n  __typename\n}\n\nfragment MarketplaceOrderEvent on MarketplaceOrderEvent {\n  id\n  type\n  value {\n    message\n    __typename\n  }\n  marketplaceOrderActor: actor {\n    ...User\n    __typename\n  }\n  orderLineItem {\n    ...SimpleOrderLineItem\n    __typename\n  }\n  marketplaceOrder {\n    ...MarketplaceOrder\n    __typename\n  }\n  insertedAt\n  updatedAt\n  __typename\n}\n\nfragment SimpleOrderLineItem on OrderLineItem {\n  id\n  price\n  totalPrice\n  barcode\n  quantity\n  status\n  fulfillmentStatus\n  shopifyOrderLineItem {\n    ...ShopifyOrderLineItem\n    __typename\n  }\n  product {\n    ...Product\n    __typename\n  }\n  productVariant {\n    ...ProductVariant\n    __typename\n  }\n  cancelledAt\n  insertedAt\n  updatedAt\n  __typename\n}\n\nfragment MarketplaceOrderFailedEvent on MarketplaceOrderFailedEvent {\n  id\n  type\n  value {\n    errorCode\n    errorMessage\n    errorHint\n    __typename\n  }\n  orderLineItem {\n    ...SimpleOrderLineItem\n    __typename\n  }\n  marketplaceOrder {\n    ...MarketplaceOrder\n    __typename\n  }\n  insertedAt\n  updatedAt\n  __typename\n}\n\nfragment OrderLineItemEvent on OrderLineItemEvent {\n  id\n  type\n  value {\n    message\n    __typename\n  }\n  orderLineItemActor: actor {\n    ...User\n    __typename\n  }\n  orderLineItem {\n    ...SimpleOrderLineItem\n    __typename\n  }\n  insertedAt\n  updatedAt\n  __typename\n}\n\nfragment OrderLink on OrderLink {\n  id\n  type\n  url\n  params {\n    ticketId\n    __typename\n  }\n  insertedAt\n  updatedAt\n  __typename\n}\n",
'OrderStatuses' : "query OrderStatuses {\n  orderStatuses {\n    ...OrderStatuses\n    __typename\n  }\n}\n\nfragment OrderStatuses on OrderStatusCount {\n  count\n  status\n  __typename\n}\n",
'OrderLabels': "query OrderLabels($includeOrderCount: Boolean = false, $orderLabelsFirst: Int, $orderLabelsLast: Int, $orderLabelsBefore: String, $orderLabelsAfter: String) {\n  orderLabels(\n    first: $orderLabelsFirst\n    last: $orderLabelsLast\n    before: $orderLabelsBefore\n    after: $orderLabelsAfter\n  ) {\n    pageInfo {\n      ...PageInfo\n      __typename\n    }\n    edges {\n      node {\n        ...OrderLabel\n        ...OrderLabelWithOrderCount @include(if: $includeOrderCount)\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment PageInfo on PageInfo {\n  hasNextPage\n  hasPreviousPage\n  startCursor\n  endCursor\n  __typename\n}\n\nfragment OrderLabel on OrderLabel {\n  id\n  color\n  handle\n  title\n  insertedAt\n  updatedAt\n  __typename\n}\n\nfragment OrderLabelWithOrderCount on OrderLabel {\n  ...OrderLabel\n  orderCount\n  __typename\n}\n",
'UserCreateAccessToken' : "mutation UserCreateAccessToken($input: UserCreateAccessTokenInput!, $includeUser: Boolean = true) {\n  userCreateAccessToken(input: $input) {\n    accessToken {\n      ...UserAccessToken\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment UserAccessToken on UserAccessToken {\n  id\n  token\n  user @include(if: $includeUser) {\n    ...User\n    __typename\n  }\n  __typename\n}\n\nfragment User on User {\n  id\n  email\n  name\n  roles\n  updatedAt\n  insertedAt\n  __typename\n}\n",
'OrderNode' : "query OrderNode($id: ID!, $includeOrderLabels: Boolean = true, $includeCustomerAddresses: Boolean = true, $includeOrderLineItems: Boolean = true, $includeProductDescription: Boolean = false, $includeOrderEvents: Boolean = true, $includeShipments: Boolean = true, $orderLineItemsFirst: Int, $orderLineItemsLast: Int, $orderLineItemsBefore: String, $orderLineItemsAfter: String, $orderLabelsFirst: Int, $orderLabelsLast: Int, $orderLabelsBefore: String, $orderLabelsAfter: String, $orderEventsFirst: Int, $orderEventsLast: Int, $orderEventsBefore: String, $orderEventsAfter: String, $shipmentsFirst: Int, $shipmentsLast: Int, $shipmentsBefore: String, $shipmentsAfter: String) {\n  node(id: $id) {\n    __typename\n    ...OrderWithShipments\n  }\n}\n\nfragment OrderWithShipments on Order {\n  ...Order\n  shipments(\n    first: $shipmentsFirst\n    last: $shipmentsLast\n    before: $shipmentsBefore\n    after: $shipmentsAfter\n  ) @include(if: $includeShipments) {\n    pageInfo {\n      ...PageInfo\n      __typename\n    }\n    edges {\n      node {\n        ...Shipment\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment Order on Order {\n  id\n  status\n  fulfillmentStatus\n  financialStatus\n  ecomPlatform\n  name\n  customerName\n  customerEmail: email\n  shop {\n    ...Shop\n    __typename\n  }\n  shopifyOrder {\n    id\n    legacyResourceId\n    __typename\n  }\n  customer {\n    ...Customer\n    __typename\n  }\n  shippingAddress {\n    ...Address\n    __typename\n  }\n  formattedShippingAddress {\n    ...Address\n    __typename\n  }\n  orderLineItems(\n    first: $orderLineItemsFirst\n    last: $orderLineItemsLast\n    before: $orderLineItemsBefore\n    after: $orderLineItemsAfter\n  ) @include(if: $includeOrderLineItems) {\n    pageInfo {\n      ...PageInfo\n      __typename\n    }\n    edges {\n      node {\n        ...OrderLineItem\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  orderEvents(\n    first: $orderEventsFirst\n    last: $orderEventsLast\n    before: $orderEventsBefore\n    after: $orderEventsAfter\n  ) @include(if: $includeOrderEvents) {\n    ...OrderEventConnection\n    __typename\n  }\n  orderLabels(\n    first: $orderLabelsFirst\n    last: $orderLabelsLast\n    before: $orderLabelsBefore\n    after: $orderLabelsAfter\n  ) @include(if: $includeOrderLabels) {\n    pageInfo {\n      ...PageInfo\n      __typename\n    }\n    edges {\n      node {\n        ...OrderLabel\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  orderLinks {\n    ...OrderLink\n    __typename\n  }\n  discountCode\n  currency\n  subtotalPrice\n  totalDiscount\n  totalShipping\n  totalPrice\n  usdSubtotalPrice: subtotalPrice(currency: \"USD\")\n  usdTotalShipping: totalShipping(currency: \"USD\")\n  usdTotalPrice: totalPrice(currency: \"USD\")\n  insertedAt\n  updatedAt\n  __typename\n}\n\nfragment Shop on Shop {\n  id\n  currencyCode\n  displayName\n  ecomPlatform\n  ecomPlatformId\n  storefrontHost\n  insertedAt\n  updatedAt\n  __typename\n}\n\nfragment Customer on Customer {\n  id\n  email\n  phone\n  firstName\n  lastName\n  defaultAddress {\n    ...Address\n    __typename\n  }\n  addresses @include(if: $includeCustomerAddresses) {\n    ...Address\n    __typename\n  }\n  __typename\n}\n\nfragment Address on Address {\n  id\n  address1\n  address2\n  city\n  province\n  provinceCode\n  zip\n  country\n  countryCode\n  phone\n  name\n  firstName\n  lastName\n  cpf\n  company\n  __typename\n}\n\nfragment PageInfo on PageInfo {\n  hasNextPage\n  hasPreviousPage\n  startCursor\n  endCursor\n  __typename\n}\n\nfragment OrderLineItem on OrderLineItem {\n  id\n  price\n  totalPrice\n  barcode\n  quantity\n  status\n  fulfillmentStatus\n  productTitle\n  productVariantTitle\n  imageSrc\n  shopifyOrderLineItem {\n    ...ShopifyOrderLineItem\n    __typename\n  }\n  marketplaceOrders {\n    ...MarketplaceOrder\n    __typename\n  }\n  product {\n    ...Product\n    __typename\n  }\n  productVariant {\n    ...ProductVariant\n    __typename\n  }\n  cancelledAt\n  insertedAt\n  updatedAt\n  usdPrice: price(currency: \"USD\")\n  usdTotalPrice: totalPrice(currency: \"USD\")\n  __typename\n}\n\nfragment ShopifyOrderLineItem on ShopifyOrderLineItem {\n  id\n  name\n  __typename\n}\n\nfragment MarketplaceOrder on MarketplaceOrder {\n  id\n  quantity\n  status\n  marketplaceOrderStatus\n  marketplaceLogisticsStatus\n  currency\n  price\n  subtotalPrice\n  totalPrice\n  shippingFee\n  shippingMethod\n  retailCurrency\n  retailPrice\n  retailShippingFee\n  retailSubtotalPrice\n  retailTotalPrice\n  marketplace\n  marketplaceId\n  marketplaceAccountId\n  marketplaceError\n  marketplaceErrorMessage\n  payloadOverrides {\n    ...MarketplaceOrderPayload\n    __typename\n  }\n  shippingAddress {\n    ...Address\n    __typename\n  }\n  shipments(first: 5) {\n    pageInfo {\n      ...PageInfo\n      __typename\n    }\n    edges {\n      node {\n        ...Shipment\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  processedAt\n  lastRefetchAt\n  insertedAt\n  updatedAt\n  __typename\n}\n\nfragment MarketplaceOrderPayload on MarketplaceOrderPayload {\n  accountEmail\n  force\n  itemId\n  propertyValueIds\n  productUrl\n  quantity\n  retailProductPriceCents\n  shippingFeeCents\n  address {\n    ...MarketplaceOrderPayloadAddress\n    __typename\n  }\n  __typename\n}\n\nfragment MarketplaceOrderPayloadAddress on MarketplaceOrderPayloadAddress {\n  address1\n  address2\n  city\n  zip\n  province\n  countryCode\n  mobileNumber\n  mobileNumberCountryPrefix\n  __typename\n}\n\nfragment Shipment on Shipment {\n  id\n  trackingNumber\n  lastMileCarrierTrackingNumber\n  shippingMethodHandle\n  shippingDays\n  lastEventDescription\n  lastEventStatus\n  lastRefetchAt\n  insertedAt\n  updatedAt\n  __typename\n}\n\nfragment Product on Product {\n  id\n  publishStatus\n  publishError\n  marketplaceProductUrl\n  deletedAt\n  deleteNote\n  deleteReason\n  quarantineType\n  quarantinedAt\n  insertedAt\n  updatedAt\n  productCompareAtPriceRange {\n    ...ProductPriceRange\n    __typename\n  }\n  productPriceRange {\n    ...ProductPriceRange\n    __typename\n  }\n  productTranslations {\n    ...ProductTranslation\n    __typename\n  }\n  productImages {\n    ...ProductImage\n    __typename\n  }\n  __typename\n}\n\nfragment ProductPriceRange on ProductPriceRange {\n  minVariantPrice\n  maxVariantPrice\n  __typename\n}\n\nfragment ProductTranslation on ProductTranslation {\n  id\n  language\n  title\n  description @include(if: $includeProductDescription)\n  __typename\n}\n\nfragment ProductImage on ProductImage {\n  id\n  src: marketplaceSrc\n  imageSrc\n  position\n  __typename\n}\n\nfragment ProductVariant on ProductVariant {\n  id\n  marketplaceId\n  position\n  sku\n  barcode\n  price\n  compareAtPrice\n  stockLevel\n  productImage {\n    ...ProductImage\n    __typename\n  }\n  updatedAt\n  insertedAt\n  __typename\n}\n\nfragment OrderEventConnection on OrderEventConnection {\n  edges {\n    node {\n      ...OrderEvent\n      __typename\n    }\n    __typename\n  }\n  pageInfo {\n    ...PageInfo\n    __typename\n  }\n  __typename\n}\n\nfragment OrderEvent on OrderEvent {\n  ...OrderFormattedShippingAddressEvent\n  ...OrderCommentEvent\n  ...OrderLabelEvent\n  ...MarketplaceOrderEvent\n  ...MarketplaceOrderFailedEvent\n  ...OrderLineItemEvent\n  ...OrderFinancialStatusEvent\n  ...EmailOrderEvent\n  __typename\n}\n\nfragment OrderFormattedShippingAddressEvent on OrderFormattedShippingAddressEvent {\n  id\n  type\n  value {\n    pre {\n      ...Address\n      __typename\n    }\n    post {\n      ...Address\n      __typename\n    }\n    __typename\n  }\n  orderFormattedShippingAddressActor: actor {\n    ...User\n    __typename\n  }\n  insertedAt\n  updatedAt\n  __typename\n}\n\nfragment User on User {\n  id\n  email\n  name\n  roles\n  updatedAt\n  insertedAt\n  __typename\n}\n\nfragment OrderCommentEvent on OrderCommentEvent {\n  id\n  type\n  value {\n    message\n    __typename\n  }\n  orderCommentActor: actor {\n    ...User\n    __typename\n  }\n  insertedAt\n  updatedAt\n  __typename\n}\n\nfragment OrderLabelEvent on OrderLabelEvent {\n  id\n  type\n  value {\n    action\n    orderLabel {\n      ...OrderLabel\n      __typename\n    }\n    __typename\n  }\n  orderLabelActor: actor {\n    ...User\n    __typename\n  }\n  insertedAt\n  updatedAt\n  __typename\n}\n\nfragment OrderLabel on OrderLabel {\n  id\n  color\n  handle\n  title\n  insertedAt\n  updatedAt\n  __typename\n}\n\nfragment MarketplaceOrderEvent on MarketplaceOrderEvent {\n  id\n  type\n  value {\n    message\n    __typename\n  }\n  marketplaceOrderActor: actor {\n    ...User\n    __typename\n  }\n  orderLineItem {\n    ...SimpleOrderLineItem\n    __typename\n  }\n  marketplaceOrder {\n    ...MarketplaceOrder\n    __typename\n  }\n  insertedAt\n  updatedAt\n  __typename\n}\n\nfragment SimpleOrderLineItem on OrderLineItem {\n  id\n  price\n  totalPrice\n  barcode\n  quantity\n  status\n  fulfillmentStatus\n  shopifyOrderLineItem {\n    ...ShopifyOrderLineItem\n    __typename\n  }\n  product {\n    ...Product\n    __typename\n  }\n  productVariant {\n    ...ProductVariant\n    __typename\n  }\n  cancelledAt\n  insertedAt\n  updatedAt\n  __typename\n}\n\nfragment MarketplaceOrderFailedEvent on MarketplaceOrderFailedEvent {\n  id\n  type\n  value {\n    errorCode\n    errorMessage\n    errorHint\n    __typename\n  }\n  orderLineItem {\n    ...SimpleOrderLineItem\n    __typename\n  }\n  marketplaceOrder {\n    ...MarketplaceOrder\n    __typename\n  }\n  insertedAt\n  updatedAt\n  __typename\n}\n\nfragment OrderLineItemEvent on OrderLineItemEvent {\n  id\n  type\n  value {\n    message\n    __typename\n  }\n  orderLineItemActor: actor {\n    ...User\n    __typename\n  }\n  orderLineItem {\n    ...SimpleOrderLineItem\n    __typename\n  }\n  insertedAt\n  updatedAt\n  __typename\n}\n\nfragment OrderFinancialStatusEvent on OrderFinancialStatusEvent {\n  id\n  type\n  value {\n    gateway\n    oldFinancialStatus\n    newFinancialStatus\n    paynlTransactionId\n    currency\n    amount\n    __typename\n  }\n  financialStatusActor: actor {\n    ...User\n    __typename\n  }\n  insertedAt\n  updatedAt\n  __typename\n}\n\nfragment EmailOrderEvent on EmailOrderEvent {\n  id\n  type\n  emailMessage {\n    ...EmailMessage\n    __typename\n  }\n  insertedAt\n  updatedAt\n  __typename\n}\n\nfragment EmailMessage on EmailMessage {\n  id\n  sender\n  recipient\n  subject\n  htmlBody\n  sentAt\n  status\n  templateName\n  insertedAt\n  updatedAt\n  __typename\n}\n\nfragment OrderLink on OrderLink {\n  id\n  type\n  url\n  params {\n    ticketId\n    __typename\n  }\n  insertedAt\n  updatedAt\n  __typename\n}\n",
'SearchOrdersAndProduct' : "query SearchOrdersAndProduct($ordersQuery: String!, $productQuery: String!, $includeProductDescription: Boolean = false, $ordersFirst: Int, $ordersLast: Int, $ordersBefore: String, $ordersAfter: String) {\n  orders: searchOrders(\n    query: $ordersQuery\n    first: $ordersFirst\n    last: $ordersLast\n    before: $ordersBefore\n    after: $ordersAfter\n  ) {\n    pageInfo {\n      ...PageInfo\n      __typename\n    }\n    edges {\n      node {\n        ...OrderSimple\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  product: productSearch(query: $productQuery) {\n    ...Product\n    __typename\n  }\n}\n\nfragment PageInfo on PageInfo {\n  hasNextPage\n  hasPreviousPage\n  startCursor\n  endCursor\n  __typename\n}\n\nfragment OrderSimple on Order {\n  id\n  name\n  email\n  customerName\n  status\n  fulfillmentStatus\n  financialStatus\n  __typename\n}\n\nfragment Product on Product {\n  id\n  publishStatus\n  publishError\n  marketplaceProductUrl\n  deletedAt\n  deleteNote\n  deleteReason\n  quarantineType\n  quarantinedAt\n  insertedAt\n  updatedAt\n  productCompareAtPriceRange {\n    ...ProductPriceRange\n    __typename\n  }\n  productPriceRange {\n    ...ProductPriceRange\n    __typename\n  }\n  productTranslations {\n    ...ProductTranslation\n    __typename\n  }\n  productImages {\n    ...ProductImage\n    __typename\n  }\n  __typename\n}\n\nfragment ProductPriceRange on ProductPriceRange {\n  minVariantPrice\n  maxVariantPrice\n  __typename\n}\n\nfragment ProductTranslation on ProductTranslation {\n  id\n  language\n  title\n  description @include(if: $includeProductDescription)\n  __typename\n}\n\nfragment ProductImage on ProductImage {\n  id\n  src: marketplaceSrc\n  imageSrc\n  position\n  __typename\n}\n"
}

if __name__ == "__main__":
    # failed orders example 
    print(get_payload(operationName='OrderList', variables={"ordersFirst" : 25}))
    
    # bucket roksolana example 
    print(get_payload(operationName='OrderList', variables={"ordersFirst" : 25, "orderLabelId":"T3JkZXJMYWJlbDo2"}))

    # autorization example
    print(get_payload(operationName='UserCreateAccessToken', variables={"input":{"email":"andrew@gmail.com","password":"Andrew"}}))

    # OrderLabels example
    print(get_payload(operationName='OrderLabels'))

    # OrderStatuses example
    print(get_payload(operationName='OrderStatuses'))