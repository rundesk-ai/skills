package ingest

import (
	"os"
	"path/filepath"
	"testing"
)

func write(t *testing.T, dir, name, body string) string {
	t.Helper()
	p := filepath.Join(dir, name)
	if err := os.WriteFile(p, []byte(body), 0o600); err != nil {
		t.Fatal(err)
	}
	return p
}

func TestSumFile(t *testing.T) {
	p := write(t, t.TempDir(), "a.txt", "3\n\n4\n5\n")
	total, err := SumFile(p)
	if err != nil || total != 12 {
		t.Fatalf("got %d, %v", total, err)
	}
}

func TestSumAllOneFile(t *testing.T) {
	p := write(t, t.TempDir(), "a.txt", "1\n2\n")
	got := SumAll([]string{p})
	if len(got) != 1 || got[0].Total != 3 || got[0].Path != p {
		t.Fatalf("got %+v", got)
	}
}

func TestCountLines(t *testing.T) {
	dir := t.TempDir()
	n, err := CountLines([]string{write(t, dir, "a", "1\n\n2\n"), write(t, dir, "b", "3\n")})
	if err != nil || n != 3 {
		t.Fatalf("got %d, %v", n, err)
	}
}

func TestLargest(t *testing.T) {
	got := Largest([]Result{{Path: "a", Total: 3}, {Path: "b", Total: 9}, {Path: "c", Total: 9}, {Path: "d", Total: 99, Err: os.ErrNotExist}})
	if got != "b" {
		t.Fatalf("got %q", got)
	}
}
