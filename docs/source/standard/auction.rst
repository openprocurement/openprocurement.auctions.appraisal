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

:date:
  :ref:`date`, auto-generated, read-only

  The date of the procedure creation/undoing.

:owner:
  string, auto-generated, read-only

  The entity whom the procedure has been created by.
 
:merchandisingObject:
  string, read-only

  Originates from `lot.id <http://lotsloki.api-docs.registry.ea2.openprocurement.io/en/latest/standard/Lot.html>`_

  The identifier of a lot, which is to be privatized, within the Registry.

:title:
  string, multilingual, read-only

  * Ukrainian by default (required) - Ukrainian title

  * ``title_en`` (English) - English title

  * ``title_ru`` (Russian) - Russian title

  Oprionally can be mentioned in English/Russian.

  Originates from `lot.title <http://lotsloki.api-docs.registry.ea2.openprocurement.io/en/latest/standard/Lot.html>`_.

  The name of the auction, displayed in listings. 
 
:description:
  string, multilingual, read-only

  |ocdsDescription|
  A description of the goods, services to be provided.

  * Ukrainian by default - Ukrainian decription

  * ``decription_en`` (English) - English decription

  * ``decription_ru`` (Russian) - Russian decription

  Originates from `lot.description <http://lotsloki.api-docs.registry.ea2.openprocurement.io/en/latest/standard/Lot.html>`_.

:auctionID:
  string, auto-generated, read-only

  The auction identifier to refer auction to in "paper" documentation. 

  |ocdsDescription|
  It is included to make the flattened data structure more convenient.

:tenderAttempts:
  integer, read-only

  Originates from `auction.tenderAttempts <http://lotsloki.api-docs.registry.ea2.openprocurement.io/en/latest/standard/auction.html>`_.

  The number which represents what time procedure with a current lot takes place.

:procurementMethod:
  string, auto-generated, read-only

  Purchase method. The only value is “open”.

:procurementMethodType:
  string, read-only

  Originates from `auction.procurementMethodType <http://lotsloki.api-docs.registry.ea2.openprocurement.io/en/latest/standard/auction.html>`_.

  Type of the procedure within the auction announcement. The given value is `sellout.insider`. 

:procurementMethodDetails:
  string, read-only

  Originates from `auction.procurementMethodDetails <http://lotsloki.api-docs.registry.ea2.openprocurement.io/en/latest/standard/auction.html>`_.

  Parameter that accelerates auction periods. Set quick, accelerator=1440 as text value for procurementMethodDetails for the time frames to be reduced in 1440 times.

:submissionMethod:
  string, read-only

  The given value is `electronicAuction`.

:submissionMethodDetails:
  string, read-only

  Originates from `auction.submissionMethodDetails <http://lotsloki.api-docs.registry.ea2.openprocurement.io/en/latest/standard/auction.html>`_.

  Parameter that works only with mode = “test” and speeds up auction start date.

:procuringEntity:
  :ref:`ProcuringEntity`, read-only

  Originates from `lot.lotCustodian <http://lotsloki.api-docs.registry.ea2.openprocurement.io/en/latest/standard/organization.html>`_.

  Organization conducting the auction.

  |ocdsDescription|
  The entity managing the procurement, which may be different from the buyer who is paying / using the items being procured.

:auctionParameters:
  :ref:`Auction_Parameters`, read-only

  Originates from `auction.auctionParameters <http://lotsloki.api-docs.registry.ea2.openprocurement.io/en/latest/standard/auction.html>`_.

  The parameters that indicates the major specifications of the procedure.

:contractTerms:
  :ref:`contractTerms`, read-only

  Originates from `lot.items <http://lotsloki.api-docs.registry.ea2.openprocurement.io/en/latest/standard/Lot.html#contracts>`_.

  The parameters that indicates the major specifications of the contract.

:value:
  :ref:`value`, read-only

  Originates from `auction.value <http://lotsloki.api-docs.registry.ea2.openprocurement.io/en/latest/standard/auction.html>`_. 

  |ocdsDescription|
  The total estimated value of the procurement.

:minimalStep:
  :ref:`value`, read-only

  Auction step (increment). `minimalStep.value` that will be always automatically set is 0. Validation rules:

  * `amount` should be greater than `Auction.value.amount`
  * `currency` should either be absent or match `Auction.value.currency`
  * `valueAddedTaxIncluded` should either be absent or match `Auction.value.valueAddedTaxIncluded`

:guarantee:
  :ref:`Guarantee`, required

  Originates from `auction.guarantee <http://lotsloki.api-docs.registry.ea2.openprocurement.io/en/latest/standard/auction.html>`_.

  The assumption of responsibility for payment of performance of some obligation if the liable party fails to perform to expectations.

:registrationFee:
  :ref:`Guarantee`, read-only

  Originates from `auction.registrationFee <http://lotsloki.api-docs.registry.ea2.openprocurement.io/en/latest/standard/auction.html>`_.

  The sum of money required to enroll on an official register.

:bankAccount:
  :ref:`Bank_Account`, read-only

  Originates from `auction.bankAccount <http://lotsloki.api-docs.registry.ea2.openprocurement.io/en/latest/standard/auction.html#bank-account>`_.

  Details which uniquely identify a bank account, and are used when making or receiving a payment.

:items:
  Array of :ref:`item` objects, read-only

  Originates from `lot.items <http://lotsloki.api-docs.registry.ea2.openprocurement.io/en/latest/standard/item.html>`_.

  List that contains single item being sold. 

  |ocdsDescription|
  The goods and services to be purchased, broken into line items wherever possible. Items should not be duplicated, but a quantity of 2 specified instead.

:documents:
  Array of :ref:`document` objects
 
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
  :ref:`period`, required

  Period when Auction is conducted. `startDate` should be provided.

:awardPeriod:
  :ref:`period`, read-only

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

.. _contractTerms:

Contract Terms
==============

Schema
------

:type:
  string, read-only

  Originates from `lot.items <http://lotsloki.api-docs.registry.ea2.openprocurement.io/en/latest/standard/Lot.html#contracts>`_.

  Type of the contract. The only value is `yoke`.
