.. . Kicking page rebuild 2014-10-30 17:00:08
.. include:: defs.hrst

.. index:: Award
.. _award:

Award
=====

Schema
------

:id:
    string, auto-generated, read-only
    
    |ocdsDescription|
    Identifier for this award.
    
:bid_id:
    string, auto-generated, read-only

    The ID of a bid that the award relates to.
    
:status:
    string, required
    
    |ocdsDescription|
    The current status of the award drawn from the `awardStatus` codelist.

    Possible values are:

    * `pending.verification` - the procedure awaits the auction protocol to be uploaded
    * `pending.payment` - the procedure awaits the payment to be made
    * `unsuccessful` - the award has been rejected by the qualification committee (bank)
    * `active` - the auction is awarded to the bidder from the `bid_id`
    * `pending.waiting` - the second bidder awaits the first bidder to be disqualified
    * `cancelled` - the second bidder does not want to wait for the first bidder to be disqualified

:verificationPeriod:
    :ref:`period`, auto-generated, read-only
    
    The period of uploading (for the auction winner) and verification (for the bank) of the auction protocol
    
:signingPeriod:
    :ref:`period`, auto-generated, read-only

    The period for the contract to be activated in the system (by the bank)
    
:date:
    string, :ref:`Date`, auto-generated, read-only
    
    |ocdsDescription|
    The date of the contract award.
    
:value:
    `Value` object, auto-generated, read-only
    
    |ocdsDescription|
    The total value of this award.
    
:suppliers:
    Array of :ref:`Organization` objects, auto-generated, read-only
    
    |ocdsDescription|
    The suppliers awarded with this award.
    
:items:
    Array of :ref:`Item` objects, auto-generated, read-only
    
    |ocdsDescription|
    The goods and services awarded in this award, broken into line items wherever possible. Items should not be duplicated, but the quantity should be specified instead. 
    
:documents:
    Array of :ref:`Document` objects, required
    
    |ocdsDescription|
    All documents and attachments related to the award, including any notices. 
