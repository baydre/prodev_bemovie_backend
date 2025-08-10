from django.core.management.base import BaseCommand
from django.core.cache import cache
from django.conf import settings
import time


class Command(BaseCommand):
    help = 'Test Redis cache connectivity and performance'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Testing Redis connectivity...'))
        
        # Display current configuration
        cache_config = settings.CACHES['default']
        self.stdout.write(f"Redis Backend: {cache_config['BACKEND']}")
        self.stdout.write(f"Redis Location: {cache_config['LOCATION']}")
        
        try:
            # Test basic connectivity
            test_key = 'redis_test_key'
            test_value = f'test_value_{int(time.time())}'
            
            self.stdout.write('Testing cache set operation...')
            cache.set(test_key, test_value, 30)
            
            self.stdout.write('Testing cache get operation...')
            retrieved_value = cache.get(test_key)
            
            if retrieved_value == test_value:
                self.stdout.write(
                    self.style.SUCCESS('✓ Redis connectivity test PASSED')
                )
            else:
                self.stdout.write(
                    self.style.ERROR(f'✗ Redis connectivity test FAILED - Expected: {test_value}, Got: {retrieved_value}')
                )
                return
            
            # Test cache deletion
            self.stdout.write('Testing cache delete operation...')
            cache.delete(test_key)
            deleted_check = cache.get(test_key)
            
            if deleted_check is None:
                self.stdout.write(
                    self.style.SUCCESS('✓ Redis delete operation test PASSED')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'⚠ Redis delete test issue - Value still exists: {deleted_check}')
                )
            
            # Test performance
            self.stdout.write('Testing cache performance...')
            start_time = time.time()
            
            for i in range(100):
                cache.set(f'perf_test_{i}', f'value_{i}', 60)
            
            set_time = time.time() - start_time
            
            start_time = time.time()
            
            for i in range(100):
                cache.get(f'perf_test_{i}')
            
            get_time = time.time() - start_time
            
            self.stdout.write(f'Performance: 100 SET operations took {set_time:.3f}s')
            self.stdout.write(f'Performance: 100 GET operations took {get_time:.3f}s')
            
            # Cleanup
            for i in range(100):
                cache.delete(f'perf_test_{i}')
            
            self.stdout.write(
                self.style.SUCCESS('✓ All Redis tests completed successfully!')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'✗ Redis connectivity test FAILED with error: {e}')
            )
            self.stdout.write(
                self.style.WARNING('This may indicate Redis server is not running or configuration is incorrect.')
            )
