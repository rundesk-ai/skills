use logstat::{summarize, EndpointStats};

const LOG: &str = "\
2026-10-01T12:00:00Z GET /a 200 10 5
2026-10-01T12:00:01Z GET /a 500 20 7
garbage line
2026-10-01T12:00:02Z POST /b 201 5 100
2026-10-01T12:00:03Z GET /a 200 30 9
";

#[test]
fn per_endpoint_rows_busiest_first() {
    let rows = summarize(LOG.as_bytes());
    assert_eq!(
        rows,
        vec![
            EndpointStats {
                endpoint: "GET /a".into(),
                requests: 3,
                errors: 1,
                bytes: 60,
                p95_ms: 9
            },
            EndpointStats {
                endpoint: "POST /b".into(),
                requests: 1,
                errors: 0,
                bytes: 5,
                p95_ms: 100
            },
        ]
    );
}
