# Processor Code

## Creating a new processor

The skeleton for a processor is:

```python
from base import Base


class Your_Pattern(Base):

    def __init__(self):
        super(Your_Pattern, self).__init__()
        self.some_state_variable

    def get_next_frame(self, weights):
        # Do something with list of weight values

        # Compute a list of RGB tuples

        return pixels
```

