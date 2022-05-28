# USAGE
```
pip install unofficial-xitroo-api
```
## How does that work?
It will get the latest inbox email and returns their body or subject as string to get for example account verification codes

# Documentation

## Arguments
```
.get_bodyText()
.get_bodyHtmlStrict()
.get_bodyHtml()
.get_subject()
>>> returns string from last mail

.get_latest_inbox_raw()
>>> returns json from latest mail
```
## Parameters
You can also pass in an integer how many times it should check the inbox

refresh_counter=int

refresh_wait=int
>"refresh_counter" is how many times it should ckeck the inbox (default is 5)

>"refresh_wait" is how many seconds it should wait between refreshes (default is 5)

Example:
```
xitroo("test@xitroo.de", refresh_counter=5, refresh_wait=5)
```
## Examples
```
from xitroo.api import xitroo

xitroo_email = xitroo("test@xitroo.de")
print(xitroo_email.get_bodyText())
```
```
from xitroo.api import xitroo as x

print(x("test@xitroo.de", refresh_counter=5, refresh_wait=5).get_subject())
```
