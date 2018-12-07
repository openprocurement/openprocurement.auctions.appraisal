.. . Kicking page rebuild 2014-10-30 17:00:08
.. include:: defs.hrst

.. index:: Auction, Auction
.. _auction:

Auction
=======

Schema
------

:id:
  uuid, auto-generated, read-only

  Internal id of procedure.

:auctionID:
  string, auto-generated, read-only

  The auction identifier to refer auction to in "paper" documentation. 

  |ocdsDescription|
  It is included to make the flattened data structure more convenient.

:date:
  :ref:`date`, auto-generated, read-only

  The date of the procedure creation/undoing.

:owner:
  string, auto-generated, read-only

  The entity whom the procedure has been created by.

:lotIdentifier:
  string, required

  The identifier of a lot, which is to be privatized, within the Registry.

:title:
  string, multilingual, required

  * Ukrainian by default (required) - Ukrainian title

  * ``title_en`` (English) - English title

  * ``title_ru`` (Russian) - Russian title

  Oprionally can be mentioned in English/Russian.

  The name of the auction, displayed in listings. 
 
:description:
  string, multilingual, required

  |ocdsDescription|
  A description of the goods, services to be provided.

  * Ukrainian by default - Ukrainian decription

  * ``decription_en`` (English) - English decription

  * ``decription_ru`` (Russian) - Russian decription

:tenderAttempts:
  integer, optional

  The number which represents what time procedure with a current lot takes place.

:procurementMethod:
  string, auto-generated, read-only

  Purchase method. The only value is “open”.

:procurementMethodType:
  string, read-only

  Type of the procedure within the auction announcement. The given value is `appraisal.insider`. 

:procurementMethodDetails:
  string, auto-generated, optional

  Parameter that accelerates auction periods. Set quick, accelerator=1440 as text value for procurementMethodDetails for the time frames to be reduced in 1440 times.

:submissionMethod:
  string, auto-generated, read-only

  The given value is `electronicAuction`.

:submissionMethodDetails:
  string, optional

  Parameter that works only with mode = “test” and speeds up auction start date.

:procuringEntity:
  :ref:`ProcuringEntity`, required

  Organization conducting the auction.

  |ocdsDescription|
  The entity managing the procurement, which may be different from the buyer who is paying / using the items being procured.

:auctionParameters:
  :ref:`Auction_Parameters`, auto-generated, read-only

  The parameters that indicates the major specifications of the procedure.

:contractTerms:
  :ref:`contractTerms`, required

  The parameters that indicates the major specifications of the contract.

:value:
  :ref:`value`, required

  |ocdsDescription|
  The total estimated value of the procurement.

:minimalStep:
  :ref:`value`, required

  Auction step (increment). `minimalStep.value` that will be always automatically set is 0. Validation rules:

  * `amount` should be greater than `Auction.value.amount`
  * `currency` should either be absent or match `Auction.value.currency`
  * `valueAddedTaxIncluded` should either be absent or match `Auction.value.valueAddedTaxIncluded`

:guarantee:
  :ref:`Guarantee`, required

  The assumption of responsibility for payment of performance of some obligation if the liable party fails to perform to expectations.

:registrationFee:
  :ref:`Guarantee`, required

  The sum of money required to enroll on an official register.

:bankAccount:
  :ref:`Bank_Account`, optional

  Details which uniquely identify a bank account, and are used when making or receiving a payment.

:items:
  Array of :ref:`item` objects, required

  List that contains single item being sold. 

  |ocdsDescription|
  The goods and services to be purchased, broken into line items wherever possible. Items should not be duplicated, but a quantity of 2 specified instead.

:documents:
  Array of :ref:`document` objects, optional
 
  |ocdsDescription|
  All documents and attachments related to the auction.

:dateModified:
  :ref:`date`, auto-generated, read-only

  |ocdsDescription|
  Date when the auction was last modified.

:questions:
  Array of :ref:`question` objects, optional

  Questions to `procuringEntity` and answers to them.

:bids:
  Array of :ref:`bid` objects, optional (required for the process to be succsessful)

  A list of all bids placed in the auction with information about participants, their proposals and other qualification documentation.

  |ocdsDescription|
  A list of all the companies who entered submissions for the auction.

:awards:
  Array of :ref:`award` objects

  All qualifications (disqualifications and awards).

:awardCriteria:
  string, auto-generated, read-only

  The given value is `highestCost`.

:contracts:
  Array of :ref:`Contract` objects

  |ocdsDescription|
  Information on contracts signed as part of a process.

:cancellations:
  Array of :ref:`cancellation` objects, optional

  Contains 1 object with `active` status in case of cancelled Auction.

  The :ref:`cancellation` object describes the reason of auction cancellation and contains accompanying
  documents  if there are any.

:auctionUrl:
  url, auto-generated, read-only

  A web address where auction is accessible for view.

:status:
  string, required

+-------------------------+--------------------------------------+
|        Status           |            Description               |
+=========================+======================================+
| `draft`                 | draft of procedure                   |
+-------------------------+--------------------------------------+
| `active.tendering`      | tendering period (tendering)         |
+-------------------------+--------------------------------------+
| `active.auction`        | auction period (auction)             |
+-------------------------+--------------------------------------+
| `active.qualification`  | winner qualification (qualification) |
+-------------------------+--------------------------------------+
| `active.awarded`        | standstill period (standstill)       |
+-------------------------+--------------------------------------+
| `unsuccessful`          | unsuccessful auction (unsuccessful)  |
+-------------------------+--------------------------------------+
| `complete`              | complete auction (complete)          | 
+-------------------------+--------------------------------------+
| `cancelled`             | cancelled auction (cancelled)        |
+-------------------------+--------------------------------------+

:enquiryPeriod:
  :ref:`period`, auto-generated, read-only

  Period when questions are allowed.

  |ocdsDescription|
  The period during which enquiries may be made and will be answered.

:tenderPeriod:
  :ref:`period`, auto-generated, read-only

  Period when bids can be submitted.

  |ocdsDescription|
  The period when the auction is open for submissions. The end date is the closing date for auction submissions.

:auctionPeriod:
  :ref:`period`, auto-generated, read-only (required for ``auctionPeriod.startDate``)

  Period when Auction is conducted. `startDate` should be provided.

:awardPeriod:
  :ref:`period`, auto-generated, read-only

  Awarding process period.

  |ocdsDescription|
  The date or period on which an award is anticipated to be made.

:mode: 
  string, optional

  The additional parameter with a value `test`.

.. _Auction_Parameters:

Auction Parameters
==================

Schema
------

:type:
  string, auto-generated, read-only

  Type of the auction.
:dutchSteps:
  integer, optional

  Number of steps within the Dutch auction phase. 

.. _Bank_Account:

Bank Account
============

Schema
------

:description:
  string, multilingual, optional

  Additional information that has to be noted from the Organizer point.

  * Ukrainian by default - Ukrainian decription
    
    * ``decription_en`` (English) - English decription
    
    * ``decription_ru`` (Russian) - Russian decription

:bankName:  
  string, required

  Name of the bank.

:accountIdentification:
  Array of :ref:`classification`, required

  Major data on the account details of the state entity selling a lot, to facilitate payments at the end of the process.

  Most frequently used are:

  * 'UA-EDR';
  * 'UA-MFO';
  * 'accountNumber'.
