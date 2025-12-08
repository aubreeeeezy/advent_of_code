package main

import (
    "bufio"
    "fmt"
    "os"
    "strings"
    "time"
)


type TachyonManifold struct {
    ManifoldState [][]rune
    StartRow int
    StartCol int
    Cache map[[2]int]int
}

func NewTachyonManifold(lines []string) *TachyonManifold{
    var startRow int = -1
    var startCol int = -1
    var manifoldState [][]rune = make([][]rune, len(lines))
    for r, line := range lines {
        manifoldState[r] = make([]rune, len(line))
        for c, ch := range line {
            manifoldState[r][c] = ch
            if ch == 'S' {
                startRow = r
                startCol = c
            }
        }
    }
    return &TachyonManifold{
        ManifoldState : manifoldState,
        StartRow: startRow,
        StartCol: startCol,
        Cache: make(map[[2]int]int),
    }
}

func GridToString(grid [][]rune) string {
    var b strings.Builder

    for _, row := range grid {
        for _, r := range row {
            b.WriteRune(r)
        }
        b.WriteByte('\n')
    }

    return b.String()
}

func (self *TachyonManifold) String() string{
    return GridToString(self.ManifoldState)
}

func (self *TachyonManifold) Percolate() int{
    var width int = len(self.ManifoldState[0])
    var height int = len(self.ManifoldState)
    var splits int = 0
    for r, row := range self.ManifoldState[0:height - 1]{
        for c, ch := range row {
            if ch == 'S' {
                self.ManifoldState[r + 1][c] = '|'
            } else if ch == '|'{
                if self.ManifoldState[r + 1][c] == '^'{
                    splits += 1 
                    if c > 0 {
                        self.ManifoldState[r + 1][c - 1] = '|'
                    } 
                    if c < width - 1 {
                        self.ManifoldState[r + 1][c + 1] = '|'
                    }
                } else {
                    self.ManifoldState[r + 1][c] = '|'
                }
            }
        }
    }
    return splits
}

func (self *TachyonManifold) PercolateQuantum() int {
    width := len(self.ManifoldState[0])
    height := len(self.ManifoldState)

    if self.Cache == nil {
        self.Cache = make(map[[2]int]int)
    }

    var subPercolate func(row, column int) int
    subPercolate = func(row, column int) int {
        key := [2]int{row, column}

        if v, ok := self.Cache[key]; ok {
            return v
        }

        if row == height-1 {
            return 1
        }

        below := self.ManifoldState[row+1][column]
        result := 0

        if below == '^' {
            if column == 0 {
                result += 1
            } else {
                result += subPercolate(row+1, column-1)
            }

            if column == width-1 {
                result += 1
            } else {
                result += subPercolate(row+1, column+1)
            }
        } else {
            result = subPercolate(row+1, column)
        }

        self.Cache[key] = result
        return result
    }

    return subPercolate(self.StartRow, self.StartCol)
}


func main() {
    start := time.Now()

    file, err := os.Open("../sample_beam.txt")
    if err != nil {
        panic(err)
    }
    defer file.Close()

    scanner := bufio.NewScanner(file)
    var lines []string
    for scanner.Scan() {
        lines = append(lines, scanner.Text())
    }
    if err := scanner.Err(); err != nil {
        panic(err)
    }
    var tm TachyonManifold = *NewTachyonManifold(lines) 
    part2 := tm.PercolateQuantum()
    part1 := tm.Percolate()
    

    fmt.Printf("part_1_calculation: %d\n", part1)
    fmt.Printf("part_2_calculation: %d\n", part2)

    elapsed := time.Since(start)
    fmt.Printf("took %s\n", elapsed)
}
