ota-mkfw: fimrware image packer
===============================

Simple proof-of-concept firmware image packer.
It works similar to [`px_mkfw.py`][1] from PX4 firmware,
except it uses [RFC-7049 (CBOR)][2] instead of JSON.
Thanks to binay format we may omit base64 encoding, and gzip is optional.


File format
-----------

For CBOR there exists own CDDL, but JSON-like is easier to understood:

```none
// File
[	                                // File root element is Array
    "OTAFWv1", 	                    // first element is magic string (in map it's position unpredictable)
    Metadata{},	                    // second - Metadata object (map)
    {                               // third element - image map
        "firmware.bin": Image{},    // required
        "parameters.xml": Image{},  // optional additional data
        ...
    }
]
// EOF

// Metadata object
{
    "description": "some description",                  // may be ""
    "build_date": Tag(0, "2016-02-09T23:57:09+0300"),   // RFC3339, alternative: Tag(1, <posix time>)
    "version": "0.1.0",                                 // may be `git describe`
    "revision": "<git hash>",                           // SCM revision.
    "board": "<some id>",                               // Board ID
    ...                                                 // extensions
}

// Image object
{
    "load_address": 0x00800000,             // optional, flash location
    "dfu_alt": 0,                           // optional, DFU Alternate setting number (look dfu-util)

    "size": 123,                            // uncompressed size to verify payload
    "sha1sum": "<byte string (20 bytes)>",  // optional, SHA1 digest of uncompressed data

    "image": "<uncompressed byte string>",  // File data. May be raw byte string and compressed (tagged)
                                            // deflated: Tag(12222, "<defalted byte string>")
    ...                                     // extensions
}
```


Comparison
----------

Current PX4 master (3e02bb1), px4fmu-v2: `.px4` file size is 847153, `.ofw` - 635442.
Both has same images of:

| image              | size (bytes) |
| ------------------ | ------------:|
| firmware_nuttx.bin |       992428 |
| parameters.xml     |       204128 |
| airframes.xml      |        21010 |

```
ota-mkfw -o nuttx-px4fmu-v2-default.ofw --desc PX4FMUv2 --board PX4FMUv2 --git-identity -n firmware.bin -a 0x00800000 --dfu-alt 0 -n parameters.xml -n airframes.xml firmware_nuttx.bin ../../../parameters.xml ../../../airframes.xml
```

The difference not so great, also base64 and JSON parser exist everywhere,
while CBOR require additional libraries.


[1]: https://github.com/PX4/Firmware/blob/master/Tools/px_mkfw.py
[2]: https://tools.ietf.org/html/rfc7049
