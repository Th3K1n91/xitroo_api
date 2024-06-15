# Unofficial Xitroo API

This is an unofficial API for interacting with the Xitroo email service. The API provides a set of Python classes and methods to manage email addresses, retrieve and send emails, handle inboxes, solve captchas, and more.

## Table of Contents
- [Installation](#Installation)
- [Quick Start](#Quick-Start)
- [Classes Overview](#classes-overview)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)

## Installation

To install this package, clone the repository and install the required dependencies:

```bash
pip install unofficial-xitroo-api
```

## Quick Start

Here's a brief example to get you started:
```python
from xitroo import Xitroo

# Generate mail
email = Xitroo.generate()
print(email)

# Initialize the Xitroo object
xitroo = Xitroo("your-email@xitroo.com")

# Get the inbox
inbox = xitroo.Inbox()

# Get the latest email
latest_mail = xitroo.getLatestMail()
print(latest_mail.getBodyText())

# Print code form latest email
print(Xitroo.getCode(latest_mail))
```
## Classes Overview
### Xitroo
The main class to interact with the Xitroo API. It includes methods for managing email addresses, headers, sessions, and performing various email operations.

### Mail
Represents an email. It provides methods to retrieve email content, attachments, and metadata.

### Inbox
Represents an inbox. It provides methods to retrieve emails and inbox information.

### SearchMail
Provides methods to search the inbox by different criteria such as date, sender, title, and text in the body.

### Captcha
Handles captcha-related operations including retrieving and verifying captchas.

## Documentation
For detailed documentation, please refer to the [HTML documentation](http://htmlpreview.github.io/?https://github.com/Th3K1n91/xitroo_api/tree/main/docs/index.html) in the docs folder.

## Contributing
We welcome contributions! Please fork the repository and submit pull requests.

## License
This project is licensed under the [MIT License](LICENSE). See the LICENSE file for details.
