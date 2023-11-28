#!/usr/bin/env bash
set -u

CHECKS=(
	"Check the number of queens is correct"
	"Check the queens are in the board"
	"Check the queens are not attacking another queen vertically"
	"Check the queens are not attacking another queen horizontally"
	"Check the queens are not attacking another queen diagonally"
)

declare -A err_counters
for check in "${CHECKS[@]}"; do
    err_counters["$check"]=0
done

total_instances=0
invalid_answer=0
satisfiable=0
unsatisfiable=0

for instance in instances/**/*.txt; do
	(( total_instances++ ))
	has_sol=`./solved.bin --file ${instance} --quiet | grep "Solution found!"`

	output=`./nqueens.bin --file ${instance} --verify --quiet`
	exit_status=$?
	if [[ ${exit_status} -ne 0 ]]; then
		echo ""
		echo "ERROR: While solving the instance ${instance}, nqueens.bin failed (exit status ${exit_status})"
		exit -1
	fi

	if [[ "${output}" =~ "Solution found!" ]] && [[ -z "${has_sol}" ]]; then
		echo "- ${instance} reported SAT but it was UNSAT"
		(( invalid_answer++ ))
	elif [[ "${output}" =~ "No solution found!" ]] && [[ -n "${has_sol}" ]]; then
		echo "- ${instance} reported UNSAT but it was SAT"
		(( invalid_answer++ ))
	else
		if [[ "${output}" =~ "Solution found!" ]]; then
			(( satisfiable++ ))
		else 
			(( unsatisfiable++ ))
		fi

		for check in "${CHECKS[@]}"; do
			if [[ "${output}" =~ "${check}: Err" ]]; then
				echo "- ${instance} failed check ${check}"
				((err_counters["${check}"]++))
			fi
		done
	fi
done

echo ""
echo "SUMMARY"
echo "======="
echo "Tested ${total_instances} instances"
echo "SAT instances: ${satisfiable}"
echo "UNSAT instances: ${unsatisfiable}"
echo "SATisfiability query -> ${invalid_answer} errors"

for check in "${CHECKS[@]}"; do
	count="${err_counters[$check]}"
	echo "${check} -> ${count} instances with errors"
done

