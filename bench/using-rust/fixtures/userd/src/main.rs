mod upstream;

use std::collections::HashMap;
use std::sync::{Arc, Mutex};
use std::time::{Duration, Instant};

use upstream::{get_user, UpstreamError, User};

#[derive(Default)]
struct Cache {
    users: HashMap<u64, User>,
    misses: u64,
}

type Shared = Arc<Mutex<Cache>>;

async fn fetch_user(cache: Shared, id: u64) -> Result<User, UpstreamError> {
    let mut c = cache.lock().unwrap();
    if let Some(u) = c.users.get(&id) {
        return Ok(u.clone());
    }
    c.misses += 1;
    let mut attempt = 0;
    let user = loop {
        match get_user(id).await {
            Ok(u) => break u,
            Err(e) if attempt == 2 => return Err(e),
            Err(_) => {
                attempt += 1;
                std::thread::sleep(Duration::from_millis(100 * attempt));
            }
        }
    };
    c.users.insert(id, user.clone());
    Ok(user)
}

#[tokio::main]
async fn main() {
    let cache: Shared = Arc::default();
    let start = Instant::now();
    let mut handles = Vec::new();
    for i in 0..200u64 {
        let cache = cache.clone();
        handles.push(tokio::spawn(async move { fetch_user(cache, i % 50).await }));
    }
    let mut failed = 0;
    for h in handles {
        if h.await.unwrap().is_err() {
            failed += 1;
        }
    }
    let misses = cache.lock().unwrap().misses;
    println!(
        "200 requests, {misses} cache misses, {failed} failed, {:?}",
        start.elapsed()
    );
}
