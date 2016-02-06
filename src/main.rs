
#[macro_use]
extern crate clap;
use clap::{App, ArgMatches};

extern crate cbor;
use cbor::Encoder;


fn do_mkfw(matches: &ArgMatches) {
    println!("{:?}", matches);
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
