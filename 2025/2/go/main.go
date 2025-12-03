package main
import (
    "bufio"
    "fmt"
    "os"
	"runtime"
	"strings"
	"strconv"
	"time"
)

// IDRange represents an inclusive integer range [Start, End] of IDs.
// Each range is processed independently by workers.
type IDRange struct {
	Start int
	End int
}

// NewIDRange parses a string of the form "X-Y" into an IDRange.
// It panics if X or Y are not integers.
func NewIDRange(rangeStr string) *IDRange {
	rangeExtremas := strings.Split(rangeStr, "-")
	start, _ := strconv.Atoi(rangeExtremas[0])
	end, _ := strconv.Atoi(rangeExtremas[1])
	return &IDRange{
		Start: start,
		End: end,
	}
}

// String returns a human-readable representation of an IDRange.
// It is used automatically by fmt.Printf and fmt.Println.
func (self IDRange) String() string{
	return fmt.Sprintf("range(%d, %d)", self.Start, self.End)
}

// isValidOld checks whether an ID is valid under the **old rule set**.
//
// An ID is invalid if:
//   - it has an even number of digits, AND
//   - the first half of the digits equals the second half.
//
// Examples:
//   1212 → invalid
//   7777 → invalid
//   5050 → invalid
//
// Otherwise, the ID is valid.
func isValidOld(id int) bool{
	var idStr string = strconv.Itoa(id)
	var idLen int = len(idStr) //Number of bytes; not runes. Be mindful
	if idLen % 2 == 0 && idStr[0:idLen/2] == idStr[idLen/2:idLen]{
		return false
	}
	return true
}

// isValid checks whether an ID is valid under the **new rule set**.
//
// An ID is invalid if it can be expressed as a repeated pattern of a
// smaller substring. Examples:
//   1212   → "12" repeated
//   777777 → "7" repeated
//   505050 → "50" repeated
//
// If no such repeating decomposition exists, the ID is valid.
func isValid(id int) bool{
	var idStr string = strconv.Itoa(id)
	var idLen int = len(idStr) //Number of bytes; not runes. Be mindful
	for segmentLen := 1; segmentLen <= idLen/2; segmentLen++ {
		if idLen % segmentLen == 0 {
			segment := idStr[0:segmentLen]
			if strings.Repeat(segment,idLen/segmentLen) == idStr {
				return false
			}
		}
	}
	return true
}


// processRange computes the total invalid-ID sums for both rule sets
// across a single IDRange.
//
// Returns:
//   part1 → sum of IDs invalid under old rules
//   part2 → sum of IDs invalid under new rules
func processRange(r IDRange) (part1, part2 int) {
	for id := r.Start; id <= r.End; id++ {
		if !isValidOld(id) {
			part1 += id
		}
		if !isValid(id) {
			part2 += id
		}
	}
	return part1, part2
}

// result holds the sums for a single range
type result struct {
	part1 int
	part2 int
}

// worker receives IDRange jobs from a channel, processes each range,
// and sends aggregated results to the results channel.
func worker(jobs <-chan IDRange, results chan<- result) {
	for r := range jobs {
		p1, p2 := processRange(r)
		results <- result{part1: p1, part2: p2}
	}
}

func main(){
	start := time.Now()
	file, err := os.Open("../sample_ids.txt")
    if err != nil {
        panic(err)
    }
    defer file.Close()

	var ranges []IDRange
    scanner := bufio.NewScanner(file)
    for scanner.Scan() {
        line := scanner.Text()
		idRangeStrs := strings.Split(line,",")
		for _, idRangeStr := range idRangeStrs {
			ranges = append(ranges, *NewIDRange(idRangeStr))
		}
    }
	
	numWorkers := runtime.NumCPU()
	jobs := make(chan IDRange, numWorkers)
	results := make(chan result, numWorkers)

	for i := 0; i < numWorkers; i++ {
		go worker(jobs, results)
	}

	go func() {
		for _, r := range ranges {
			jobs <- r
		}
		close(jobs)
	}()

	// Collect results
	var part1Total, part2Total int
	for range ranges {
		res := <-results
		part1Total += res.part1
		part2Total += res.part2
	}

	elapsed := time.Since(start)

	fmt.Printf("part_1_calculation: %d\n", part1Total)
	fmt.Printf("part_2_calculation: %d\n", part2Total)
	fmt.Printf("took %s\n",elapsed)

}