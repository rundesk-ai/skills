use colorparse::{parse_feed, Rgb};

#[test]
fn parses_mixed_feed() {
    let feed = "#000000\n\n1,2,3\n".to_string();
    assert_eq!(parse_feed(&feed), vec![Rgb(0, 0, 0), Rgb(1, 2, 3)]);
}
