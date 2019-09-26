# Dancefloor Server

This is a simple HTTP service that exposes a public API and control web page to the running dance floor. It also exposes a GUI control interface.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [GUI Frontend](#gui-frontend)
- [API](#api)
  - [`GET /api/status`](#get-apistatus)
  - [`POST /api/playlist/advance`](#post-apiplaylistadvance)
  - [`POST /api/playlist/previous`](#post-apiplaylistprevious)
  - [`POST /api/playlist/add`](#post-apiplaylistadd)
  - [`POST /api/playlist/stay`](#post-apiplayliststay)
  - [`DELETE /api/playlist/:position`](#delete-apiplaylistposition)
  - [`GET /api/playlists`](#get-apiplaylists)
  - [`GET /api/playlists/:name`](#get-apiplaylistsname)
  - [`POST /api/playlists/:name`](#post-apiplaylistsname)
  - [`POST /api/playlists/:name/activate`](#post-apiplaylistsnameactivate)
  - [`GET /api/tempo`](#get-apitempo)
  - [`POST /api/tempo`](#post-apitempo)
  - [`POST /api/tempo/nudge`](#post-apitemponudge)
  - [`GET /api/brightness`](#get-apibrightness)
  - [`POST /api/brightness`](#post-apibrightness)
  - [`GET /api/layers/:name`](#get-apilayersname)
  - [`PATCH /api/layers/:name`](#patch-apilayersname)
- [TODO](#todo)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## GUI Frontend

The frontend is developed in a separate project. See source here: https://github.com/tennessee-garage/ddfui

For "production", we periodically check in a snapshot of this frontend to the `./static` folder here, so the RPi can serve it directly. These are the rough steps to follow:

```
### Build "production" frontend js, css, and assets.

$ cd ~/git/ddfui
$ npm install
$ yarn build

### Copy the built assets into this project.

$ cd ~/git/dance-floor/floor
$ ./bin/sync-frontend.sh ~/git/ddfui/build/
```

## API

### `GET /api/status`

Returns the current status.

**Request Arguments**

None.

**Response**

A structure consisting of:

* `playlist` (object): The current playlist; see `GET /api/playlist`.
* `tempo` (object): The current tempo; see `GET /api/tempo`.
* `processors` (array): A list of available processor, each an object consisting of:
  * `name` (string): The name of the processor.
* `brightness` (number): The global brightness, a number on `0.0 - 1.0`.

```json
{
  "playlist": {
    "current_position": 1,
    "millis_remaining": 2106,
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
    ]
  },
  "processors": {
    "animator": {
      "name": "animator"
    },
    "message": {
      "name": "message"
    },
    "pulsar": {
      "name": "pulsar"
    }
  },
  "layers": {
    "overlay1": {
      "enabled": true,
      "processor_name": "CoolStep"
    },
    "overlay2": {
      "enabled": false,
      "processor_name": null
    }
  },
  "tempo": {
    "bpm": 120.0,
    "downbeat_millis": 1500861666019
  }
}```

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


### `POST /api/playlist/previous`

Moves the playlist to the previous item, returning the playlist object.

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


### `POST /api/playlist/stay`

Cancel any auto-advance timeout on the current playlist item ("stay" on this processor).

**Request arguments**

None.

**Response**

The playlist object.


### `DELETE /api/playlist/:position`

Remove the playlist item at position `position`.

**Request arguments**

None.

**Response**

The playlist object upon success; HTTP `400` on error.


### `GET /api/playlists`

Lists _all_ playlists known to the system.

**Request arguments**

None.

**Response**

A dictionary of playlist items, keyed by a slug-like playlist name. Each value has the same format as `GET /api/playlist`.


### `GET /api/playlists/:name`

Fetches a single playlist, by slug-like playlist name.

**Request arguments**

None.

**Response**

The playlist object upon success; HTTP `404` if not found.


### `POST /api/playlists/:name`

Creates or updates a single playlist, by slug-like playlist name.

**Request arguments**

The request body should be a well-formed playlist object.

**Response**

The playlist object upon success; HTTP `400` upon failure.


### `POST /api/playlists/:name/activate`

Set this playlist as the current playlist.

**Request arguments**

None.

**Response**

The playlist object upon success; HTTP `404` if not found.


### `GET /api/tempo`

Get the current tempo settings.

**Request arguments**

None.

**Response**

The BPM information, consisting of:

* `bpm` (number): Beats per minute.
* `downbeat_millis` (number): Timestamp in milliseconds of the downbeat.


### `POST /api/tempo`

Set the current tempo.

**Request arguments**

* `bpm` (number): Beats per minute, as a number

**Response**

The BPM information.


### `POST /api/tempo/nudge`

Shift the BPM, downbeat, or both by a relative amount

**Request arguments**

* `bpm_delta` (number; optional): Value to add to or subtract from the current bpm.
* `downbeat_millis_delta` (number; optional): Value to add to or subtract from the current downbeat.

**Response**

The BPM information.


### `GET /api/brightness`

Get the global brightness of the floor, on a scale of 0.0 to 1.0.

**Response**

The current brightness.

```json
{
  "brightness": 0.7
}
```


### `POST /api/brightness`

Change the global brightness of the floor, on a scale of 0.0 to 1.0.

**Request arguments**

* `brightness` (number): The desired brightness, on a scale of `0.0` to `1.0`.

**Response**

Same as `GET /api/brightness`


### `GET /api/layers/:name`

Get details about a rendering layer.

**Response**

The layer's details.

```json
{
  "enabled": true,
  "processor_name": "CoolStep"
}
```


### `PATCH /api/layers/:name`

Adjust a rendering layer. Currently supports changing the processor, by patching the `processor_name` field.

**Request arguments**

* `processor_name` (string): The new processor name, or empty string to select no processor.
* `enabled` (boolean): Whether or not to enable the layer.

**Response**

Same as `GET /api/layers/:name`.


## TODO

Some improvements which should be made:

* Use a wsgi server in "production".
* Common error handling.
* Threadsafety around `Playlist` actions.
* Implement "add" and "delete" playlist operations.
