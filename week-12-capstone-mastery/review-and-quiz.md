# Week 12 — Final 50-Question Defense

## Video / media

1. Why separate upload control plane from data plane?
2. Why are resumable uploads valuable?
3. Why transcode asynchronously?
4. Why create several media renditions?
5. What workload makes CDN central?
6. What is origin shielding?
7. What happens when one rendition fails?
8. How can readiness metadata become inconsistent with media artifacts?

## Feed

9. Fan-out-on-write?
10. Fan-out-on-read?
11. Main cost of fan-out-on-write?
12. Main cost of fan-out-on-read?
13. Why use a hybrid strategy for celebrities?
14. Is feed cache authoritative?
15. How should deleted posts propagate?

## Geospatial/realtime

16. Why spatial indexing?
17. What is a hot spatial cell?
18. How stale may driver location be?
19. Why must match ownership be stronger than location freshness?
20. What happens when mobile connectivity drops?
21. Why partition by city/region?

## Sync/storage

22. Why separate file content from metadata?
23. Why immutable blocks?
24. Why content hashes?
25. Why is offline operation effectively a network partition?
26. Name three conflict policies.
27. What if block upload succeeds but metadata commit fails?
28. How are unreferenced blocks eventually cleaned?

## Streaming

29. Why does aggregate bitrate matter more than API RPS?
30. What is content pre-positioning?
31. Why might a premiere be easier to forecast but harder to absorb?
32. Tradeoff of many bitrate renditions?
33. What happens when an edge cache fails?

## Final transcription

34. 100k media hours/day equals how many one-minute chunks/day?
35. Approximately how many one-minute chunks/sec average?
36. If each takes 15s, roughly how much average concurrency?
37. What does deterministic chunk artifact naming buy you?
38. Why is broker delivery state not business source of truth?
39. How do you avoid double billing on redelivery?
40. What metric should scale workers?
41. What protects one tenant from monopolizing workers?
42. Why might PostgreSQL remain the right core DB?
43. When might partitioning become useful?
44. What requirement would justify Kafka over a simple work queue?
45. What requirement might justify Temporal/managed orchestration?
46. What are your top five cost drivers?
47. What must GDPR discussion include beyond “EU server”?
48. How do you prove a failed job recovered?
49. What does a good architecture revisit trigger look like?
50. What is the System Design Ninja mindset?
