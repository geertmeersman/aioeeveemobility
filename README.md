# aioeeveemobility

Asynchronous library to communicate with the EEVEE Mobility API

[![maintainer](https://img.shields.io/badge/maintainer-Geert%20Meersman-green?style=for-the-badge&logo=github)](https://github.com/geertmeersman)
[![buyme_coffee](https://img.shields.io/badge/Buy%20me%20a%20Duvel-donate-yellow?style=for-the-badge&logo=buymeacoffee)](https://www.buymeacoffee.com/geertmeersman)
[![discord](https://img.shields.io/discord/1094198226493636638?style=for-the-badge&logo=discord)](https://discord.gg/s8JNwREmxV)

[![MIT License](https://img.shields.io/github/license/geertmeersman/aioeeveemobility?style=flat-square)](https://github.com/geertmeersman/aioeeveemobility/blob/master/LICENSE)

[![GitHub issues](https://img.shields.io/github/issues/geertmeersman/aioeeveemobility)](https://github.com/geertmeersman/aioeeveemobility/issues)
[![Average time to resolve an issue](http://isitmaintained.com/badge/resolution/geertmeersman/aioeeveemobility.svg)](http://isitmaintained.com/project/geertmeersman/aioeeveemobility)
[![Percentage of issues still open](http://isitmaintained.com/badge/open/geertmeersman/aioeeveemobility.svg)](http://isitmaintained.com/project/geertmeersman/aioeeveemobility)
[![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-brightgreen.svg)](https://github.com/geertmeersman/aioeeveemobility/pulls)

[![Python](https://img.shields.io/badge/Python-FFD43B?logo=python)](https://github.com/geertmeersman/aioeeveemobility/search?l=python)

[![github release](https://img.shields.io/github/v/release/geertmeersman/aioeeveemobility?logo=github)](https://github.com/geertmeersman/aioeeveemobility/releases)
[![github release date](https://img.shields.io/github/release-date/geertmeersman/aioeeveemobility)](https://github.com/geertmeersman/aioeeveemobility/releases)
[![github last-commit](https://img.shields.io/github/last-commit/geertmeersman/aioeeveemobility)](https://github.com/geertmeersman/aioeeveemobility/commits)
[![github contributors](https://img.shields.io/github/contributors/geertmeersman/aioeeveemobility)](https://github.com/geertmeersman/aioeeveemobility/graphs/contributors)
[![github commit activity](https://img.shields.io/github/commit-activity/y/geertmeersman/aioeeveemobility?logo=github)](https://github.com/geertmeersman/aioeeveemobility/commits/main)


## API Example

```python
"""Test for aioeeveemobility."""
from aioeeveemobility import EeveeMobilityClient

import asyncio
import json
import aiohttp

async def main():
    client = EeveeMobilityClient(
        "user@email.com",
        "yourpassword",
    )

    try:
        user = await client.request("user")
        print(f"Hello {user.get('first_name')}")
        fleets = await client.request(f"user/{user.get('id')}/fleets")
        for fleet in fleets:
            for entity in fleet.get('fleet').get('entities'):
                if entity.get('id') == fleet.get('entity_id'):
                    break
            print(f"Fleet: {fleet.get('fleet').get('name')}, {entity.get('name')} | Payout rate: {fleet.get('payout_rate').get('rate')} {fleet.get('payout_rate').get('currency_code')} {fleet.get('payout_rate').get('suffix')}")

        cars = await client.request(f"cars")
        for car in cars:
            print(f"Your car: {car.get('display_name')} {car.get('license')}")
            addresses = await client.request(f"cars/{car.get('id')}/addresses")
            print("Addresses:")
            for address in addresses:
                print(f" > {address.get('name')}: {address.get('location')}")
            events = await client.request(f"cars/{car.get('id')}/events")
            print("Events:")
            for event in events.get('data'):
                print(event)

    finally:
        await client.close_session()

asyncio.run(main())
```
