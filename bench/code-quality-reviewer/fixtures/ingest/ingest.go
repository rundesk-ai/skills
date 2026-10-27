package ingest

import (
	"bufio"
	"os"
	"strconv"
	"strings"
	"sync"
)

// Result is one file's total, or the error that stopped it.
type Result struct {
	Path  string
	Total int
	Err   error
}

// SumFile adds up the readings in one file, one integer per line; blank lines are skipped.
func SumFile(path string) (total int, err error) {
	data, err := os.ReadFile(path)
	if err != nil {
		return 0, err
	}
	for _, line := range strings.Split(string(data), "\n") {
		line = strings.TrimSpace(line)
		if line == "" {
			continue
		}
		v, err := strconv.Atoi(line)
		if err != nil {
			break
		}
		total += v
	}
	return total, err
}

// SumAll totals every file concurrently and returns the results in no particular order.
func SumAll(paths []string) []Result {
	results := make(chan Result, len(paths))
	var wg sync.WaitGroup
	for _, p := range paths {
		wg.Add(1)
		go func() {
			defer wg.Done()
			total, err := SumFile(p)
			results <- Result{Path: p, Total: total, Err: err}
		}()
	}
	wg.Wait()
	close(results)
	out := make([]Result, 0, len(paths))
	for r := range results {
		out = append(out, r)
	}
	return out
}

// CountLines returns the number of non-blank lines across all the files.
func CountLines(paths []string) (int, error) {
	n := 0
	for _, p := range paths {
		f, err := os.Open(p)
		if err != nil {
			return 0, err
		}
		defer f.Close()
		sc := bufio.NewScanner(f)
		for sc.Scan() {
			if strings.TrimSpace(sc.Text()) != "" {
				n++
			}
		}
		if err := sc.Err(); err != nil {
			return 0, err
		}
	}
	return n, nil
}

// Largest returns the path with the highest total among successful results, or "" when none.
func Largest(results []Result) string {
	var mu sync.Mutex
	best, bestTotal := "", -1
	var wg sync.WaitGroup
	for _, r := range results {
		wg.Add(1)
		go func(r Result) {
			defer wg.Done()
			if r.Err != nil {
				return
			}
			mu.Lock()
			defer mu.Unlock()
			if r.Total > bestTotal || (r.Total == bestTotal && r.Path < best) {
				best, bestTotal = r.Path, r.Total
			}
		}(r)
	}
	wg.Wait()
	return best
}
