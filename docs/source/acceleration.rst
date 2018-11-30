.. _acceleration:

Acceleration mode for sandbox
=============================

If you want to experiment with auctions, you can use acceleration mode and start your auction name with "TESTING".

Acceleration mode was developed to enable the procedure testing in the sandbox and to reduce time frames of this procedure. 

To enable acceleration mode you will need to:
    * add additional parameter `mode` with a value ``test``;
    * set ``quick, accelerator=1440`` as text value for `procurementMethodDetails`. This parameter will accelerate auction periods. The number 1440 shows that restrictions and time frames will be reduced in 1440 times.
    * for the `submissionMethodDetails` you need to select 1 of 4 options:
          * set ``fast-forward,dutch=-:-,sealedbid=-:---,bestbid=-:---`` as text value. ``dutch= - : -`` - at which step and who won in `dutch` part. ``sealedbid= - : ---`` - who scored on `sealedbid` and with what rate. ``bestbid= - : ---`` - who scored on `bestbid` and with what rate.
          * set ``fast-forward,option1`` as text value. The auction will have a bet in `dutch` part. Minimum required number of participants - 1.
          * set ``fast-forward,option2`` as text value. The auction will have a bet in `dutch` part, a bet on `sealedbid`. Minimum required number of participants - 2.
          * set ``fast-forward,option3`` as text value. The auction will have a bet in `dutch` part, a bet on `sealedbid`, and a bet on `bestbid`. Minimum required number of participants - 2.

**This mode will work only in the sandbox**.
