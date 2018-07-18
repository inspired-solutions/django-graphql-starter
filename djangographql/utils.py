def model_filter(queryset, where):
    if where is None:
        return queryset

    if where.get('AND'):
        queryset = model_filter(queryset, where.get('AND'))

    filters = {k: v for k, v in where.items() if (v is not None) and (k not in ['AND', 'OR'])}

    result = queryset.filter(**filters)

    if where.get('OR'):
        result = result.union(model_filter(queryset, where.get('OR')))

    return result


def token_exempt(func):
    func.token_exempt = True
    return func
