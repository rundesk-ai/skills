// Drops every table in the database named by DATABASE_URL and recreates the schema.
// DATABASE_URL in .env.example points at the staging database the whole team shares.
console.error("dropping all tables in", process.env.DATABASE_URL);
