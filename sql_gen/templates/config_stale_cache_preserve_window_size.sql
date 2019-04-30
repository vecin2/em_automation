update FC_GLOBALS 
 set STRING_VALUE ='{{ no_of_days | description("Enter the number of days that would like to preserve the cache for. For example enter 0 if you want to delete all caches when running the batch processes CleanAllCacheState or InvalidateAllCaches") | default(30) }}'
 where name ='STALE_CACHE_PRESERVE_WINDOW_SIZE'

