ota-mkfw: fimrware image packer
===============================

Simple proof-of-concept firmware image packer.
It works similar to [`px_mkfw.py`][1] from PX4 firmware,
except it uses [RFC-7049 (CBOR)][2] instead of JSON.
Thanks to binay format we may omit base64 encoding, and gzip is optional.


File format
-----------

For CBOR there exists own CDDL, but JSON-like is easier to understood:

```json
// File
[	// File root element is Array
	"OTAFWv1", 	// first element is magic string (in map it's position unpredictable)
	Metadata{},	// second - Metadata object (map)
	{		// third element - image map
		"firmware.bin": Image{},	// required
		"parameters.xml": Image{},	// optional additional data
		...
	}
]

// Metadata
{
	"description": "some description",
	"build_date": Tag(0, "<time>"),	// RFC3339, alternative: Tag(1, <posix time>)
	"version": "0.1.0",		// may be git identity
	"revision": "<git hash>",	// SCM revision. String.
	"board": "<some id>",		// Board ID, String
	...				// extensions
}

// Image
{
	"load_address": 0x00800000,		// optional, flash location
	"dfu_alt": 0,				// DFU Alternate setting number (look dfu-util)

	"size": 123,				// uncompressed size to verify payload
	"sha1sum": "<byte string (20 bytes)>",	// optional SHA1 digest of uncompressed data

	"image": "<uncompressed byte string>"	// File data. May be raw byte string and compressed (tagged)
						// deflated: Tag(12222, "<defalted byte string>")
	...	// extensions
}
```


[1]: https://github.com/PX4/Firmware/blob/master/Tools/px_mkfw.py
[2]: https://tools.ietf.org/html/rfc7049
