
#[macro_use]
extern crate clap;
use clap::{App, ArgMatches};

//extern crate cbor;
//use cbor::Encoder;

//#[feature(plugin)]
//#[plugin(serde_macros)]

extern crate serde;
extern crate serde_cbor;

use serde::ser::Serialize;
use serde::de::Deserialize;
use serde_cbor::to_writer;

use std::collections::HashMap;
use std::collections::BTreeMap;
use std::io::prelude::*;
use std::io::BufWriter;
use std::fs::File;

static MAGIC_OTAFWV1: &'static str = "OTAFWv1";
static UNKNOWN: &'static str = "UNKNOWN";
/*
//#[derive(Debug, PartialEq, Serialize)]
#[derive(Serialize, Deserialize)]
struct OFWFile {
    magic: String,
    description: String,
    //build_date: String, TAG0
    version: String,    // Aka git-identity
    revision: String,
    board: String,
    data: HashMap<String, OFWImage>,
}

//#[derive(Debug, PartialEq, Serialize)]
#[derive(Serialize, Deserialize)]
struct OFWImage {
    size: u64,
    sha1sum: Option<Vec<u8>>,
    load_addr: Option<u64>,
    dfu_alt: Option<u32>,
    payload: Vec<u8>,
}
*/
include!(concat!(env!("OUT_DIR"), "/lib.rs"));

impl OFWFile {
    fn new(description: &str, board: &str) -> OFWFile {
        OFWFile {
            magic: MAGIC_OTAFWV1.to_string(),
            description: description.to_string(),
            board: board.to_string(),

            version: UNKNOWN.to_string(),
            revision: UNKNOWN.to_string(),
            data: HashMap::new(),
        }
    }
}

fn do_mkfw(matches: &ArgMatches) {
    println!("{:?}", matches);

    let mut header = OFWFile::new(
        matches.value_of("desc").unwrap_or(""),
        matches.value_of("board").unwrap());

    //let mut header = HashMap::new();
    //header.insert("magic", MAGIC_OTAFWV1);
    //header.insert("description", matches.value_of("desc").unwrap_or(""));
    //header.insert("board", matches.value_of("board").unwrap());

    //let mut data = HashMap::new();
    //data.insert("firmware.bin", vec!["123", "321"]);

    //header.insert("data", data);

    println!("Header: {:?}", header);

    let mut file = File::create(matches.value_of("OUTPUT").unwrap()).unwrap();
    //let mut file = BufWriter::new(file);
    //let mut encoder = Encoder::from_writer(file);
    //encoder.encode(header);
    //encoder.flush();
    //
    to_writer(&mut file, &header);
}

fn do_upload(matches: &ArgMatches) {
    println!("{:?}", matches);
}

fn main() {
    let yaml = load_yaml!("cli.yaml");
    let matches = App::from_yaml(yaml)
        .version(crate_version!())
        .get_matches();

    match matches.subcommand() {
        ("mkfw", Some(subm)) => do_mkfw(subm),
        ("upload", Some(subm)) => do_upload(subm),
        _ => {},
    }
}
