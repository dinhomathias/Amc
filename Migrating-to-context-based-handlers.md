Don't do this:
```python
import warnings
from telegram.utils.deprecate import TelegramDeprecationWarning
warnings.filterwarnings('ignore', category=TelegramDeprecationWarning)
```
I mean.. you can, but your shit will break in the future.

Please do this instead: