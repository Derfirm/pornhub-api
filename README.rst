===============================
Unofficial api for pornhub.com
===============================

.. image:: https://travis-ci.org/derfirm/pornhub-api.svg?branch=master
    :target: https://travis-ci.org/derfirm/pornhub-api

.. image:: https://api.codacy.com/project/badge/Grade/72b5baaa2a7d438cbe725924954a62b2
    :target: https://www.codacy.com/manual/Derfirm/pornhub-api

.. image:: https://img.shields.io/pypi/v/pornhub-api.svg
    :target: https://pypi.python.org/pypi/pornhub-api


Key Features
____________
- response are fully-annotated with pydantic_
- rest without parsing

.. _pydantic: https://pydantic-docs.helpmanual.io/


Installing
__________
.. code:: bash

    $ pip install pornhub-api

or with aiohttp support

.. code:: bash

    $ pip install pornhub-api[aiohttp-backend]

or with httpx support

.. code:: bash

    $ pip install pornhub-api[httpx-backend]

Supported versions
__________________
- Python 3.7+


Getting started
===============
Initiate Api client
___________________
.. code-block:: python

    from pornhub_api import PornhubApi

    api = PornhubApi()

Initiate with AioHttp backend
_____________________________

.. code-block:: python

    import asyncio
    from pornhub_api.backends.aiohttp import AioHttpBackend


    async def execute():
        async with AioHttpBackend() as backend:
            api = PornhubApi(backend=backend)
            video = await api.video.get_by_id("ph560b93077ddae")
            print(video.title)

    asyncio.run(execute())


Search Videos
_____________
.. code-block:: python

    videos = api.search_videos.search_videos(
        "chechick",
        ordering="mostviewed",
        period="weekly",
        tags=["black"],
    )
    for vid in videos:
        print(vid.title, vid.video_id)

Get Stars
___________
.. code-block:: python

    api.stars.all()
    or
    api.stats.all_detailed()



Get single Video details
________________________
.. code-block:: python

   video = api.video.get_by_id("ph560b93077ddae")
   print(video.title)


Get all videos tags or categories
_________________________________
.. code-block:: python

   categories = api.video.categories()
   tags = api.video.tags("a")


Check Video availability
_________________________
.. code-block:: python

   response = api.video.is_active("ph560b93077ddae")
   print(response.is_active)


Search video by random tag and category
_______________________________________
.. code-block:: python


    import random
    api = PornhubApi()

    tags = random.sample(api.video.tags("f").tags, 5)
    category = random.choice(api.video.categories().categories)
    result = api.search.search_videos(ordering="mostviewed", tags=tags, category=category)

    print(result.size())
    for vid in result:
        print(vid.title, vid.url)
