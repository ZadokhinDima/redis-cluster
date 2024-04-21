# Redis

## Eviction strategies.
To test eviction strategies I've limited the memory of redis nodes to 5 mb. This allows to store <40k records. 

The script stores 50k records. Each record has 30% chance of having no TTL. TTL is also random between 30 and 120 minutes. 
Also each recored will be read by the script random amount of times (0-10). All this data will be available in key of the record.
After storing all records the script will read for all keys and print which were evicted.

### noeviction
After filling the memory script failed with error:
`redis.exceptions.OutOfMemoryError: command not allowed when used memory > 'maxmemory'.`

### allkeys-lru
Evicted keys that were stored earlier. 
Evicted records with ttl of all ranges and those without ttl.
Also evicted records with different reads counts.
The end of the output:
```
Key 29474-no_ttl-0_reads was evicted
Key 29599-ttl_92-9_reads was evicted
Key 29697-no_ttl-0_reads was evicted
Key 29737-ttl_119-5_reads was evicted
Key 29757-no_ttl-9_reads was evicted
Key 29791-ttl_64-5_reads was evicted
Key 29836-ttl_56-10_reads was evicted
Key 29866-no_ttl-7_reads was evicted
Key 29941-ttl_37-0_reads was evicted
Key 29960-no_ttl-5_reads was evicted
Key 29970-no_ttl-10_reads was evicted
Key 30004-ttl_109-2_reads was evicted
Key 30060-no_ttl-0_reads was evicted
Key 30064-ttl_79-6_reads was evicted
Key 30075-ttl_68-5_reads was evicted
Key 30110-ttl_75-7_reads was evicted
```

### allkeys-lfu
Evicted keys of form all range indexes (last evicted   `49888-ttl_66-0_reads`).
No difference by ttl.

I expected that evicted keys would be with smaller read counts. However, there are evicted records with 10 reads.
Using search in console I found out that there are much less evicted records with 10 reads then with 0 reads. (There clearly is a corelation between read counts and the number of evicted keys).
The end of the output:
```
Key 49236-ttl_117-5_reads was evicted
Key 49243-ttl_43-0_reads was evicted
Key 49283-ttl_68-1_reads was evicted
Key 49340-ttl_68-0_reads was evicted
Key 49346-no_ttl-9_reads was evicted
Key 49384-no_ttl-7_reads was evicted
Key 49399-ttl_75-0_reads was evicted
Key 49470-ttl_81-5_reads was evicted
Key 49591-ttl_56-8_reads was evicted
Key 49603-ttl_52-3_reads was evicted
Key 49618-no_ttl-4_reads was evicted
Key 49631-ttl_105-0_reads was evicted
Key 49683-ttl_101-0_reads was evicted
Key 49690-ttl_103-7_reads was evicted
Key 49703-ttl_108-0_reads was evicted
Key 49733-ttl_40-2_reads was evicted
Key 49888-ttl_66-0_reads was evicted
```

### allkeys-random
As expected no clear pattern for evicted keys.
```
Key 49267-ttl_105-4_reads was evicted
Key 49466-no_ttl-10_reads was evicted
Key 49467-ttl_94-10_reads was evicted
Key 49563-ttl_108-10_reads was evicted
Key 49581-ttl_40-2_reads was evicted
Key 49656-ttl_43-1_reads was evicted
Key 49670-ttl_114-5_reads was evicted
Key 49721-ttl_72-0_reads was evicted
Key 49767-no_ttl-2_reads was evicted
```

### volatile-lru

Similar output to `allkeys-lru` but records with no ttl weren't evicted.
End of the output:
```
Key 34825-ttl_93-9_reads was evicted
Key 34828-ttl_42-8_reads was evicted
Key 34868-ttl_85-10_reads was evicted
Key 34884-ttl_49-5_reads was evicted
Key 34926-ttl_46-8_reads was evicted
Key 34934-ttl_72-3_reads was evicted
Key 34941-ttl_39-8_reads was evicted
Key 34946-ttl_85-8_reads was evicted
Key 34966-ttl_98-10_reads was evicted
Key 34974-ttl_39-9_reads was evicted
Key 35037-ttl_99-6_reads was evicted
Key 35075-ttl_112-0_reads was evicted
Key 35085-ttl_51-5_reads was evicted
Key 35178-ttl_72-9_reads was evicted
Key 35204-ttl_36-0_reads was evicted
Key 35231-ttl_101-6_reads was evicted
Key 35244-ttl_59-0_reads was evicted
Key 35461-ttl_106-8_reads was evicted
```

