package marketer;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.web.bind.annotation.*;

@RestController
public class Controller {

    @Autowired
    private RedisTemplate<String, Object> redisTemplate;

    @GetMapping("/hello")
    public String hello() {
        return "Ciao dal server!";
    }

    @PostMapping("/set")
    public String setKey(@RequestParam String key, @RequestParam String value) {
        redisTemplate.opsForValue().set(key, value);
        return "Chiave impostata: " + key;
    }

    @GetMapping("/get")
    public String getKey(@RequestParam String key) {
        return "Valore: " + redisTemplate.opsForValue().get(key);
    }
}
