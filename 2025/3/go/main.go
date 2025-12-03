package main
import (
    "bufio"
    "fmt"
    "os"
	"strings"
	"strconv"
	"time"
	
)
type PowerBank struct{
	Jolts []int
}

func newPowerBank(bankStr string) *PowerBank {
	var jolts []int = make([]int, len(bankStr))
	for i := 0; i < len(bankStr); i++ {
		jolts[i] = int(bankStr[i] - '0')//Ascii magic '0'-'9' are consecutive so by subtracting the byte value for '0' from the byte value of the digit we get the int value

	}
	return &PowerBank{
		Jolts: jolts,
	}
}

func (self PowerBank) String() string{
	parts := make([]string, len(self.Jolts))
    for i, n := range self.Jolts {
        parts[i] = strconv.Itoa(n)
    }
    return strings.Join(parts, ",")
}

func cascadeIntSlice(slice []int, startingPos, startingValue int) {
    n := len(slice)
    for i := startingPos; i < n; i++ {
        slice[i] = startingValue + (i - startingPos)
    }
}

func (self PowerBank) getPositionalReading(numBatteries int) []int {
	var digitPositons []int = make([]int, numBatteries)
	cascadeIntSlice(digitPositons, 0, 0)  
	for currDigit := 0; currDigit < numBatteries; currDigit++ {
		for batteryPos := digitPositons[currDigit]; batteryPos <= len(self.Jolts) - numBatteries + currDigit; batteryPos ++ {
			if self.Jolts[batteryPos] > self.Jolts[digitPositons[currDigit]] {
				cascadeIntSlice(digitPositons, currDigit, batteryPos)
			}
		} 
	}
	return digitPositons
} 

func (self PowerBank) getReading(numBatteries int) int {
	var reading int = 0
	var posReading []int = self.getPositionalReading(numBatteries)
	for _, i := range posReading{
		reading = (reading * 10) + self.Jolts[i]
	}
	return reading
}

func processBank(b PowerBank) (int, int) {
	return b.getReading(2), b.getReading(12)
}

func main(){

	file, err := os.Open("../sample_banks.txt")
    if err != nil {
        panic(err)
    }
    defer file.Close()

	var banks []PowerBank
	scanner := bufio.NewScanner(file)
    for scanner.Scan() {
        line := scanner.Text()
		banks = append(banks, *newPowerBank(line))
	}

	start := time.Now()
	var part1Total, part2Total int
	for _, b := range banks {
		p1, p2 := processBank(b)
		part1Total += p1
		part2Total += p2
	}
	elapsed := time.Since(start)

	fmt.Printf("part_1_calculation: %d\n", part1Total)
	fmt.Printf("part_2_calculation: %d\n", part2Total)
	fmt.Printf("took %s\n",elapsed)
}