### volatile-lfu

Similar output to `allkeys-lfu` but records with no ttl weren't evicted.
End of the output:
```
Key 49404-ttl_39-0_reads was evicted
Key 49428-ttl_57-5_reads was evicted
Key 49443-ttl_41-0_reads was evicted
Key 49566-ttl_45-4_reads was evicted
Key 49574-ttl_113-3_reads was evicted
Key 49590-ttl_80-6_reads was evicted
Key 49645-ttl_56-6_reads was evicted
Key 49677-ttl_80-1_reads was evicted
Key 49687-ttl_100-4_reads was evicted
Key 49690-ttl_98-0_reads was evicted
Key 49735-ttl_45-1_reads was evicted
Key 49752-ttl_90-2_reads was evicted
```

### volatile-random

Similar output to `allkeys-random` but records with no ttl weren't evicted.
End of the output:
```
Key 49592-ttl_117-6_reads was evicted
Key 49643-ttl_105-4_reads was evicted
Key 49694-ttl_70-0_reads was evicted
Key 49700-ttl_39-1_reads was evicted
Key 49705-ttl_86-4_reads was evicted
Key 49729-ttl_36-10_reads was evicted
Key 49765-ttl_35-6_reads was evicted
Key 49944-ttl_85-7_reads was evicted
```

### volatile-ttl

Evicted records with ttl <= 93 minutes. 

```
Key 49522-ttl_85-1_reads was evicted
Key 49525-ttl_40-7_reads was evicted
Key 49540-ttl_81-5_reads was evicted
Key 49551-ttl_75-10_reads was evicted
Key 49552-ttl_51-1_reads was evicted
Key 49559-ttl_84-10_reads was evicted
Key 49616-ttl_88-3_reads was evicted
Key 49645-ttl_47-1_reads was evicted
Key 49646-ttl_89-8_reads was evicted
Key 49648-ttl_65-9_reads was evicted
Key 49649-ttl_70-1_reads was evicted
Key 49668-ttl_71-4_reads was evicted
Key 49725-ttl_83-7_reads was evicted
Key 49727-ttl_92-6_reads was evicted
Key 49744-ttl_55-7_reads was evicted
Key 49768-ttl_42-7_reads was evicted
Key 49846-ttl_61-10_reads was evicted
Key 49850-ttl_60-5_reads was evicted
Key 49928-ttl_77-5_reads was evicted
```

## Probablistic cache wrapper

To test cache implementation I wrote a script that retrieves value every 5 seconds and prints responses (Response contains info about ttl and recomputation status).

```
No recomputation. TTL: 53 seconds.
Recomputed with remaining 46 seconds.
No recomputation. TTL: 53 seconds.
Recomputed with remaining 46 seconds.
No recomputation. TTL: 53 seconds.
No recomputation. TTL: 46 seconds.
No recomputation. TTL: 39 seconds.
Recomputed with remaining 32 seconds.
No recomputation. TTL: 53 seconds.
No recomputation. TTL: 46 seconds.
Recomputed with remaining 39 seconds.
No recomputation. TTL: 53 seconds.
Recomputed with remaining 46 seconds.
No recomputation. TTL: 53 seconds.
Recomputed with remaining 46 seconds.
No recomputation. TTL: 53 seconds.
No recomputation. TTL: 46 seconds.
No recomputation. TTL: 39 seconds.
No recomputation. TTL: 32 seconds.
No recomputation. TTL: 25 seconds.
No recomputation. TTL: 18 seconds.
Recomputed with remaining 11 seconds.
No recomputation. TTL: 53 seconds.
No recomputation. TTL: 46 seconds.
Recomputed with remaining 39 seconds.
No recomputation. TTL: 53 seconds.
```

Probability of cache recomputation in the script is `1 - ttl / Initial ttl `
Worked fine for 5 secons delays, but if I make requests every second cache will be recomputed too early.

To increase/decrease cache recomputation probability it is possible to use exponencial functions: 
`1 - (ttl / Initial ttl) ** 2 ` to increase chance of cache recomputation
`1 - (ttl / Initial ttl) ** 0.5 ` to decrease chance of cache recomputation