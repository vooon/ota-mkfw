
#[macro_use]
extern crate clap;
use clap::App;


fn main() {
    let yaml = load_yaml!("cli.yaml");
    let matches = App::from_yaml(yaml)
        .version(crate_version!())
        .get_matches();
}
