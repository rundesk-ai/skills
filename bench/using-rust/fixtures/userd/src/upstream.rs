//! Stand-in for the user directory the service fronts. Slow, and fails now and then.

use std::sync::atomic::{AtomicU64, Ordering};
use std::time::Duration;

#[derive(Debug, Clone, PartialEq)]
pub struct User {
    pub id: u64,
    pub name: String,
}

#[derive(Debug)]
pub struct UpstreamError;

static CALLS: AtomicU64 = AtomicU64::new(0);

pub async fn get_user(id: u64) -> Result<User, UpstreamError> {
    tokio::time::sleep(Duration::from_millis(20)).await;
    // Every fifth call fails, like the real directory under load.
    if CALLS.fetch_add(1, Ordering::Relaxed) % 5 == 4 {
        return Err(UpstreamError);
    }
    Ok(User { id, name: format!("user-{id}") })
}
