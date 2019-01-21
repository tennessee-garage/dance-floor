import time
import os
import logging


class profile(object):
    """Utility decorator that implements a simple profiler.
    """

    PROFILE_ENABLED = 'PROFILE' in os.environ and os.environ['PROFILE']
    PROFILE_DATA = []

    def __init__(self, print_seconds=None):
        """Decorator constructor.

        Args
            print_seconds: If given, will print the timing results at the end of the
            function call every print_seconds seconds and reset.  There should only be one of these.
        """
        self.print_seconds = print_seconds
        if print_seconds:
            print("Profiling enabled: output every {} seconds".format(print_seconds))

    def __call__(self, fn, *args, **kwargs):
        # Return the original function if profiling is not enabled
        if not self.PROFILE_ENABLED:
            return fn

        function_name = fn.__name__

        data = {
            'name': function_name,
            'calls': 0,
            'cumulative': 0,
            'print_seconds': self.print_seconds,
            'last_print': time.time()
        }

        # Save our instance's profile data off in the global store
        self.PROFILE_DATA.append(data)

        def new_fn(*args, **kwargs):
            data['calls'] += 1
            start_time = time.time()

            ret_val = fn(*args, **kwargs)

            total = time.time() - start_time
            data['cumulative'] += total

            if data['print_seconds']:
                if (time.time() - data['last_print']) > data['print_seconds']:
                    print("---------------------------")
                    print(" {: >5s} | {: >8s} | {: >8s} | {: >5s} | {}"
                          .format('calls', 'percall', 'cumul', 'pct', 'func'))
                    print_profile_line(data)
                    for other_data in profile.PROFILE_DATA:
                        # Don't print our data out again
                        if other_data['name'] == data['name']:
                            continue

                        print_profile_line(other_data, data['print_seconds'])
                        other_data['calls'] = 0
                        other_data['cumulative'] = 0

                    data['calls'] = 0
                    data['cumulative'] = 0
                    data['last_print'] = time.time()

            return ret_val

        return new_fn


def print_profile_line(data, total=None):
    name = data['name']
    calls = data['calls']
    cumulative = data['cumulative']
    per_call = float(data['cumulative']) / data['calls']

    if total:
        pct = '{: >5.2f}'.format(100 * (cumulative / float(total)))
    else:
        pct = '{: >5s}'.format('--')

    print(" {: >5d} | {: >8.3f} | {: >8.3f} | {} | {}".format(calls, per_call*1000, cumulative*1000, pct, name))
