def get_or_set_multiple_cache(keys, defaults, timeout=DEFAULT_CACHE_TIMEOUT, function_args=None, function_kwargs=None):
    pipeline = redis_client.pipeline()
    # Get values from cache
    for key in keys:
        pipeline.get(key)
    # Check which values are missing from cache and set them
    missing_indices = []
    for i, result in enumerate(pipeline.execute()):
        if result is None:
            missing_indices.append(i)
    if missing_indices:
        for i in missing_indices:
            key = keys[i]
            default = defaults[i]
            if type(default).__name__ == 'function':
                result = default(*function_args or (), **function_kwargs or {})
                pipeline.set(key, result, timeout)
                defaults[i] = result  # Update defaults with actual value
            else:
                pipeline.set(key, default, timeout)
        # Execute pipeline to set missing values in cache
        pipeline.execute()
    # Create dictionary with key-value pairs
    result_dict = {}
    for i, key in enumerate(keys):
        result_dict[key] = defaults[i] if defaults[i] is not None else redis_client.get(key)
    return result_dict
