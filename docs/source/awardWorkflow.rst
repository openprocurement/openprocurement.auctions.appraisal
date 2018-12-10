.. _awardWorkflow: 

##############
Award Workflow
##############

Procedure Workflow for 1 Submitted Bid
======================================

Award Section
-------------

.. graphviz::

    digraph G {
        subgraph cluster_1 {
            node [style=filled, fillcolor=seashell2];
            edge[style=dashed,  arrowhead="vee", label="*"];
            "pending.admission" -> "pending";
            edge[style=dashed,  arrowhead="vee", label="**"];
            "pending" -> "active";
            node [style=filled, fillcolor=white];
            edge[style=solid,  arrowhead="vee", label="~", constraint=false];
            "pending.admission" -> "unsuccessful";
            edge[style=dashed,  arrowhead="vee", label="~~", constraint=false];
            "pending.admission" -> "unsuccessful";
            edge[style=dashed,  arrowhead="vee",  label="***", constraint=false];
            "pending" -> "unsuccessful";
            edge[style=solid,  arrowhead="vee", label="~~~", constraint=false];
            "active" -> "unsuccessful"; 
            label = "Awarding Process";
            color=white
            {rank=same; "pending" "unsuccessful"}
        }
    }
Legend
""""""

 \* admission protocol is downloaded and award is switched to `pending` by the organizer.
 
 \*\* protocol is downloaded and award is switched to `active` by the organizer.

 \*\*\* organizer has decided to disqualify the bidder.

 \~ admission protocol is not downloaded and award is not switched to `pending` by the organizer in time.

 \~\~ organizer has decided to disqualify the bidder. The approptiate document is downloaded and award is manually switched to `unsuccessful`.

 \~\~\~ organizer switched contract to `cancelled`.

Roles
"""""

:Chronograph: solid

:Organizer:  dashed


Contract Section
----------------

.. graphviz::

    digraph G {
        subgraph cluster_1 {
            node [style=filled, fillcolor=seashell2];
            edge[style=dashed,  arrowhead="vee", label="*"];
            "pending" -> "acive";
            label = "Contract Workflow";
            color=white
        }
        edge[style=dashed,  arrowhead="vee",  label="**"];
        "pending" -> "cancelled";
    }

Legend
""""""

 \* document was downloaded to contract. The contract itself was successfully activated by the organizer.

 \*\* there was no document uploaded. The organizer refused to activate the contract.

Roles
"""""

:Chronograph: solid

:Organizer:  dashed

Procedure Description
---------------------

1. The procedure receives `active.qualification` status. 

2. The award initially receives `pending.admission` status. The process enters the `admissionPeriod` with the auto-generated duration of 0-5 business days. During this term the organizer uploads the protocol (`documentType: admissionProtocol`) first and manually switches award to `pending` status then. Simultaneously the awarding process enters the the `verificationPeriod` phase. If the actions needed are not completed, the award auctomatically receives `unsuccessful` status, so that the procedure will be switched to `unsuccessful` as well.

    2.1 If the organizer decides to disqualify the bidder, a document (`documentType: rejectionProtocol` or `act`) has to be downloaded first and the award has to be manually switched to `unsuccessful` then. The procedure will be given `unsuccessful` status this way.

3. When the conditions are met, the process enters the `verificationPeriod` with the auto-generated duration of 0-10 business days. During this term the organizer uploads the protocol (`documentType: auctionProtocol`) first and manually switches award to `active` status then. Simultaneously the awarding process enters the signingPeriod phase and the procedure receives `active.awarded` status.

    3.1 If the organizer decides to disqualify the bidder, a document (`documentType: rejectionProtocol` or `act`) has to be downloaded first and the award has to be manually switched to `unsuccessful` then.

4. It is then when the qualification procedure enters the `signingPeriod` stage, which lasts up to 40 days from the beginning of the bidder qualification process. The contract of the qualifying bid initially receives a `pending` status. Within this time, the organizer should upload the document (`documentType: contractSigned`) in the system and manually switch contract to `active` status in order to successfully finish the qualification procedure. 

    4.1 For the bidder to be disqualified a document (`documentType: rejectionProtocol` or `act`) has to be downloaded first and the contract has to be manually switched to `cancelled` by the organizer then. As long as such an action is done, award status will receive `unsuccessful`.

Procedure Workflow for 2 Submitted Bids or More
================================================

Award Section
-------------

.. graphviz::

    digraph G {
        subgraph cluster_1 {
            node [style=filled, fillcolor=lightblue];
            edge[style=dotted,  arrowhead="vee"];
            "pending.waiting" -> cancelled[label="2nd award only" fontcolor=blue];
            label = "Awarding Process";
            color=white
        }   
        subgraph cluster_2 {
            node [style=filled, fillcolor=seashell2];
            edge[label="**", style=dashed,  arrowhead="vee"];
            "pending" -> "active";
            edge[label="*", style=solid,  arrowhead="vee"];
            "pending.waiting" -> "pending";
            node [style=filled, fillcolor=white];
            edge[label="***", style=dashed,  arrowhead="vee"];
            "pending" -> unsuccessful;
            edge[label="~", style=solid,  arrowhead="vee"];
            "active" -> unsuccessful;
            color=white
            {rank=same; "pending" "unsuccessful" "cancelled"}
        }   
    }

