package main

import (
    "bufio"
    "fmt"
    "os"
    "time"
)

var NEIGHBOR_OFFSETS = [][2]int{
    {-1, -1}, {-1, 0}, {-1, 1},
    {0, -1},           {0, 1},
    {1, -1},  {1, 0},  {1, 1},
}

var THRESHOLD = 4

type PaperStack struct {
    Rolls  map[[2]int]struct{}
    Width  int
    Height int
}

func (ps *PaperStack) neighbors(i, j int) [][2]int {
    res := make([][2]int, 0, len(NEIGHBOR_OFFSETS))
    for _, d := range NEIGHBOR_OFFSETS {
        iRel := i + d[0]
        jRel := j + d[1]
        if 0 <= iRel && iRel < ps.Height && 0 <= jRel && jRel < ps.Width {
            res = append(res, [2]int{iRel, jRel})
        }
    }
    return res
}

func newPaperStack(stackStrLst []string) *PaperStack {
    height := len(stackStrLst)
    width := len(stackStrLst[0])

    rolls := make(map[[2]int]struct{}, height*width/2) // rough capacity guess
    for i, rowStr := range stackStrLst {
        for j, ch := range rowStr {
            if ch == '@' {
                rolls[[2]int{i, j}] = struct{}{}
            }
        }
    }

    return &PaperStack{
        Rolls:  rolls,
        Height: height,
        Width:  width,
    }
}

func (ps *PaperStack) buildHeat() [][]int {
    heat := make([][]int, ps.Height)
    for i := 0; i < ps.Height; i++ {
        heat[i] = make([]int, ps.Width)
    }

    for coord := range ps.Rolls {
        i, j := coord[0], coord[1]
        for _, n := range ps.neighbors(i, j) {
            ni, nj := n[0], n[1]
            heat[ni][nj]++
        }
    }
    return heat
}

func (ps *PaperStack) removeAllWithCascade() (part1, total int) {
    heat := ps.buildHeat()

    queue := make([][2]int, 0)
    inQueue := make([][]bool, ps.Height)
    for i := 0; i < ps.Height; i++ {
        inQueue[i] = make([]bool, ps.Width)
    }

    for coord := range ps.Rolls {
        i, j := coord[0], coord[1]
        if heat[i][j] < THRESHOLD {
            queue = append(queue, coord)
            inQueue[i][j] = true
        }
    }

    part1 = len(queue)

    for len(queue) > 0 {
        coord := queue[0]
        queue = queue[1:]

        i, j := coord[0], coord[1]

        if _, exists := ps.Rolls[coord]; !exists {
            continue
        }

        if heat[i][j] >= THRESHOLD {
            continue
        }

        delete(ps.Rolls, coord)
        total++

        for _, n := range ps.neighbors(i, j) {
            ni, nj := n[0], n[1]
            neighborCoord := [2]int{ni, nj}

            if _, ok := ps.Rolls[neighborCoord]; !ok {
                continue
            }

            heat[ni][nj]--
            if heat[ni][nj] < THRESHOLD && !inQueue[ni][nj] {
                queue = append(queue, neighborCoord)
                inQueue[ni][nj] = true
            }
        }
    }

    return part1, total
}

func main() {
    file, err := os.Open("../sample_stack.txt")
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

    paperStack := newPaperStack(lines)

    start := time.Now()

    part1, part2Total := paperStack.removeAllWithCascade()

    fmt.Printf("part_1_calculation: %d\n", part1)
    fmt.Printf("part_2_calculation: %d\n", part2Total)

    elapsed := time.Since(start)
    fmt.Printf("took %s\n", elapsed)
}
