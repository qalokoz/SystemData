import org.apache.jcs.JCS;
import org.apache.jcs.access.exception.CacheException;
import java.util.List;

 /**
  * The cache method takes a List of Object arrays and stores it in a cache region called "myCacheRegion" 
  using the JCS library's put method. The getCachedList method retrieves the cached list from the same 
  cache region using the get method.

  Dependency
            <dependency>
                <groupId>org.apache.jcs</groupId>
                <artifactId>jcs</artifactId>
                <version>2.3</version>
            </dependency>

  */
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