Legend
""""""

 Blue nodes represent statuses for the 2nd award ONLY

 \* award for winner is always formed in `pending`.
 
 \*\* protocol is downloaded and award is switched to `active` by the organizer.

 \*\*\* organizer has decided to disqualify the bidder.

 \~\~\~ organizer switched contract to `cancelled`.

Roles
"""""

:Chronograph: solid

:Organizer:  dashed

:Participant: dotted

Contract Section
----------------

.. graphviz::

    digraph G {
        subgraph cluster_1 {
            node [style=filled, color=lightgrey];
            edge[label="**" style=dashed];
            "pending" -> "cancelled";
            edge[label="*" style=dashed];
            "pending" -> "active"
            label = "Contract Workflow";
            color=white
        }
    }

Legend
""""""

 \* document was downloaded to contract. The contract itself was successfully activated by the organizer.

 \*\* there was no document uploaded. The organizer refused to activate the contract.

Roles
"""""

:Chronograph: solid

:Organizer:  dashed

Procedure Description
---------------------

1. The procedure receives `active.qualification` status. 

2. The award with the highest qualifying bid initially receives `pending` status. The process enters the `verificationPeriod` with the auto-generated duration of 0-10 business days. During this term the organizer uploads the protocol (`documentType: auctionProtocol`) first and manually switches award to `active` status then. Simultaneously the procedure enters the signingPeriod phase and the procedure receives `active.awarded` status.

    2.1 If the organizer decides to disqualify the bidder, a document (`documentType: rejectionProtocol` or `act`) has to be downloaded first and the award has to be manually switched to `unsuccessful` then.

3. It is then when the qualification procedure enters the `signingPeriod` stage, which lasts up to 40 days from the beginning of the bidder qualification process. The contract of the qualifying bid initially receives a `pending` status. Within this time, the organizer should upload the document (`documentType: contractSigned`) in the system and manually switch contract to `active` status in
order to successfully finish the qualification procedure. 

    3.1 For the bidder to be disqualified a document (`documentType: rejectionProtocol` or `act`) has to be downloaded first and the contract has to be manually switched to `cancelled` by the organizer then. As long as such an action is done, award status will receive `unsuccessful`.

4. The second highest qualifying bidder, immediately after the auction ending receives the `pending.waiting` status, in which by default they agree to wait for the end of the qualification of the highest qualifying bidder to be eligible to go through the qualification process if the highest bidder is disqualified. The only action that they can make is to manually cancel the award decision (switch award to `cancelled` status) - withdraw the security deposit and lose the chance to become a winner of the auction. If that is done and the first highest qualifying bidder becomes `unsuccessful`, the procedure receives the `unsuccessful` status. Provided that first award gets disqualified while the second has not disqualified themselves, the second award automatically changes its status from `pending.waiting` to `pending`, after which they undergo the same qualification procedure as outlined above for the first award.

Notes
=====

1. The auto-generated period duration does not influence the actions which can be done.

2. For the bidder to be qualified and not invalidated, the bid should be in the amount of more or equal to the starting price of the auction + the minimal step of the auction.

    2.1. In case the first two highest bids do not exceed the amount of starting price + the minimal step, the awards are not being formed at all, and the procedure automatically becomes `unsuccessful`.

    2.2 In case the second highest bid is smaller than the starting price + the minimal step, two awards are formed with the smaller one becoming unsuccessful immediately. The first highest bid (if larger than the value.amount + minimmalStep.amount) undergoes the awarding procedure and can win the auction.

3. The organizer can disqualify the award at any stage of the awarding process up to the moment, when a document with the `documentType: contractSigned` has been downloaded. 

4. The second highest qualifying bidder can disqualify themselves at any point in time BEFORE the start of their qualification process.

Statuses
========

:pending:
   :`Award`: Awaiting for the protocol to be uploaded and confirmed by the organizer. The valid bidder is able to submit the protocol as well, although it is not sufficient to move to the next status.

   :`Contract`: Awaiting for the contract to be signed (uploaded and activated in the system by the organizer).

:active:
    :`Award`: Auction protocol (`documentType: auctionProtocol`) was downloaded so that the award could be switched to `active` by the organizer.

    :`Contract`: The document (`documentType: contractSigned`) was downloaded  so that the status of the contract object could be switched to `active` by the organizer.

:unsuccessful:
    Terminal status of award. Rejection protocol or act (`documentType: rejectionProtocol/act`) was downloaded so that the award could be switched to `unsuccessful` by the organizer. Or when the contract becomes status `cancelled`, the status of the award will be `unsuccessful`.

:cancelled:
    Terminal status of contract. Rejection protocol or act (`documentType: rejectionProtocol/act`) was downloaded so that the contract could be switched to `cancelled` by the organizer.
