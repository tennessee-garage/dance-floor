# Dancefloor Server

This is a simple HTTP service that exposes a public API and control web page to the running dance floor.

## API

### `GET /api/playlist`

Returns the current playlist.

**Request Arguments**

None.

**Response**

A playlist structure, consisting of:

* `current_position` (number): Current playlist position.
* `millis_remaining` (number): Number of milliseconds remaining on current item, `0` for indefinite.
* `queue` (object): The complete playlist, each item consisting of:
  * `name` (string): The processor name.
  * `duration` (number): The play duration, `0` for indefinite.
  * `args` (object; optional): Arguments to the processor.

```json
{
    "current_position": 1,
    "current": {
        "name": "message",
        "args": {
            "text": "Bleep bloop fazz!"
        },
        "duration": 5
    },
    "queue": [
        {
            "args": {
                "animation": "Color train"
            },
            "duration": 5,
            "name": "animator"
        },
        {
            "args": {
                "text": "Bleep bloop fazz!"
            },
            "duration": 5,
            "name": "message"
        },
        {
            "args": null,
            "duration": 5,
            "name": "raver_plaid"
        }
    ],
    "millis_remaining": 1492
}
```


### `POST /api/playlist/advance`

Advances the playlist to the next item, returning the playlist object.

**Request arguments**

None.

**Response**

The playlist object.


### `POST /api/playlist/add`

Adds a new item to the playlist, at the end of the playlist.

**Request arguments**

* `name` (string): The processor name.
* `duration` (number; optional): Play time in seconds; default of `0` for indefinite.
* `args` (string; optional): Processor-specific arguments.
* `next` (boolean; optional): If `true`, insert in next position rather than end. Implied when `immediate = true`.
* `immediate` (boolean; optional): If `true`, insert in next position _and_ advance immediately.

**Response**

The playlist object upon success; HTTP `400` on error.


### `DELETE /api/playlist/:position`

Remove the playlist item at position `position`.

**Request arguments**

None.

**Response**

The playlist object upon success; HTTP `400` on error.

## TODO

Some improvements which should be made:

* Bundle JS dependencies for internet-free operation.
* Use a wsgi server in "production".
* Common error handling.
* Threadsafety around `Playlist` actions.
* Implement "add" and "delete" playlist operations.
