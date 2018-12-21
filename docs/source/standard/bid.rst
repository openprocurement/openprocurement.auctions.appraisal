.. . Kicking page rebuild 2014-10-30 17:00:08

.. index:: Bid, Parameter, LotValue, bidder, participant, pretendent

.. _bid:

Bid
===

Schema
------

:tenderers:
    List of :ref:`Organization` objects, required

:date:
    string, :ref:`date`, auto-generated

    Date when bid has been submitted.

:id:
    uid, auto-generated

    Internal identifire of bid.

:status:
    string, required

    Possible values are:

    * `draft`
    * `active`

:value:
    :ref:`Value`, required

    Validation rules:

    * `amount` should be less than `Auction.value.amout`
    * `currency` should either be absent or match `Auction.value.currency`
    * `valueAddedTaxIncluded` should either be absent or match `Auction.value.valueAddedTaxIncluded`

:documents:
    Array of :ref:`Document`, optional

    All documents needed.

:participationUrl:
    URL, auto-generated

    A web address for participation in auction.

:qualified:
    bool, required

    Confirms the absence of grounds for refusal to participate. CDB accepts only true value.

:eligible:
    bool, optional 

    Confirms compliance of eligibility criteria set by the customer in the tendering documents. CDB accepts only true value.
