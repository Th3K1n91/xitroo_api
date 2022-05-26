# USAGE
```
pip install xitrooapi
```

## Examples
```
from xitrooapi import xitroo

email = xitroo("test@xitroo.de")
email.get_bodyText
```
or
```
email.get_bodyHtml
```
or
```
email.get_bodyHtmlStrict
```
You can also pass in an integer how many times it should check the inbox
```
xitroo("test@xitroo.de", refresh_counter=5, refresh_wait=5)
```
>refresh_counter is how many times it should ckeck the inbox (default is 5)

>refresh_wait is how many seconds it should wait between refreshes (default is 5)
