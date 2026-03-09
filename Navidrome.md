# Features | Navidrome
Explore Navidrome’s features and capabilities

*   1: [How to Use Smart Playlists in Navidrome (Beta)](#pg-d676e3ea312d31aa400bceddcaaca97c)
*   2: [Multi-Library Support](#pg-8bfdde434876e93c726d436fb957a728)
*   3: [Jukebox mode](#pg-abb8df56bac935deda508fc1b20c59f7)
*   4: [Sharing](#pg-44bca95ff8cd242faa92ad4fc176e766)
*   5: [Scrobbling](#pg-132fa14c2cdd54d9f9b4dd47ed2a8133)
*   6: [Plugins](#pg-212409e2a264d841db57c863fec75c44)

1 - How to Use Smart Playlists in Navidrome (Beta)
--------------------------------------------------

Learn how to create and manage Smart Playlists in Navidrome, a dynamic way to organize and enjoy your music collection.

Smart Playlists in Navidrome offer a dynamic way to organize and enjoy your music collection. They are created using JSON objects stored in files with a `.nsp` extension. These playlists are automatically updated based on specified criteria, providing a personalized and evolving music experience.

Creating Smart Playlists[](#creating-smart-playlists)
-----------------------------------------------------

To create a Smart Playlist, you need to define a JSON object with specific [fields](about:/docs/usage/features/smart-playlists/#fields) and [operators](about:/docs/usage/features/smart-playlists/#operators) that describe the criteria for selecting tracks. The JSON object is stored in a `.nsp` file Here are some examples to get you started:

### Example 1: Recently Played Tracks[](#example-1-recently-played-tracks)

This playlist includes tracks played in the last 30 days, sorted by the most recently played.

```
{
  "name": "Recently Played",
  "comment": "Recently played tracks",
  "all": [{ "inTheLast": { "lastPlayed": 30 } }],
  "sort": "lastPlayed",
  "order": "desc",
  "limit": 100
}

```


### Example 2: 80’s Top Songs[](#example-2-80s-top-songs)

This playlist features top-rated songs from the 1980s.

```
{
  "all": [
    { "any": [{ "is": { "loved": true } }, { "gt": { "rating": 3 } }] },
    { "inTheRange": { "year": [1981, 1990] } }
  ],
  "sort": "year",
  "order": "desc",
  "limit": 25
}

```


### Example 3: Favourites[](#example-3-favourites)

This playlist includes all loved tracks, sorted by the date they were loved.

```
{
  "all": [{ "is": { "loved": true } }],
  "sort": "dateLoved",
  "order": "desc",
  "limit": 500
}

```


### Example 4: All Songs in Random Order[](#example-4-all-songs-in-random-order)

This playlist includes all songs in a random order. Note: This is not recommended for large libraries.

```
{
  "all": [{ "gt": { "playCount": -1 } }],
  "sort": "random"
  // limit: 1000 // Uncomment this line to limit the number of songs
}

```


### Example 5: Multi-Field Sorting[](#example-5-multi-field-sorting)

This playlist demonstrates multiple sort fields - songs from the 2000s, sorted by year (descending), then by rating (descending), then by title (ascending).

```
{
  "name": "2000s Hits by Year and Rating",
  "all": [{ "inTheRange": { "year": [2000, 2009] } }],
  "sort": "-year,-rating,title",
  "limit": 200
}

```


### Example 6: Library-Specific Playlist[](#example-6-library-specific-playlist)

This playlist includes only high-rated songs from a specific library (useful in multi-library setups).

```
{
  "name": "High-Rated Songs from Library 2",
  "all": [{ "is": { "library_id": 2 } }, { "gt": { "rating": 4 } }],
  "sort": "-rating,title",
  "limit": 100
}

```


Creating Smart Playlists using the UI[](#creating-smart-playlists-using-the-ui)
-------------------------------------------------------------------------------

Currently Smart Playlists can only be created by manually editing `.nsp` files. We plan to add a UI for creating and editing Smart Playlists in future releases.

In the meantime, if you want a graphical way to create playlists, you can use [Feishin](https://github.com/jeffvli/feishin/), a desktop/web client for Navidrome, that supports creating Smart Playlists:

![](https://www.navidrome.org/docs/usage/features/smart-playlists/feishin_nsp_editor_hu_8213d122113f764b.webp)

Smart Playlists created/edited in Feishin will be available in Navidrome UI as soon as they are saved.

Importing Smart Playlists[](#importing-smart-playlists)
-------------------------------------------------------

Smart Playlists are imported the same way as regular (`.m3u`) playlists, during the library scan. Place your `.nsp` files in any folder in your library or the path specified by the `PlaylistsPath` configuration. Navidrome will automatically detect and import these playlists.

Managing Smart Playlists[](#managing-smart-playlists)
-----------------------------------------------------

### Visibility and Ownership[](#visibility-and-ownership)

*   Visibility: To make a Smart Playlist accessible to all users, set it to ‘public’. This is crucial if you want to use it in another `.nsp` file (with `inPlaylist` and `notInPlaylist`).
*   Ownership: By default, Smart Playlists are owned by the first admin user. You can change the ownership in the Playlists view to allow other users to manage them.

### User-Specific Playlists[](#user-specific-playlists)

Smart Playlists based on user interactions (e.g., play count, loved tracks) are automatically updated based on the owner’s interactions. If you want personalized playlists for each user, create separate `.nsp` files for each user and assign ownership accordingly.

### Refreshing Playlists[](#refreshing-playlists)

Smart Playlists are refreshed automatically when they are accessed by the UI or any Subsonic client. This ensures that the playlist is up-to-date when you view it. To avoid unnecessary load, there is a minimum delay between refreshes. This delay can be adjusted by setting the [`SmartPlaylistRefreshDelay`](about:/docs/usage/configuration/options/#:~:text=SmartPlaylistRefreshDelay) configuration option. By default, this is set to `5s`, meaning that Smart Playlists refreshes are spaced at least 5 seconds apart. You can adjust this value in the configuration file.

Troubleshooting Common Issues[](#troubleshooting-common-issues)
---------------------------------------------------------------

### Playlist Not Showing Up[](#playlist-not-showing-up)

If a Smart Playlist is not showing up in the Navidrome UI, check the following:

*   Check the logs for any errors during the library scan.
*   Ensure the `.nsp` file is in the correct folder and has the correct permissions.
*   Ensure the file is correctly formatted and does not contain any syntax errors. Tip: Use a JSON validator to check the file (ex: [https://jsonlint.com/](https://jsonlint.com/))
*   Check the playlist’s visibility and ownership settings.

### Referencing Other Playlists[](#referencing-other-playlists)

When referencing another playlist by ID (using the operator `inPlaylist`), ensure that the referenced playlist is not another Smart Playlist unless it is set to ‘public’. This ensures proper functionality.

### Special Characters in Conditions[](#special-characters-in-conditions)

If you encounter issues with conditions like `contains` or `endsWith`, especially with special characters like underscores (`_`), be aware that these might be ignored in some computations. Adjust your conditions accordingly.

### Sorting by multiple fields[](#sorting-by-multiple-fields)

You can now sort by multiple fields by separating them with commas. You can also control the sort direction for each field by prefixing it with `+` (ascending, default) or `-` (descending).

Examples:

*   `"sort": "year,title"` - Sort by year first (ascending), then by title (ascending)
*   `"sort": "year,-rating"` - Sort by year (ascending), then by rating (descending)
*   `"sort": "-lastplayed,title"` - Sort by last played date (descending), then by title (ascending)

The global `order` field can still be used and will reverse the direction of all sort fields.

### Deleting Users with Shared Smart Playlists[](#deleting-users-with-shared-smart-playlists)

If you encounter issues deleting users with shared Smart Playlists, check if the playlists are used by other users. See [this issue](https://github.com/navidrome/navidrome/issues/3180) for details.

### Editing Playlists[](#editing-playlists)

To change the rules of a Smart Playlist, you need to edit the `.nsp` file directly (or use [Feishin](https://github.com/jeffvli/feishin/)). Changes are automatically detected during the next library scan. The list of tracks in a Smart Playlist is read-only and cannot be edited directly.

Additional Resources[](#additional-resources)
---------------------------------------------

### Fields[](#fields)

Here’s a table of fields you can use in your Smart Playlists:


|Field               |Description                             |
|--------------------|----------------------------------------|
|title               |Track title                             |
|album               |Album name                              |
|hascoverart         |Track has cover art                     |
|tracknumber         |Track number                            |
|discnumber          |Disc number                             |
|year                |Year of release                         |
|date                |Recording date                          |
|originalyear        |Original year                           |
|originaldate        |Original date                           |
|releaseyear         |Release year                            |
|releasedate         |Release date                            |
|size                |File size                               |
|compilation         |Compilation album                       |
|dateadded           |Date added to library                   |
|datemodified        |Date modified                           |
|discsubtitle        |Disc subtitle                           |
|comment             |Comment                                 |
|lyrics              |Lyrics                                  |
|sorttitle           |Sorted track title                      |
|sortalbum           |Sorted album name                       |
|sortartist          |Sorted artist name                      |
|sortalbumartist     |Sorted album artist name                |
|albumtype           |Album type                              |
|albumcomment        |Album comment                           |
|catalognumber       |Catalog number                          |
|filepath            |File path, relative to the MusicFolder  |
|filetype            |File type                               |
|grouping            |Grouping                                |
|duration            |Track duration                          |
|bitrate             |Bitrate                                 |
|bitdepth            |Bit depth                               |
|bpm                 |Beats per minute                        |
|channels            |Audio channels                          |
|loved               |Track is loved                          |
|dateloved           |Date track was loved                    |
|lastplayed          |Date track was last played              |
|daterated           |Date track was lrated                   |
|playcount           |Number of times track was played        |
|rating              |Track rating                            |
|mbz_album_id        |MusicBrainz Album ID                    |
|mbz_album_artist_id |MusicBrainz Album Artist ID             |
|mbz_artist_id       |MusicBrainz Artist ID                   |
|mbz_recording_id    |MusicBrainz Recording ID                |
|mbz_release_track_id|MusicBrainz Release Track ID            |
|mbz_release_group_id|MusicBrainz Release Group ID            |
|library_id          |Library ID (for multi-library filtering)|


##### Notes[](#notes)

*   Dates must be in the format `"YYYY-MM-DD"`.
*   Booleans must not be enclosed in quotes. Example: `{ "is": { "loved": true } }`.
*   `filepath` is relative to your music library folder. Ensure your paths are correctly specified without the `/music` prefix (or whatever value you set in `MusicFolder`).
*   Numeric fields like `library_id`, `year`, `tracknumber`, `discnumber`, `size`, `duration`, `bitrate`, `bitdepth`, `bpm`, `channels`, `playcount`, and `rating` support numeric comparisons (`gt`, `lt`, `inTheRange`, etc.).
*   **Multi-Library**: Smart Playlists can include songs from multiple libraries if the user has access to them. Use the `library_id` field to filter songs from specific libraries.

##### Special Fields[](#special-fields)

*   `random`: Used for random sorting (e.g., `"sort": "random"`)
*   `value`: Used internally for tag and role-based queries

##### MusicBrainz Fields[](#musicbrainz-fields)

The following fields contain MusicBrainz IDs that can be used to create playlists based on specific MusicBrainz entities:

*   `mbz_album_id`: Filter by specific MusicBrainz album
*   `mbz_album_artist_id`: Filter by specific MusicBrainz album artist
*   `mbz_artist_id`: Filter by specific MusicBrainz artist
*   `mbz_recording_id`: Filter by specific MusicBrainz recording
*   `mbz_release_track_id`: Filter by specific MusicBrainz release track
*   `mbz_release_group_id`: Filter by specific MusicBrainz release group

Any tags imported from the music files, that are not listed above, can be also used as fields in your Smart Playlists. Check the [complete list of tags](https://github.com/navidrome/navidrome/blob/master/resources/mappings.yaml) imported by navidrome. You can also add your own custom tags to your music files and use them in your Smart Playlists. Check the [Custom Tags](https://www.navidrome.org/docs/usage/configuration/custom-tags/) for more information.

### Operators[](#operators)

Here’s a table of operators you can use in your Smart Playlists:


|Operator     |Description             |Argument type                    |
|-------------|------------------------|---------------------------------|
|is           |Equal                   |String, Number, Boolean          |
|isNot        |Not equal               |String, Number, Boolean          |
|gt           |Greater than            |Number                           |
|lt           |Less than               |Number                           |
|contains     |Contains                |String                           |
|notContains  |Does not contain        |String                           |
|startsWith   |Starts with             |String                           |
|endsWith     |Ends with               |String                           |
|inTheRange   |In the range (inclusive)|Array of two numbers or dates    |
|before       |Before                  |Date ("YYYY-MM-DD")              |
|after        |After                   |Date ("YYYY-MM-DD")              |
|inTheLast    |In the last             |Number of days                   |
|notInTheLast |Not in the last         |Number of days                   |
|inPlaylist   |In playlist             |Another playlist’s ID (see below)|
|notInPlaylist|Not in playlist         |Another playlist’s ID (see below)|


The nature of the field determines the argument type. For example, `year` and `tracknumber` require a number, while `title` and `album` require a string.

To get a playlist’s ID to be used in `inPlaylist` and `notInPlaylist`, navigate to the playlist in the Navidrome UI and check the URL. The ID is the last part of the URL after the `/playlists/` path:

![](https://www.navidrome.org/docs/usage/features/smart-playlists/playlist_url_hu_897fa85abd44fe06.webp)

2 - Multi-Library Support
-------------------------

Learn how to set up and manage multiple music libraries in Navidrome with user-specific access controls.

Overview[](#overview)
---------------------

Navidrome supports multiple music libraries since v0.58.0, allowing you to organize your music into separate collections with user-specific access controls. This feature is perfect for:

*   Separating different types of content (music vs. audiobooks)
*   Organizing by quality (lossy vs. lossless)
*   Separating personal collections (family members, roommates)
*   Organizing by genre or era (classical, jazz, modern)
*   Managing different sources (official releases vs. bootlegs/live recordings)

How Multi-Library Works[](#how-multi-library-works)
---------------------------------------------------

### Default Library[](#default-library)

When Navidrome starts, it automatically creates a default library using your `MusicFolder` configuration. This becomes “Library 1” and all existing users automatically get access to it, ensuring backward compatibility.

### User Access Control[](#user-access-control)

*   **Admin users** automatically have access to all libraries
*   **Regular users** must be explicitly granted access to libraries by an administrator
*   Users can only see and access music from libraries they have permission to use
*   Each user can switch between their accessible libraries using the library selector in the UI

### Data Isolation[](#data-isolation)

*   **Albums** are scoped to a single library; each library maintains its own set of albums and their songs.
*   **Artists** can have albums and songs spread across multiple libraries. The same artist may appear in several libraries, each with different albums or tracks.
*   Artist statistics and metadata are aggregated across all libraries where the artist appears.
*   Playlists can contain songs from multiple libraries (if the user has access to those libraries)
*   Smart playlists can be scoped to specific libraries
*   Search results are filtered by the user’s accessible (and selected) libraries

Setting Up Multi-Library[](#setting-up-multi-library)
-----------------------------------------------------

### Creating Additional Libraries[](#creating-additional-libraries)

1.  **Access Library Management**
    
    *   Log in as an administrator
    *   Go to **Settings** → **Libraries**
2.  **Create a New Library**
    
    *   Click the **"+"** button to add a new library
    *   Provide a **Name** for the library (e.g., “Audiobooks”, “FLAC Collection”)
    *   Set the **Path** to the folder containing your music files
    *   Optionally set the library as default for new users
    *   Click **Save**
3.  **Initial Scan**
    
    *   The new library will automatically begin scanning
    *   Monitor the scanning progress in the Activity Panel
    *   Large libraries may take time to complete the initial scan

### Managing User Access[](#managing-user-access)

1.  **Assign Libraries to Users**
    
    *   Go to **Settings** → **Users**
    *   Click on a user to edit their settings
    *   In the **Libraries** section, check the libraries the user should access
    *   Click **Save**
2.  **Verify Access**
    
    *   Users will see a library selector in the sidebar if they have access to multiple libraries
    *   The library selector is displayed in the top left corner of the UI
    *   Users can select multiple libraries to browse and listen to their music

Configuration Considerations[](#configuration-considerations)
-------------------------------------------------------------

### File Organization[](#file-organization)

Each library should have its own root folder structure:

```
/music/main/           # Default library (MusicFolder)
├── Artist 1/
├── Artist 2/
└── ...

/music/audiobooks/     # Audiobooks library
├── Author 1/
├── Author 2/
└── ...

/other_path/lossless/       # High-quality library
├── Artist 1/
├── Artist 2/
└── ...

```


It is up to the user where to save music collections. You can store your artists in `/music` or any other path you want to use.

### Permissions[](#permissions)

*   The Navidrome user must have read access to all library folders
*   Consider using the same ownership/permissions across all library folders
*   Ensure adequate disk space for each library’s cache and metadata

### Performance[](#performance)

*   Each library maintains its own file system watcher
*   Multiple libraries scanning simultaneously may impact performance
*   Consider staggering initial scans of large libraries
*   Large numbers of libraries may affect UI performance

Using Multi-Library[](#using-multi-library)
-------------------------------------------

### Switching Libraries[](#switching-libraries)

*   Use the library selector in the sidebar to select visible libraries
*   All browsing, searching, and playback is scoped to the selected libraries

### Cross-Library Features[](#cross-library-features)

*   **Playlists**: Can contain songs from multiple libraries (user must have access)
*   **Smart Playlists**: Can be scoped to specific libraries using filters
*   **Search**: Results from all accessible libraries (filtered by permissions)
*   **Statistics**: Maintained separately per library

API and Client Support[](#api-and-client-support)
-------------------------------------------------

### Subsonic API[](#subsonic-api)

*   The `getMusicFolders` endpoint returns all libraries accessible to the authenticated user
*   All other endpoints respect the user’s library permissions
*   Clients that support multiple music folders will work with Navidrome’s multi-library feature

### Client Compatibility[](#client-compatibility)

Most Subsonic-compatible clients that support multiple music folders will work with Navidrome’s multi-library feature. Check your client’s documentation for music folder support.

Troubleshooting[](#troubleshooting)
-----------------------------------

### Library Not Scanning[](#library-not-scanning)

*   Verify the path exists and is readable by the Navidrome user
*   Check the logs for permission errors
*   Ensure the path doesn’t overlap with other libraries

### User Cannot Access Library[](#user-cannot-access-library)

*   Verify the user has been granted access to the library in user settings
*   Check that the library has completed its initial scan

### Performance Issues[](#performance-issues)

*   Monitor system resources during simultaneous library scans
*   Consider adjusting scanner settings if experiencing high I/O

Best Practices[](#best-practices)
---------------------------------

*   Design your folder structure before creating libraries
*   Use clear, descriptive names for libraries
*   Consider future growth when organizing

*   [Configuration Options](https://www.navidrome.org/docs/usage/configuration/options/): Basic setup and MusicFolder configuration
*   [Smart Playlists](https://www.navidrome.org/docs/usage/features/smart-playlists/): Create dynamic playlists with library-specific filters
*   [Backup](https://www.navidrome.org/docs/usage/admin/backup/): Protecting your multi-library setup

3 - Jukebox mode
----------------

Activate Navidrome’s Jukebox mode

Introduction[](#introduction)
-----------------------------

Navidrome’s Jukebox feature is a built-in functionality that allows users to play music directly to the server’s audio hardware. This essentially turns your server into a jukebox, enabling you to play songs or playlists remotely through a supported Subsonic client. With the Jukebox feature, you can control the audio playback in real-time, just like you would with any other media player. It’s a convenient way to enjoy your music collection without the need for additional hardware or software. Ideal for parties, background music, or personal enjoyment, this feature enhances the versatility of your Navidrome server setup.

Navidrome’s Jukebox mode is based on the OpenSource audio player [MPV](https://mpv.io/). MPV is a mature and tested audio/videoplayer that is supported on many platforms. Navidrome’s Jukebox mode uses MPV for audio playback in combination with MPV’s feature to be controlled through [IPC](https://mpv.io/manual/master/#json-ipc).

MPV Installation[](#mpv-installation)
-------------------------------------

MPV must be present on the system where the Navidrome server runs. You might find it already installed or could install it yourself using the methods given on the MPV’s [installation page](https://mpv.io/installation/).

The minimal requirement is the IPC support. MPV added IPC support with version 0.7.0 for Linux and macOS and added Windows support with version 0.17.0. Your OS will most probably include newer versions (0.3X) which we recommend. After the installation check the version with:

Jukebox mode will use the MPV audio device naming scheme for its configuration. To get an overview about the available audio devices on the system do:

```
$ mpv --audio-device=help

```


Here is an example on macOS:

```
List of detected audio devices:
  'auto' (Autoselect device)
  'coreaudio/AppleGFXHDAEngineOutputDP:10001:0:{D109-7950-00005445}' (BenQ EW3270U)
  'coreaudio/AppleUSBAudioEngine:Cambridge Audio :Cambridge Audio USB Audio 1.0:0000:1' (Cambridge Audio USB 1.0 Audio Out)
  'coreaudio/BuiltInSpeakerDevice' (MacBook Pro-Lautsprecher)

```


or on Linux:

```
List of detected audio devices:
  'auto' (Autoselect device)
  'alsa' (Default (alsa))
  'alsa/jack' (JACK Audio Connection Kit)
  'alsa/default:CARD=Headphones' (bcm2835 Headphones, bcm2835 Headphones/Default Audio Device)

  ...

  'jack' (Default (jack))
  'sdl' (Default (sdl))
  'sndio' (Default (sndio))

```


Please use the full device name **if you do not want to use MPV’s auto device**. For example on macOS:

```
"coreaudio/AppleUSBAudioEngine:Cambridge Audio :Cambridge Audio USB Audio 1.0:0000:1"

```


Configuration[](#configuration)
-------------------------------

Jukebox mode is enabled by setting this option in your [configuration file](https://www.navidrome.org/docs/usage/configuration/options/) (normally `navidrome.toml`):

In most cases, this should be the only config option needed.

The MPV binary should be found automatically on the path. In case this does not work use this configuration option:

Jukebox mode will use MPV’s **auto** device for playback if no device is given.

One can supply an array of multiple devices under `Jukebox.Devices` (note: this config option cannot be set as an environment variable):

```
Jukebox.Devices = [
    # "symbolic name " "device"
    [ "internal",     "coreaudio/BuiltInSpeakerDevice" ],
    [ "dac",          "coreaudio/AppleUSBAudioEngine:Cambridge Audio :Cambridge Audio USB Audio 1.0:0000:1" ]
]

```


and select one by using `Jukebox.Default`:

Here is one example configuration:

```
# Enable/Disable Jukebox mode
Jukebox.Enabled = true

# List of registered devices, syntax:
#  "symbolic name " - Symbolic name to be used in UI's
#  "device" - MPV audio device name, do mpv --audio-device=help to get a list

Jukebox.Devices = [
    # "symbolic name " "device"
    [ "internal",     "coreaudio/BuiltInSpeakerDevice" ],
    [ "dac",          "coreaudio/AppleUSBAudioEngine:Cambridge Audio :Cambridge Audio USB Audio 1.0:0000:1" ]
]

# Device to use for Jukebox mode, if there are multiple entries above.
# Using device "auto" if missing
Jukebox.Default = "dac"

```


### The `MPVCmdTemplate` / Snapcast integration[](#the-mpvcmdtemplate--snapcast-integration)

There might be cases, where you want to control the call of the `mpv` binary. Noteable mentions would be the integration with Snapcast for multi room audio. You can use the `MPVCmdTemplate` for this.

The default value is `mpv --audio-device=%d --no-audio-display --pause %f --input-ipc-server=%s`.


|Symbol|Meaning                  |
|------|-------------------------|
|%s    |Path to IPC server socket|
|%d    |Audio device (see above) |
|%f    |Path to file to play     |


To integrate with Snapcast alter the template:

```
MPVCmdTemplate = "mpv --no-audio-display --pause %f --input-ipc-server=%s --audio-channels=stereo --audio-samplerate=48000 --audio-format=s16 --ao=pcm --ao-pcm-file=/tmp/snapfifo"

```


This assumes Snapcast is running on the same machine as Navidrome. Check the [Snapcast documentation](https://github.com/badaix/snapcast/blob/develop/doc/player_setup.md#mpv) for details.

Usage[](#usage)
---------------

Once Jukebox mode is enabled and configured, to start playing music through your servers speakers you’ll need to download a third-party [Subsonic client](https://www.subsonic.org/pages/apps.jsp). This client acts as a remote control. Not all Subsonic clients support Jukebox mode and you’ll need to check that your client supports this feature.

Jukebox mode is currently not supported through the Navidrome Web UI.

Troubleshooting[](#troubleshooting)
-----------------------------------

If Jukebox mode is enabled one should see the message “**Starting playback server**” in the log. The number of detected audio devices and the device chosen will be given in the log as well:

```
INFO[0000] Starting playback server
INFO[0000] 4 audio devices found
INFO[0000] Using default audio device: dac

```


For further troubleshooting, set Navidrome’s loglevel to DEBUG:

4 - Sharing
-----------

How to create links to your media to be shared on Facebook, X, WhatsApp

Navidrome has a “Sharing” feature which allows users to generate a shareable link for a track, album, artist, or playlist. This link can then be sent to friends, allowing them to listen or download the music without having an account on your Navidrome instance.

### Enabling the Sharing Feature[](#enabling-the-sharing-feature)

The Sharing feature is disabled by default. To enable it, you need to adjust your Navidrome [configuration](https://www.navidrome.org/docs/usage/configuration/options/). In your configuration file, set `EnableSharing=true`, or set the environment variable `ND_ENABLESHARING=true`.

Once the Sharing feature is enabled, all users will have access to all existing shares. This includes the ability to change the description and expiration date of the shares, as well as the capability to create new shares.

Please note that at this time, there is no way to set specific sharing permissions per user. This means that once the Sharing feature is enabled, all users have equal access and capabilities related to sharing. This includes the ability to view, modify, and create shares.

Due to this, we advise you to enable this feature only if you are comfortable with these permissions. Future updates may include more granular permission controls for sharing.

### Default Expiration for Shares[](#default-expiration-for-shares)

By default, new shares (public links) expire after 1 year (“8760h”). You can set a different default expiration time for all new shares using the `DefaultShareExpiration` config option. This sets how long new shares will be valid, unless you manually change the expiration when creating the share.

Set it in your config file:

```
DefaultShareExpiration = "8760h"  # Shares expire after 1 year by default

```


Or as an environment variable:

```
ND_DEFAULTSHAREEXPIRATION=8760h

```


Use values like `"24h"` or `"1h30m"`. Valid suffixes are `"h"` (hours), `"m"` (minutes), and `"s"` (seconds).

### Using the Sharing Feature[](#using-the-sharing-feature)

Once the Sharing feature is enabled, all users will be able to access current shares, modify descriptions and expiration, and create new ones. However, as of the initial implementation, there is currently no way to set permissions per user. When browsing your music collection, you will notice a “Share” button or menu item available for each item, be it a track, album, artist, or playlist. To share an item, simply click on this “Share” button.

Upon clicking the “Share” button, a dialog box will appear, allowing you to configure your share. This includes setting a description other configurations for the share.

![](https://www.navidrome.org/screenshots/share-dialog.webp)

Once you have configured your share as desired, click the “Share” button. This will generate a unique shareable link, which you can then copy and share with your friends.

The generated sharable links will be in the following format: `http://yourserver.com/share/XXXXXXXXXX`. If you have Navidrome behind a reverse proxy, ensure you allow traffic to `/share`.

### Subsonic API Endpoints[](#subsonic-api-endpoints)

The Sharing feature also implements the related Subsonic API endpoints. See the [API docs for implemented endpoints](https://opensubsonic.netlify.app/categories/sharing/)

### Meta-tags to HTML[](#meta-tags-to-html)

Meta-tags are added to the HTML to provide some information about the shared music on chat platforms. Example of a link shared in Discord:

![](https://www.navidrome.org/screenshots/share-meta.webp)

5 - Scrobbling
--------------

Information on setting up scrobbling with Last.fm and ListenBrainz.

Navidrome allows you to easily scrobble your played songs to Last.fm and ListenBrainz.

Last.fm[](#lastfm)
------------------

1.  Ensure you have the API Key and API Secret set according to the instructions in [External Integrations](about:/docs/usage/integration/external-services/#lastfm).
2.  Go to your user profile’s Personal Settings.
3.  Toggle the option `Scrobble to Last.fm`, a new browser tab will open directing you to Last.fm.

![](https://www.navidrome.org/screenshots/navidrome-personal-settings.webp)

4.  If you are not logged in, then log in with your Last.fm credentials.

![](https://www.navidrome.org/screenshots/lastfm-login.webp)

5.  Click “Yes, allow access”.

![](https://www.navidrome.org/screenshots/lastfm-allow-access.webp)

ListenBrainz[](#listenbrainz)
-----------------------------

1.  Toggle the option `Scrobble to ListenBrainz`. If you already have a User key generated, skip to step 4.
2.  Click on the appropriate link in the pop-up that opens.

![](https://www.navidrome.org/screenshots/listenbrainz-popup.webp)

3.  On the ListenBrainz website, either generate a new token or copy your existing one, then go back to your Navidrome tab.

![](https://www.navidrome.org/screenshots/listenbrainz-token.webp)

4.  Paste the token in the pop-up and save.

Scrobble History[](#scrobble-history)
-------------------------------------

Starting with version 0.59.0, Navidrome tracks your scrobble/listen history natively. This means that for music added after this version, Navidrome maintains a complete record of when each track was played. This historical data will be used in future features such as statistics and analytics (“Navidrome Wrapped” style reports).

6 - Plugins
-----------

Extend Navidrome’s functionality with community-developed plugins

Navidrome supports a plugin system that allows you to extend its functionality with community-developed extensions. Plugins run in a secure WebAssembly sandbox, providing isolation from the main application while enabling powerful customizations.

What Plugins Can Do[](#what-plugins-can-do)
-------------------------------------------

Plugins can extend Navidrome in several ways:

*   **Metadata Agents**: Fetch artist biographies, album information, and images from external sources
*   **Scrobblers**: Send your listening history to external services beyond the built-in Last.fm and ListenBrainz support
*   **Scheduled Tasks**: Run periodic background tasks
*   **Event Handlers**: React to events like playback or library changes

Each plugin declares which capabilities it provides, and you can enable only the plugins you need.

Finding Plugins[](#finding-plugins)
-----------------------------------

Community-developed plugins can be found on GitHub using the [`navidrome-plugin`](https://github.com/topics/navidrome-plugin) topic.

When evaluating a plugin, consider:

*   **Repository activity**: Check when the plugin was last updated
*   **Documentation**: Look for clear installation and configuration instructions
*   **Issues and discussions**: Review any reported problems or user feedback
*   **Source code**: Plugins are open source, so you can review the code before installing

Installing Plugins[](#installing-plugins)
-----------------------------------------

1.  **Download the plugin**: Go to the plugin’s GitHub repository and download the `.ndp` file from the Releases page.
    
2.  **Place in plugins folder**: Copy the `.ndp` file to your plugins directory:
    
    *   Default location: `<DataFolder>/plugins`
    *   Custom location: Set `Plugins.Folder` in your configuration
3.  **Rescan for plugins**: Click the “Rescan” button in the Plugins section of the web UI, or if you have `Plugins.AutoReload = true` configured, the plugin will be detected automatically.
    
4.  **Enable the plugin**: Go to the Navidrome web UI, navigate to the Plugins section in the admin area, and enable the plugin.
    
5.  **Configure the plugin**: Some plugins require additional configuration. Check the plugin’s documentation for required settings.
    

Server Configuration[](#server-configuration)
---------------------------------------------

The following configuration options control the plugin system:



* In config file: Plugins.Enabled
  * As an env var: ND_PLUGINS_ENABLED
  * Description: Enable the plugin system
  * Default Value: true
* In config file: Plugins.Folder
  * As an env var: ND_PLUGINS_FOLDER
  * Description: Directory where plugin (.ndp) files are stored
  * Default Value: "<DataFolder>/plugins"
* In config file: Plugins.AutoReload
  * As an env var: ND_PLUGINS_AUTORELOAD
  * Description: Watch plugins folder for changes and reload automatically
  * Default Value: false
* In config file: Plugins.LogLevel
  * As an env var: ND_PLUGINS_LOGLEVEL
  * Description: Log level for plugins (error, warn, info, debug, trace)
  * Default Value: Inherit from LogLevel
* In config file: Plugins.CacheSize
  * As an env var: ND_PLUGINS_CACHESIZE
  * Description: Size of WebAssembly compilation cache
  * Default Value: "200MB"


### Example Configuration[](#example-configuration)

```
[Plugins]
Enabled = true
Folder = "/path/to/plugins"    # Optional: custom plugins folder
AutoReload = true              # Useful during development/testing
LogLevel = "debug"             # Enable detailed plugin logging
CacheSize = "200MB"            # WASM compilation cache size

```


Or using environment variables (useful for Docker):

```
ND_PLUGINS_ENABLED=true
ND_PLUGINS_FOLDER=/data/plugins
ND_PLUGINS_AUTORELOAD=true
ND_PLUGINS_LOGLEVEL=debug

```


Managing Plugins in the Web UI[](#managing-plugins-in-the-web-ui)
-----------------------------------------------------------------

Once plugins are installed, you manage them through the Navidrome web interface:

![](https://www.navidrome.org/docs/usage/features/plugins/plugins-manage_hu_8c880e1c997147c4.webp)

### Viewing Installed Plugins[](#viewing-installed-plugins)

Navigate to the Plugins section in the admin area to see all installed plugins. Each plugin shows its name, description, version, and current status.

![](https://www.navidrome.org/docs/usage/features/plugins/plugins-list_hu_48f67d9a47aa2206.webp)

### Enabling and Disabling Plugins[](#enabling-and-disabling-plugins)

Toggle individual plugins on or off. Disabled plugins remain installed but won’t run.

### Configuring Plugin Settings[](#configuring-plugin-settings)

Many plugins have configurable options. Click on a plugin to view and modify its settings. The available options depend on what the plugin supports - check the plugin’s documentation for details on each setting.

![](https://www.navidrome.org/docs/usage/features/plugins/plugins-details_hu_d2a68ba45b683f5.webp)

### User Access[](#user-access)

Some plugins are user-scoped, meaning they operate on a per-user basis (like scrobblers). For these plugins, you need to configure which users have access:

*   **All users**: Grant access to every user
*   **Specific users**: Select individual users who can use the plugin

![](https://www.navidrome.org/docs/usage/features/plugins/plugins-user-permission_hu_27263dabe3cec50b.webp)

### Library Access[](#library-access)

Plugins that interact with your music library may need library access configured:

*   **All libraries**: Grant access to all libraries
*   **Specific libraries**: Select which libraries the plugin can access

![](https://www.navidrome.org/docs/usage/features/plugins/plugins-library-permission_hu_98842b4fcf9cb016.webp)

Security[](#security)
---------------------

### WebAssembly Sandbox[](#webassembly-sandbox)

All plugins run inside a WebAssembly (WASM) sandbox provided by the [Extism](https://extism.org/) runtime. This means:

*   Plugins cannot directly access your filesystem (except explicitly granted library paths)
*   Network access is restricted to hosts declared in the plugin’s manifest
*   Plugins are isolated from each other and from Navidrome’s internal systems

### Permission System[](#permission-system)

Each plugin declares the permissions it needs in its manifest:

*   **HTTP access**: Which external hosts the plugin can contact
*   **Storage**: Whether the plugin can store persistent data
*   **Library access**: Whether the plugin needs to read your music files
*   **User access**: Whether the plugin operates on a per-user basis

Review these permissions before enabling a plugin to understand what it can access.

### Best Practices[](#best-practices)

*   Only install plugins from trusted sources
*   Review the plugin’s source code if you have concerns
*   Start with plugins disabled and enable them one at a time
*   Monitor your logs after enabling new plugins
*   Keep plugins updated to get security fixes

Troubleshooting[](#troubleshooting)
-----------------------------------

### Plugin Not Appearing[](#plugin-not-appearing)

*   Verify the `.ndp` file is in the correct plugins folder
*   Check that `Plugins.Enabled = true` in your configuration
*   Click the “Rescan” button in the Plugins section to detect new plugins
*   Check logs for any errors during plugin discovery

### Plugin Won’t Enable[](#plugin-wont-enable)

*   Check the Navidrome logs for error messages
*   Verify all required permissions are configured (users, libraries)
*   Ensure the plugin’s configuration requirements are met
*   Try setting `Plugins.LogLevel = "debug"` for more detailed logs

### Configuration Issues[](#configuration-issues)

*   Refer to the plugin’s documentation for required settings
*   Check that configuration values match the expected format
*   Look for validation errors in the logs

### Checking Logs[](#checking-logs)

Enable debug logging for plugins to troubleshoot issues:

```
[Plugins]
LogLevel = "debug" # or "trace" for more verbosity

```


Plugin-related log messages will contain `plugin=<plugin-name>` in them, making it easy to filter and identify issues.