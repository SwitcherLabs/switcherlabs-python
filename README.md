# SwitcherLabs Python SDK

SwitcherLabs is a feature flagging management platform that allows you to get started using feature flags in no time. The SwitcherLabs Python SDK allows you to easily integrate feature flags in your Python projects.

## Installation

Install the package with:

```sh
pip install --upgrade switcherlabs
```

### Requirements

- Python 3.4+ (PyPy supported)

## Usage

The package needs to be configured with your environments API Key, which is available in your SwitcherLabs dashboard under the environment details of the project you wish to use.

```python
import switcherlabs

client = switcherlabs.Client(api_key="<YOUR_API_KEY_HERE>")

flagEnabled = client.evaluate_flag(key="user_123", identifier="new_feature_flag")

if flagEnabled:
    # Do something if flag is enabled
else:
    # Else do something else.
```
