package main

import (
    "bufio"
    "fmt"
    "os"
    "strings"
    "time"
)

const MULTIPLICATION_OPERATOR rune = '*'
const ADDITION_OPERATOR rune = '+'

type MathProblem struct {
    Numerals []int
    Operator rune
}

func parseUint(s string) int {
    n := 0
    for i := 0; i < len(s); i++ {
        c := s[i]
        if c < '0' || c > '9' {
            continue
        }
        n = n*10 + int(c-'0')
    }
    return n
}

func solve(problem MathProblem) int {
    var solution int
    for i, val := range problem.Numerals {
        if i == 0 {
            solution = val
            continue
        }
        if problem.Operator == MULTIPLICATION_OPERATOR {
            solution *= val
        } else if problem.Operator == ADDITION_OPERATOR {
            solution += val
        }
    }
    return solution
}

func solve_problems(problems []MathProblem) int {
    solution := 0
    for _, p := range problems {
        solution += solve(p)
    }
    return solution
}

func get_operator_position(operator_line string) []int {
    positions := make([]int, 0, len(operator_line)/2)
    for i, c := range operator_line { // c is rune
        if c == MULTIPLICATION_OPERATOR || c == ADDITION_OPERATOR {
            positions = append(positions, i)
        }
    }
    return positions
}

func get_problem_chunks(lines []string) [][]string {
    lineCount := len(lines)
    if lineCount == 0 {
        return nil
    }

    lineLength := len(lines[0])
    operatorPositions := get_operator_position(lines[lineCount-1])
    operatorCount := len(operatorPositions)

    chunks := make([][]string, operatorCount)

    for i, start := range operatorPositions {
        var end int
        if i == operatorCount-1 {
            end = lineLength
        } else {
            end = operatorPositions[i+1]
        }

        chunk := make([]string, lineCount)
        for r, line := range lines {
            chunk[r] = line[start:end]
        }
        chunks[i] = chunk
    }

    return chunks
}

func get_problem(problem_chunk []string) MathProblem {
    chunkLen := len(problem_chunk)
    numerals := make([]int, chunkLen-1)

    for i, val := range problem_chunk[:chunkLen-1] {
        n := parseUint(strings.TrimSpace(val))
        numerals[i] = n
    }

    op := rune(problem_chunk[chunkLen-1][0])

    return MathProblem{
        Numerals: numerals,
        Operator: op,
    }
}

func get_cephalid_problem(problem_chunk []string) MathProblem {
    chunkLen := len(problem_chunk)
    width := len(problem_chunk[0])

    columns := make([]string, width)

    // Build vertical columns from all but the last line (last is operator row)
    for c := 0; c < width; c++ {
        var b strings.Builder
        for _, line := range problem_chunk[:chunkLen-1] {
            b.WriteByte(line[c])
        }
        columns[c] = b.String()
    }

    numerals := make([]int, 0, width)
    for _, col := range columns {
        s := strings.TrimSpace(col)
        if s == "" {
            continue
        }
        n := parseUint(s)
        numerals = append(numerals, n)
    }

    op := rune(problem_chunk[chunkLen-1][0])

    return MathProblem{
        Numerals: numerals,
        Operator: op,
    }
}

func main() {
    start := time.Now()

    file, err := os.Open("../sample_homework.txt")
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

    var problems []MathProblem
    var problemsCephalid []MathProblem

    for _, chunk := range get_problem_chunks(lines) {
        problems = append(problems, get_problem(chunk))
        problemsCephalid = append(problemsCephalid, get_cephalid_problem(chunk))
    }

    part1 := solve_problems(problems)          // e.g. 8 workers
    part2 := solve_problems(problemsCephalid)

    fmt.Printf("part_1_calculation: %d\n", part1)
    fmt.Printf("part_2_calculation: %d\n", part2)

    elapsed := time.Since(start)
    fmt.Printf("took %s\n", elapsed)
}
