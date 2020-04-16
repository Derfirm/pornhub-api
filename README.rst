===============================
Unofficial api for pornhub.com
===============================

Key Features
============
- response are fully-annotated with pydantic_
- rest without parsing

.. _pydantic: https://pydantic-docs.helpmanual.io/

Getting started
===============
Initiate Api client
___________________
.. code-block:: python

    from pornhub_api import PornhubApi

    api = PornhubApi()


Search Videos
_____________
.. code-block:: python

    data = api.search(
        "chechick",
        ordering="mostviewed",
        period="weekly",
        tags=["black"],
    )
    for vid in data.videos:
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

   active = api.video.is_active("ph560b93077ddae")


Search video by random tag and category
_______________________________________
.. code-block:: python


    import random
    api = PornhubApi()

    tags = random.sample(api.video.tags("f").tags, 5)
    category = random.choice(api.video.categories().categories)
    result = api.search.search(ordering="mostviewed", tags=tags, category=category)

    print(result.size())
    for vid in result.videos:
        print(vid.title, vid.url)
