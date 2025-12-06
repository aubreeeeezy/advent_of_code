package main

import (
    "bufio"
    "fmt"
    "os"
    "time"
	"strconv"
	"strings"
	"sort" 
	"math"
)

type Range struct {
    Start int
	Stop int
}

type RangeSet struct {
	Ranges []Range
}

func (self *Range) overlaps(other Range) bool{
    return self.Start <= other.Stop && other.Start <= self.Stop
} 

func sortRanges(ranges []Range) {
	sort.Slice(ranges, func(i, j int) bool {
        if ranges[i].Start == ranges[j].Start {
            return ranges[i].Stop < ranges[j].Stop
        }
        return ranges[i].Start < ranges[j].Start
    })
}

func (self *Range) mergeRange(other Range) *Range{
    return &Range{
        Start: int(math.Min(float64(self.Start), float64(other.Start))),
        Stop:  int(math.Max(float64(self.Stop), float64(other.Stop))),
    }
}

func mergeRanges(ranges []Range) []Range {
    n := len(ranges)
    if n == 0 {
        return nil
    }
    if n == 1 {
        // return a copy to avoid surprising modifications of caller’s slice
        out := make([]Range, 1)
        out[0] = ranges[0]
        return out
    }

    // Make a copy so we don't reorder caller’s slice
    rs := make([]Range, n)
    copy(rs, ranges)

    // Sort by Start (and optionally End as tiebreaker)
    sortRanges(rs)

    merged := []Range{rs[0]}

    for i := 1; i < len(rs); i++ {
        last := &merged[len(merged)-1]
        cur := rs[i]

        if last.overlaps(cur) {
            *last = *last.mergeRange(cur)
        } else {
            merged = append(merged, cur)
        }
    }

    return merged
}

func newRangeSet(ranges []Range) *RangeSet {
	sortRanges(ranges)
	return &RangeSet{
		Ranges : mergeRanges(ranges),
	}
}

func (self *Range) contains(n int) bool{
	return self.Start <= n && n <= self.Stop
}

func (self *RangeSet) contains(n int) bool{
	for _, r := range self.Ranges {
		if r.contains(n){
			return true
		}
	}
	return false
}

func main() {
    file, err := os.Open("../sample_codes.txt")
    if err != nil {
        panic(err)
    }
    defer file.Close()

    scanner := bufio.NewScanner(file)
    var ranges []Range = make([]Range, 0)
	var switchProtocol bool
	var ids []int = make([]int, 0)
    for scanner.Scan() {
		line := scanner.Text()
		if len(line) > 0 {
			if switchProtocol {
				v, _ := strconv.Atoi(line)
				ids = append(ids, v)
			} else {
				parts := strings.Split(line, "-")
				start, _ := strconv.Atoi(parts[0])
				stop, _ := strconv.Atoi(parts[1])
				var r Range = Range{
					Start : start,
					Stop : stop,
				}
				ranges = append(ranges, r)
			}
		} else {
			switchProtocol = true
		}
    }
	if err := scanner.Err(); err != nil {
        panic(err)
    }

	var db RangeSet = *newRangeSet(ranges)
    start := time.Now()

    var part1, part2 int
	for _, id := range ids {
		if db.contains(id){
			part1 ++
		}
	}
	for _, r := range db.Ranges{
		part2 += (r.Stop - r.Start) + 1
	}
    fmt.Printf("part_1_calculation: %d\n", part1)
    fmt.Printf("part_2_calculation: %d\n", part2)

    elapsed := time.Since(start)
    fmt.Printf("took %s\n", elapsed)
}
