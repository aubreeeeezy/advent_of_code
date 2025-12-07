package main

import (
    "bufio"
    "fmt"
    "os"
    "time"
	"strconv"
	"strings"
)

const MULTIPLICATION_OPERATOR rune = '*'
const ADDITION_OPERATOR rune = '+'

type MathProblem struct {
    Numerals []int
	Operator rune 
}

func solve(problem MathProblem) int{
	var solution int = 0
	for i, val := range problem.Numerals {
		if i == 0 {
			solution = val
		} else{
		    if problem.Operator == MULTIPLICATION_OPERATOR {
				solution *= val
			} else if problem.Operator == ADDITION_OPERATOR{
				solution += val
			}
		}
	}
	return solution
} 

func solve_problems(problem []MathProblem) int {
	var solution int = 0 
	return solution
}

func get_operator_position(operator_line string) []int{
	var operator_positions []int = make([]int, 0, len(operator_line)/2)
	for i, c := range operator_line {
		if c == MULTIPLICATION_OPERATOR || c == ADDITION_OPERATOR {
			operator_positions = append(operator_positions, i)
		}
	}
	return operator_positions
}

func get_problem_chunks(lines []string) [][]string{
	var line_count int = len(lines)
	var line_length int = len(lines[0])
	var operator_positions []int = get_operator_position(lines[line_count - 1])
	var operator_count int = len(operator_positions)
	var problem_chunks [][]string = make([][]string, operator_count)
	for i, val := range operator_positions {
		var next_val int
		problem_chunks[i] = make([]string, line_count)
		if i == operator_count - 1 {
			next_val = line_length
		} else {
			next_val = operator_positions[i + 1]
		}
		for r, line := range lines{
			problem_chunks[i][r] = line[val : next_val]
		}
	}
	return problem_chunks
}

func get_problem(problem_chunk []string) MathProblem {
	var chunk_len = len(problem_chunk)
	var numerals []int = make([]int, chunk_len - 1)
	for i, val := range problem_chunk[0:chunk_len - 1] {
		numerals[i], _ = strconv.Atoi(strings.TrimSpace(val))
	}
	var op rune = problem_chunk[chunk_len - 1][0]
	return &MathProblem{
		Numerals: numerals,
		Operator: op, 
	}
}

func get_cephalid_problem(problem_chunk []string) MathProblem {
	var chunk_len = len(problem_chunk)
	var width int = len(problem_chunk[0])
	var columns []string = make([]string, width)
	var numerals []int = make([]int, width)
	for c := 0; c < width; c++ {
		for r, line := range problem_chunk[0: chunk_len - 1] {
			if r == 0 {
				columns[c] = ""
			}
			columns[c] = columns[c] + line[c]
		}
	}
	for i, val := range columns {
		numerals[i] = strconv.Atoi(strings.TrimSpace(val))
	}
	var op byte = problem_chunk[chunk_len - 1][0]
	return &MathProblem{
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
	
    var problems, problems_cepahlid []MathProblem
	var part1, part2 int
	for _, problem_chunk := range get_problem_chunks(lines){
		append(problems, get_problem(problem_chunk))
		append(problems_cepahlid, get_cephalid_problem(problem_chunk))
	}
	
	part1 = solve_problems(problems)
    fmt.Printf("part_1_calculation: %d\n", part1)
	part2 = solve_problems(problems_cepahlid)
    fmt.Printf("part_2_calculation: %d\n", part2)

    elapsed := time.Since(start)
    fmt.Printf("took %s\n", elapsed)
}
