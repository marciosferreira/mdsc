# Relações entre Tabelas — Schema `brazil`

## Fluxo Principal

`file_import` → `purchase_order` → `order_item` ← `product` / `accessory`
`customer` ← `city` ← `public.country`

---

## Chaves Estrangeiras por Tabela

### alert_resolve
| Coluna | Referencia |
|---|---|
| `customer_id` | `brazil.customer.id` |
| `file_import_id` | `brazil.file_import.id` |
| `purchase_order_id` | `brazil.purchase_order.id` |

### alert_resolve_error_type
| Coluna | Referencia |
|---|---|
| `alert_resolve_id` | `brazil.alert_resolve.id` |
| `error_type_id` | `brazil.error_type.id` |

### city
| Coluna | Referencia |
|---|---|
| `country_id` | `public.country.id` |

### code_association
| Coluna | Referencia |
|---|---|
| `customer_group_id` | `brazil.customer_group.id` |

### customer
| Coluna | Referencia |
|---|---|
| `city_id` | `brazil.city.id` |

### order_item
| Coluna | Referencia |
|---|---|
| `purchase_order_id` | `brazil.purchase_order.id` |
| `product_id` | `brazil.product.id` |
| `product_id` | `mexico.product.id` |
| `accessory_id` | `brazil.accessory.id` |
| `accessory_id` | `mexico.accessory.id` |
| `error_type_id` | `brazil.error_type.id` |

### product_accessory
| Coluna | Referencia |
|---|---|
| `product_id` | `brazil.product.id` |
| `accessory_id` | `brazil.accessory.id` |

### purchase_order
| Coluna | Referencia |
|---|---|
| `customer_id` | `brazil.customer.id` |
| `file_import_id` | `brazil.file_import.id` |
| `file_import_id` | `mexico.file_import.id` |

---

## Diagrama (texto)

```
public.country
    └──→ brazil.city.country_id
              └──→ brazil.customer.city_id
                        └──→ brazil.purchase_order.customer_id
                        └──→ brazil.alert_resolve.customer_id

brazil.file_import
    └──→ brazil.purchase_order.file_import_id
              └──→ brazil.order_item.purchase_order_id
              └──→ brazil.alert_resolve.purchase_order_id
    └──→ brazil.alert_resolve.file_import_id

brazil.product ──────────────────┬──→ brazil.order_item.product_id
brazil.accessory ─────────────────┤──→ brazil.order_item.accessory_id
                                  └──→ brazil.product_accessory

brazil.error_type ───────────────┬──→ brazil.order_item.error_type_id
                                  └──→ brazil.alert_resolve_error_type.error_type_id

brazil.alert_resolve ────────────────→ brazil.alert_resolve_error_type.alert_resolve_id

brazil.customer_group ───────────────→ brazil.code_association.customer_group_id

mexico.product ──────────────────────→ brazil.order_item.product_id
mexico.accessory ────────────────────→ brazil.order_item.accessory_id
mexico.file_import ──────────────────→ brazil.purchase_order.file_import_id
```

---

## Tabelas sem FK de entrada (raiz)

- `file_import`
- `customer_group`
- `error_type`
- `product`
- `accessory`
- `resolution_memory`
- `migrations`
