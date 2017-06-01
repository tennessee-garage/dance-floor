# Processor Code

## Creating a new processor

The skeleton for a processor is:

```python
from base import Base


class Your_Pattern(Base):

    def __init__(self):
        super(Your_Pattern, self).__init__()
        # Set/initialize any state variables here

    def get_next_frame(self, weights):
        # This gets called once every 1/fps seconds
    
        # Do something with list of weight values

        # Compute a list of RGB tuples, limit by self.max_value
        # which gets set for you based on driver at object creation

        return pixels
```

The processor class name and file name should be camel case, in lower and upper case respetively.  This simply makes it easy to declare:
```bash
  --processor some_class
```
and have it find some_class.py, and then load the Some_Class class in python space.
