# Example from: docs\plans\citation_system\00_master_roadmap.md
# Index: 1
# Runnable: True
# Hash: d882ca7d

# Mitigation: Exponential backoff with checkpoint recovery
if response.status == 429:
    sleep_time = min(2 ** retry_count, 300)  # Cap at 5 minutes
    await asyncio.sleep(sleep_time)

    # Save checkpoint every 50 claims
    if claim_count % 50 == 0:
        save_checkpoint(f'checkpoint_{claim_count}.json')