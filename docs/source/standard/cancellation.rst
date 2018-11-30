.. . Kicking page rebuild 2014-10-30 17:00:08
.. include:: defs.hrst

.. index:: Cancellation
.. _cancellation:

Cancellation
============

Schema
------

:id:
    uuid, auto-generated, read-only

    Internal identifier of the object within an array.

:reason:
    string, multilingual, required

    The reason, why auction is being cancelled.

:status:
    string, required

    Possible values are:
     :`pending`:
       Default. The request is being prepared.
     :`active`:
       Cancellation activated.

:documents:
    Array of :ref:`Document` objects, optional

    Documents accompanying the Cancellation: Protocol of Auction Committee
    with decision to cancel the Auction.

:date:
    string, :ref:`date`, auto-generated

    Cancellation date.

:cancellationOf:
    string, required

    Possible values are:

    * `auction`
