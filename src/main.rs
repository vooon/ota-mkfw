
#[macro_use]
extern crate clap;
use clap::{App, ArgMatches};

extern crate cbor;
use cbor::Encoder;

//extern crate serialize;
//extern crate rustc_serialize;
//use rustc_serialize::{Encodable};
//use serialize::{Encodable};

use std::collections::HashMap;
use std::io::prelude::*;
use std::io::BufWriter;
use std::fs::File;

static MAGIC_OTAFWV1: &'static str = "OTAFWv1";
static UNKNOWN: &'static str = "UNKNOWN";

/*
#[derive(Debug, Encodable)]
struct OFWHeader {
    magic: String,
    description: String,
    //build_date: String, TAG0
    version: String,    // Aka git-identity
    revision: String,
    board: String,
    data: HashMap<String, OFWImage>,
}

#[derive(Debug, Encodable)]
struct OFWImage {
    size: u64,
    sha1sum: Option<Vec<u8>>,
    load_addr: Option<u64>,
    dfu_alt: Option<u32>,
    payload: Vec<u8>,
}

impl OFWHeader {
    fn new(description: &str, board: &str) -> OFWHeader {
        OFWHeader {
            magic: MAGIC_OTAFWV1.to_string(),
            description: description.to_string(),
            board: board.to_string(),

            version: UNKNOWN.to_string(),
            revision: UNKNOWN.to_string(),
            data: HashMap::new(),
        }
    }
}
*/

fn do_mkfw(matches: &ArgMatches) {
    println!("{:?}", matches);

    /*
    let mut header = OFWHeader::new(
        matches.value_of("desc").unwrap_or(""),
        matches.value_of("board").unwrap());
*/

    let mut header = HashMap::new();
    header.insert("magic", MAGIC_OTAFWV1);
    header.insert("description", matches.value_of("desc").unwrap_or(""));
    header.insert("board", matches.value_of("board").unwrap());

    println!("Make header: {:?}", header);

    let file = File::create(matches.value_of("OUTPUT").unwrap()).unwrap();
    //let mut writer = BufWriter::new(file);
    let mut encoder = Encoder::from_writer(file);
    encoder.encode(header);
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
