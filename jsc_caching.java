import org.apache.jcs.JCS;
import org.apache.jcs.access.exception.CacheException;
import java.util.List;

public class CacheList {
    private static final String CACHE_REGION = "myCacheRegion";

    public static void cache(List<Object[]> list) throws CacheException {
        JCS cache = JCS.getInstance(CACHE_REGION);
        cache.put("myList", list);
    }

    public static List<Object[]> getCachedList() throws CacheException {
        JCS cache = JCS.getInstance(CACHE_REGION);
        return (List<Object[]>) cache.get("myList");
    }
}
