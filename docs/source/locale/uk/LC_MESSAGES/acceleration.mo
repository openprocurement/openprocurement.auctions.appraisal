��          �       �       �   ,   �        {   8  r   �  -   '  6   U  D   �    �  �   �  �   k  �     �   �    �  H   �  7   �  �   	    �	  T     [   X  I   �  �  �  �   �    �  <  �  l     **This mode will work only in the sandbox**. Acceleration mode for sandbox Acceleration mode was developed to enable the procedure testing in the sandbox and to reduce time frames of this procedure. If you want to experiment with auctions, you can use acceleration mode and start your auction name with "TESTING". To enable acceleration mode you will need to: add additional parameter `mode` with a value ``test``; for the `submissionMethodDetails` you need to select 1 of 4 options: set ``fast-forward,dutch=-:-,sealedbid=-:---,bestbid=-:---`` as text value. ``dutch= - : -`` - at which step and who won in `dutch` part. ``sealedbid= - : ---`` - who scored on `sealedbid` and with what rate. ``bestbid= - : ---`` - who scored on `bestbid` and with what rate. set ``fast-forward,option1`` as text value. The auction will have a bet in `dutch` part. Minimum required number of participants - 1. set ``fast-forward,option2`` as text value. The auction will have a bet in `dutch` part, a bet on `sealedbid`. Minimum required number of participants - 2. set ``fast-forward,option3`` as text value. The auction will have a bet in `dutch` part, a bet on `sealedbid`, and a bet on `bestbid`. Minimum required number of participants - 2. set ``quick, accelerator=1440`` as text value for `procurementMethodDetails`. This parameter will accelerate auction periods. The number 1440 shows that restrictions and time frames will be reduced in 1440 times. Project-Id-Version: openprocurement.auctions.dgf 0.1
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2016-09-12 15:36+0300
PO-Revision-Date: 2018-12-10 18:40+0200
Last-Translator: Zoriana Zaiats <sorenabell@quintagroup.com>
Language-Team: Ukrainian <support@quintagroup.com>
Language: uk
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
Plural-Forms: nplurals=3; plural=(n%10==1 && n%100!=11 ? 0 : n%10>=2 && n%10<=4 && (n%100<10 || n%100>=20) ? 1 : 2);
X-Generator: Poedit 2.2
 **Даний механізм діє лише на пісочниці**. Режим прискорення в пісочниці Для зменшення термінів і забезпечення можливості тестування процедури на пісочниці доступний режим прискорення. Якщо хочете почати експериментувати з аукціонами, використовуйте режим прискорення. Також рекомендуємо починати заголовок таких аукціонів з "ТЕСТУВАННЯ". Щоб увімкнути режим прискорення вам потрібно: додати додатковий параметр `mode` зі значенням ``test``; оберіть одну опцію з 4 для `submissionMethodDetails`: задайте текстове значення ``fast-forward,dutch=-:-,sealedbid=-:---,bestbid=-:---``. ``dutch= - : -``- хто і на якому кроці переміг в `dutch` частині аукціону. ``sealedbid= - : ---`` - хто і з якою ставкою переміг в `sealedbid` частині аукціону. ``bestbid= - : ---`` - хто і з якою ставкою переміг в `bestbid` частині аукціону. задайте текстове значення ``fast-forward,option1``. Аукціон матиме ставку в `dutch` частині. Як мінімум один учасник має брати участь в аукціоні. задайте текстове значення ``fast-forward,option2``. Аукціон матиме ставку в `dutch` частині і в `sealedbid` частині. Як мінімум два учасники мають брати участь в аукціоні. задайте текстове значення ``fast-forward,option3``. Аукціон матиме ставку в `dutch` частині, в `sealedbid` частині, а також в `bestbid` частині. Як мінімум два учасники мають брати участь в аукціоні. встановити текстове значення ``quick, accelerator=1440`` параметру `procurementMethodDetails`. Цей параметр пришвидшить проходження періодів аукціону. Число 1440 показує, що часові обмеження та терміни скорочуються в 1440 раз. 