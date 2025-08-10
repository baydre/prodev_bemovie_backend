# Redis Cache Issue Investigation and Fix

## Problem Identified

Your Django application was experiencing Redis cache errors in production due to a configuration mismatch between development and production environments.

### Root Causes

1. **Hardcoded Redis URL**: The `settings.py` file had a hardcoded Redis location (`redis://127.0.0.1:6379/1`) instead of using environment variables.

2. **Environment Variable Not Used**: While your `.env.production` file defined `REDIS_URL`, the settings weren't configured to use this environment variable.

3. **Missing Local Environment Variable**: The local `.env` file was missing the `REDIS_URL` variable.

4. **No Error Handling**: Cache operations lacked error handling, making the application fragile when Redis connectivity issues occur.

## Solutions Implemented

### 1. Dynamic Redis Configuration ✅
**File**: `movie_rec_project/settings.py`
```python
# Before
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',  # Hardcoded!
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# After
REDIS_URL = env('REDIS_URL', default='redis://127.0.0.1:6379/1')

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_URL,  # Now uses environment variable
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

### 2. Enhanced Error Handling ✅
**File**: `movies/views.py`

Added safe cache operations with comprehensive error handling:
```python
def safe_cache_get(key):
    """Safely get data from cache with error handling"""
    try:
        return cache.get(key)
    except Exception as e:
        logger.warning(f"Cache get failed for key '{key}': {e}")
        return None

def safe_cache_set(key, value, timeout):
    """Safely set data in cache with error handling"""
    try:
        cache.set(key, value, timeout)
    except Exception as e:
        logger.warning(f"Cache set failed for key '{key}': {e}")
```

All cache operations in views now use these safe methods, ensuring the application continues to function even if Redis is unavailable.

### 3. Updated Environment Configuration ✅
**File**: `.env`
```
REDIS_URL=redis://127.0.0.1:6379/1
```

### 4. Redis Connectivity Testing Tool ✅
**File**: `movies/management/commands/test_redis.py`

Created a management command to test Redis connectivity:
```bash
python manage.py test_redis
```

This command tests:
- Basic connectivity (set/get/delete operations)
- Performance benchmarks
- Configuration validation

## Environment-Specific Configuration

### Development
- **Redis URL**: `redis://127.0.0.1:6379/1` (local Redis instance)
- **File**: `.env`

### Production (Render)
- **Redis URL**: `redis://red-xxxxxxxxxxxxx:6379/1` (Render Redis service)
- **File**: `.env.production` or environment variables in Render dashboard
- **Configuration**: Automatically provided via `render.yaml`

## Testing the Fix

### Local Testing
```bash
# Test Redis connectivity
python manage.py test_redis

# Test Django shell
python manage.py shell -c "from django.core.cache import cache; cache.set('test', 'works'); print(cache.get('test'))"
```

### Production Testing
After deployment, run:
```bash
python manage.py test_redis
```

## Benefits of This Fix

1. **Environment Agnostic**: Works seamlessly across development, staging, and production
2. **Graceful Degradation**: Application continues to work even if Redis is temporarily unavailable
3. **Better Monitoring**: Cache errors are logged for debugging
4. **Easy Testing**: Management command for quick connectivity verification
5. **Production Ready**: Uses proper environment variable configuration

## Deployment Instructions

1. **Ensure Environment Variables**: Make sure `REDIS_URL` is set in your production environment
2. **Deploy Changes**: Deploy the updated code to production
3. **Test Connectivity**: Run `python manage.py test_redis` after deployment
4. **Monitor Logs**: Check application logs for any cache-related warnings

## Monitoring

With the new error handling, cache failures will be logged as warnings but won't crash the application. Monitor your logs for messages like:
```
Cache get failed for key 'trending_movies': [connection error details]
```

This indicates Redis connectivity issues that need investigation.
